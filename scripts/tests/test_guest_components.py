"""Focused guest integration and public-data boundary checks for the six additions."""

import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from model import Invalid, configuration, load_json, validate
from verify import build
from test_preset_layouts import Markup


class PresentationContractTests(unittest.TestCase):
    def setUp(self):
        self.data = load_json(ROOT / "data/scenarios.json")["kitchen-sink"]
        self.modules = load_json(ROOT / "data/modules.json")
        self.config, _ = configuration(ROOT, "kitchen-sink")
        self.config["params"]["useExamples"] = True

    def test_old_records_remain_valid_without_presentation(self):
        for rows in self.data["collections"].values():
            for row in rows:
                row.pop("presentation", None)
        validate(self.data, self.modules, self.config, ROOT)

    def test_presentation_cannot_override_identity_state_or_provider(self):
        for field, value in [("title", "Injected title"), ("state", "available"),
                             ("url", "https://example.com/injected"), ("link", {})]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data["collections"]["specials"][1]["presentation"][field] = value
                with self.assertRaisesRegex(Invalid, "unsupported presentation fields"):
                    validate(data, self.modules, self.config, ROOT)

    def test_components_are_scoped_to_their_collections(self):
        self.data["collections"]["team"][0]["presentation"]["component"] = "tasting-menu"
        with self.assertRaisesRegex(Invalid, "unsupported component"):
            validate(self.data, self.modules, self.config, ROOT)

    def test_selections_require_structure_serving_sizes_and_available_content(self):
        cases = [
            (1, "courses", [{"name": ""}], "name"),
            (1, "courses", ["Not an object"], "object"),
            (2, "items", [{"name": "Coffee", "portion": ""}], "portion"),
            (2, "items", [{"name": "Coffee", "portion": "90 ml", "url": "x"}], "unsupported selection"),
        ]
        for index, field, value, message in cases:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data["collections"]["specials"][index]["presentation"][field] = value
                with self.assertRaisesRegex(Invalid, message):
                    validate(data, self.modules, self.config, ROOT)
        row = self.data["collections"]["specials"][1]
        row["state"] = "available"
        row["presentation"]["courses"] = []
        with self.assertRaisesRegex(Invalid, "at least one entry"):
            validate(self.data, self.modules, self.config, ROOT)

    def test_record_images_use_the_existing_local_media_contract(self):
        image = self.data["collections"]["team"][0]["presentation"]["image"]
        image["src"] = "https://example.com/unreviewed.jpg"
        with self.assertRaises(Invalid):
            validate(self.data, self.modules, self.config, ROOT)
        image["src"] = "images/team-kitchen.svg"
        image["alt"] = ""
        with self.assertRaisesRegex(Invalid, "alt"):
            validate(self.data, self.modules, self.config, ROOT)


class GuestIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="hot-eats-guest-components-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.source = Path(cls.tmp.name) / "source"
        cls.source.mkdir()
        for folder in ["assets", "content", "data", "layouts", "presets", "profiles", "config", "static"]:
            shutil.copytree(ROOT / folder, cls.source / folder)
        for name in ["hugo.toml", "site-profile.json"]:
            shutil.copy2(ROOT / name, cls.source / name)
        cls.owner_data = (ROOT / "data/restaurant.json").read_bytes()
        cls.selection = (ROOT / "site-profile.json").read_bytes()
        cls.scenarios = load_json(cls.source / "data/scenarios.json")
        data = cls.scenarios["kitchen-sink"]
        for state in ["available", "paused", "expired", "cancelled", "sold-out", "unavailable", "demo"]:
            row = copy.deepcopy(data["collections"]["specials"][1])
            row.update(id=f"tasting-state-{state}", title=f"Tasting state {state}",
                       state="available" if state == "expired" else state,
                       url=f"https://example.com/tasting-{state}")
            if state == "expired":
                row.update(start="2000-01-01T18:00:00-06:00", end="2000-01-01T21:00:00-06:00")
            data["collections"]["specials"].append(row)
        data["locations"][0]["access"]["elevator"] = "Extra reviewed access fixture."
        dish = data["menu"]["categories"][0]["items"][0]
        dish.update(price="0", state="sold-out", dietary=["Vegetarian"], options=["Add toast"],
                    location_ids=["location-1"], service_ids=["pickup"])
        (cls.source / "data/scenarios.json").write_text(json.dumps(cls.scenarios))
        cls.output = Path(cls.tmp.name) / "site"
        build(cls.source, cls.output, preset="kitchen-sink", example=True)

    def page(self, preset, route):
        return Markup((self.output / "site-kit/presets" / preset / route / "index.html").read_text())

    def test_all_presets_render_guest_components_with_their_layout_choices(self):
        for preset in self.scenarios:
            config, _ = configuration(ROOT, preset)
            layouts = config["params"]["componentLayouts"]
            cases = [("menu", "menu-section", "menu-section"),
                     ("specials", "tasting-menu", "tasting"),
                     ("specials", "beverage-flight", "flight"),
                     ("team", "team-profile", "team"),
                     ("events", "dining-space", "space"),
                     ("accessibility", "visit-steps", "steps")]
            for route, component, css in cases:
                with self.subTest(preset=preset, component=component):
                    if not config["params"]["features"][route]:
                        self.assertFalse((self.output / "site-kit/presets" / preset / route).exists())
                        continue
                    cards = self.page(preset, route).matching("restaurant-" + css)
                    self.assertTrue(cards)
                    self.assertTrue(all(c["data-layout"] == layouts[component] for c in cards))

    def test_provider_and_calendar_actions_require_current_available_records(self):
        # Verify lists and record details use the same guards.
        for state in ["available", "paused", "expired", "cancelled", "sold-out", "unavailable", "demo"]:
            with self.subTest(state=state):
                detail = self.page("kitchen-sink", "specials/tasting-state-" + state)
                url = "https://example.com/tasting-" + state
                self.assertEqual(url in detail.links, state == "available")
                self.assertEqual(bool(detail.matching("calendar-download")), state == "available")
                row = detail.matching("record")[0]
                self.assertEqual(row["data-record-state"], state)
                self.assertEqual(url in self.page("kitchen-sink", "specials").links, state == "available")

    def test_menu_keeps_prices_modifiers_filters_and_permalinks(self):
        menu = self.page("kitchen-sink", "menu")
        for value in ["0 USD", "Sold out", "Vegetarian", "Add toast"]:
            self.assertIn(value, menu.text)
        dish = next(a for _, a in menu.elements if a.get("id") == "dish-item-1")
        self.assertEqual(dish["data-locations"], "location-1")
        self.assertEqual(dish["data-services"], "pickup")
        self.assertIn("#dish-item-1", menu.links)
        self.assertTrue(all("data-category" in card for card in menu.matching("restaurant-menu-section")))

    def test_location_steps_preserve_all_access_facts_and_location_context(self):
        data = self.scenarios["kitchen-sink"]
        access = self.page("kitchen-sink", "accessibility")
        wrappers = access.matching("visit-planning")
        self.assertEqual([w["data-location-card"] for w in wrappers], [l["id"] for l in data["locations"]])
        for location in data["locations"]:
            page = self.page("kitchen-sink", "locations/" + location["id"])
            self.assertEqual(page.matching("restaurant-steps")[0]["data-layout"], "default")
            for fact in location["access"].values():
                self.assertIn(fact, page.text)
                self.assertIn(fact, access.text)

    def test_new_record_details_search_fields_and_owner_data_isolation(self):
        for preset, data in self.scenarios.items():
            config, _ = configuration(ROOT, preset)
            for module in ["specials", "team", "events"]:
                if not config["params"]["features"][module]:
                    continue
                for row in data["collections"][module]:
                    detail = self.page(preset, module + "/" + row["id"])
                    self.assertIn(row["title"], detail.text)
                    self.assertIn(row["text"], detail.text)
        search = self.page("kitchen-sink", "search")
        self.assertTrue(any("Example seasonal preparation" in a.get("data-search-text", "") for _, a in search.elements))
        self.assertTrue(any("90 ml" in a.get("data-search-text", "") for _, a in search.elements))
        self.assertEqual((ROOT / "data/restaurant.json").read_bytes(), self.owner_data)
        self.assertEqual((ROOT / "site-profile.json").read_bytes(), self.selection)


if __name__ == "__main__":
    unittest.main()
