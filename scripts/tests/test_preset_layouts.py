"""Focused configuration and guest-page integration checks for preset layouts."""

import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from model import COMPONENT_LAYOUTS, Invalid, configuration, load_json, validate
from verify import build


class Markup(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.words = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, text):
        self.words.append(text)

    def matching(self, cls):
        return [a for _, a in self.elements if cls in a.get("class", "").split()]

    @property
    def text(self):
        return " ".join(" ".join(self.words).split())

    @property
    def links(self):
        return [a["href"] for t, a in self.elements if t == "a"]


class PresetLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="hot-eats-preset-contract-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.source = Path(cls.tmp.name) / "source"
        cls.source.mkdir()
        for name in ["assets", "content", "data", "layouts", "presets", "profiles", "config", "static"]:
            shutil.copytree(ROOT / name, cls.source / name)
        for name in ["hugo.toml", "site-profile.json"]:
            shutil.copy2(ROOT / name, cls.source / name)
        # Exercise all modules using non-default layouts, without editing owner data.
        config, _ = configuration(ROOT, "multi-location")
        cls.layouts = config["params"]["componentLayouts"]
        preset = cls.source / "presets/kitchen-sink.toml"
        preset.write_text(preset.read_text().split("[params.componentLayouts]")[0] +
                          "[params.componentLayouts]\n" + "\n".join(
                              f'{key} = "{value}"' for key, value in cls.layouts.items()))
        scenarios = load_json(cls.source / "data/scenarios.json")
        data = scenarios["kitchen-sink"]
        dish = data["menu"]["categories"][0]["items"][0]
        dish.update(price="0", state="sold-out", dietary=["Vegetarian"], options=["Add toast"],
                    location_ids=["location-1"], service_ids=["pickup"])
        for action in data["actions"]:
            if action["service_id"] in ["pickup", "delivery"]:
                action.update(state="available", url="https://example.com/" + action["id"],
                              fallback_email="help@example.com", fallback_phone="+12025550142")
        for service in data["services"]:
            if service["id"] == "pickup":
                service["state"] = "paused"
            elif service["id"] == "delivery":
                service["state"] = "available"
        event = data["collections"]["calendar"][0]
        event.update(state="available", start="2099-01-15T18:00:00-06:00", end="2099-01-15T20:00:00-06:00",
                     url="https://example.com/future-event")
        expired = copy.deepcopy(event)
        expired.update(id="past-event", start="2000-01-15T18:00:00-06:00", end="2000-01-15T20:00:00-06:00",
                       url="https://example.com/past-event")
        data["collections"]["calendar"].append(expired)
        review = copy.deepcopy(data["collections"]["specials"][0])
        review.update(id="review-fixture", title="Synthetic quotation", text="Local test quotation.",
                      attribution="Test fixture", url="https://example.com/review", state="available")
        data["collections"]["reviews"] = [review]
        data["contacts"].update(email="hello@example.com", phone="+12025550142", response="Reply expectation fixture.")
        data["locations"][0]["exceptions"] = [{"date": "2099-01-16", "intervals": [], "note": "Closure fixture"}]
        (cls.source / "data/scenarios.json").write_text(json.dumps(scenarios))
        cls.output = Path(cls.tmp.name) / "output"
        build(cls.source, cls.output, preset="kitchen-sink", example=True)

    def page(self, route):
        return Markup((self.output / route / "index.html").read_text())

    def test_registry_and_all_preset_choices_are_valid(self):
        registry = load_json(ROOT / "data/component_library.json")
        self.assertEqual(COMPONENT_LAYOUTS, {c["id"]: {l["id"] for l in c["layouts"]} for c in registry["components"]})
        modules = load_json(ROOT / "data/modules.json")
        scenarios = load_json(ROOT / "data/scenarios.json")
        for preset in scenarios:
            with self.subTest(preset=preset):
                config, _ = configuration(ROOT, preset)
                config["params"]["useExamples"] = True
                self.assertEqual(set(config["params"]["componentLayouts"]), set(COMPONENT_LAYOUTS))
                validate(scenarios[preset], modules, config, ROOT)

    def test_unsupported_preset_choices_fail_preflight(self):
        config, _ = configuration(ROOT, "kitchen-sink")
        data = load_json(ROOT / "data/scenarios.json")["kitchen-sink"]
        modules = load_json(ROOT / "data/modules.json")
        for invalid in [{"dish-card": "missing"}, {"unknown": "default"}, {"notice": []}]:
            with self.subTest(invalid=invalid):
                config["params"]["componentLayouts"] = invalid
                with self.assertRaisesRegex(Invalid, "params.componentLayouts"):
                    validate(data, modules, config, ROOT)

    def test_guest_pages_use_configured_components(self):
        cases = [("menu", "dish-card", "dish"), ("menu", "dietary-key", "dietary"),
                 ("ordering", "service-card", "service"), ("locations", "location-card", "location"),
                 ("locations", "hours-panel", "schedule"), ("specials", "offer-card", "offer"),
                 ("catering", "package-card", "package"), ("calendar", "event-card", "event"),
                 ("reviews", "quote-card", "quote"), ("faq", "faq-list", "questions"),
                 ("contact", "contact-panel", "contact"), ("", "notice", "notice")]
        for route, key, css in cases:
            with self.subTest(route=route, component=key):
                cards = self.page(route).matching("restaurant-" + css)
                self.assertTrue(cards, key)
                self.assertTrue(all(c["data-layout"] == self.layouts[key] for c in cards))

    def test_menu_keeps_zero_price_state_options_and_filter_hooks(self):
        page = self.page("menu")
        for text in ["0 USD", "Sold out", "Vegetarian", "Add toast"]:
            self.assertIn(text, page.text)
        dish = next(a for _, a in page.elements if a.get("id") == "dish-item-1")
        self.assertEqual(dish["data-locations"], "location-1")
        self.assertEqual(dish["data-services"], "pickup")
        self.assertIn("#dish-item-1", page.links)

    def test_service_pause_suppresses_provider_and_keeps_fallbacks(self):
        page = self.page("ordering")
        self.assertNotIn("https://example.com/ordering-pickup-location-1", page.links)
        self.assertIn("https://example.com/ordering-delivery-location-1", page.links)
        self.assertIn("mailto:help@example.com", page.links)
        self.assertIn("tel:+12025550142", page.links)
        self.assertIn("Paused", page.text)

    def test_calendar_expiry_and_download_contract(self):
        page = self.page("calendar")
        self.assertIn("https://example.com/future-event", page.links)
        self.assertNotIn("https://example.com/past-event", page.links)
        buttons = page.matching("calendar-download")
        self.assertEqual(len(buttons), 1)
        self.assertEqual(buttons[0]["data-end"], "2099-01-15T20:00:00-06:00")
        self.assertIn("Past event", page.text)
        self.assertIn("America/Chicago", page.text)

    def test_hours_faq_contact_and_guide_contracts(self):
        page = self.page("locations")
        self.assertIn("Closure fixture", page.text)
        self.assertTrue(all(a.get("data-timezone") and a.get("data-hours") for a in page.matching("location-hours")))
        self.assertTrue(all(a.get("role") == "status" for a in page.matching("hours-status")))
        faq = self.page("faq")
        self.assertTrue(any("data-location-card" in a and a.get("id", "").startswith("faq-") for _, a in faq.elements))
        self.assertIn("mailto:hello@example.com", self.page("contact").links)
        self.assertIn("Reply expectation fixture.", self.page("contact").text)
        guide = self.page("site-kit")
        choices = {a["id"].removeprefix("component-"): a["data-preset-layout"]
                   for _, a in guide.elements if "data-kit-component" in a}
        self.assertEqual(choices, self.layouts)
        selected = [a["value"] for tag, a in guide.elements if tag == "option" and "selected" in a]
        self.assertCountEqual(selected, self.layouts.values())


if __name__ == "__main__":
    unittest.main()
