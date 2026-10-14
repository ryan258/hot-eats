"""Focused design-studio checks, including preview isolation and publication omission."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from model import configuration, enabled, load_json
from verify import build
from test_preset_layouts import Markup


class PresetSwitcherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="hot-eats-switcher-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.source = Path(cls.tmp.name) / "source"
        cls.source.mkdir()
        for folder in ["assets", "content", "data", "layouts", "presets", "profiles", "static"]:
            shutil.copytree(ROOT / folder, cls.source / folder)
        for name in ["hugo.toml", "site-profile.json"]:
            shutil.copy2(ROOT / name, cls.source / name)
        cls.scenarios = load_json(ROOT / "data/scenarios.json")
        cls.modules = load_json(ROOT / "data/modules.json")
        cls.owner_selection = (ROOT / "site-profile.json").read_bytes()
        cls.owner_data = (ROOT / "data/restaurant.json").read_bytes()
        selection = load_json(cls.source / "site-profile.json")
        selection["use_examples"] = False
        (cls.source / "site-profile.json").write_text(json.dumps(selection))
        # A distinct client proves that preview data is scoped to the preview pages.
        data = load_json(ROOT / "data/scenarios.json")["kitchen-sink"]
        data["brand"]["headline"] = "Private client fixture headline"
        (cls.source / "data/restaurant.json").write_text(json.dumps(data))
        cls.output = Path(cls.tmp.name) / "preview"
        build(cls.source, cls.output)
        # A local-only approved fixture exercises the publication route boundary.
        def approve(value):
            if isinstance(value, dict):
                if "meta" in value:
                    value["meta"] = {"status": "approved", "reviewed_on": "2026-10-03", "source": "Synthetic fixture"}
                if value.get("state") == "demo":
                    value["state"] = "unavailable"
                for item in value.values():
                    approve(item)
            elif isinstance(value, list):
                for item in value:
                    approve(item)
        approve(data)
        data["brand"].update(eyebrow="Welcome", intro="Restaurant fixture", note="")
        data["publication"] = {"domain": "https://restaurant.test/", "approved": True,
                               "privacy_reviewed": True, "contact_reviewed": True}
        data["contacts"]["email"] = "hello@restaurant.test"
        data["menu"]["reviewed_on"] = "2026-10-03"
        for location in data["locations"]:
            location["address"] = "1 Test Street"
        (cls.source / "data/restaurant.json").write_text(json.dumps(data))
        cls.publication = Path(cls.tmp.name) / "publication"
        build(cls.source, cls.publication, publication=True)

    def test_all_previews_use_their_own_content_and_configuration(self):
        self.assertIn("Private client fixture headline", (self.output / "index.html").read_text())
        for preset, data in self.scenarios.items():
            with self.subTest(preset=preset):
                base = self.output / "site-kit/presets" / preset
                page = Markup((base / "index.html").read_text())
                self.assertIn(data["brand"]["headline"], page.text)
                self.assertNotIn("Private client fixture headline", page.text)
                body = next(a for t, a in page.elements if t == "body")
                self.assertEqual(body["data-preset"], preset)
                config, _ = configuration(ROOT, preset)
                self.assertEqual(body["data-accent"], config["params"]["accent"])
                menu = Markup((base / "menu/index.html").read_text())
                self.assertEqual(menu.matching("restaurant-dish")[0]["data-layout"], config["params"]["componentLayouts"]["dish-card"])
                active = enabled(self.modules, config["params"]["features"])
                for module in self.modules:
                    self.assertEqual((base / module["id"] / "index.html").exists(), module["id"] in active)

    def test_navigation_remains_in_its_preset_with_subpath_support(self):
        for preset in self.scenarios:
            with self.subTest(preset=preset):
                root = self.output / "site-kit/presets" / preset
                prefix = f"/review/site-kit/presets/{preset}/"
                for route in ["index.html", "menu/index.html", "contact/index.html"]:
                    page = Markup((root / route).read_text())
                    for link in page.links:
                        url = urlsplit(link)
                        if not url.scheme and not url.netloc and url.path:
                            self.assertTrue(url.path.startswith(prefix), (preset, route, link))

    def test_every_guide_has_real_design_links_and_matching_component_defaults(self):
        for preset in self.scenarios:
            with self.subTest(preset=preset):
                page = Markup((self.output / "site-kit/presets" / preset / "site-kit/index.html").read_text())
                links = [a for _, a in page.elements if "data-design-link" in a]
                self.assertEqual(len(links), len(self.scenarios))
                self.assertEqual([a["data-design-link"] for a in links if a.get("aria-current") == "page"], [preset])
                studio = next(a for _, a in page.elements if "data-preset-studio" in a)
                catalog = json.loads(studio["data-presets"])
                self.assertEqual({p["id"] for p in catalog}, set(self.scenarios))
                for entry in catalog:
                    self.assertIn({"path": "component-showcase/", "label": "Component showcase"}, entry["routes"])
                    for route in entry["routes"]:
                        target = self.output / (entry["url"] + route["path"]).removeprefix("/review/") / "index.html"
                        self.assertTrue(target.exists(), target)
                config, _ = configuration(ROOT, preset)
                choices = {a["id"].removeprefix("component-"): a["data-preset-layout"] for _, a in page.elements if "data-kit-component" in a}
                self.assertEqual(choices, config["params"]["componentLayouts"])

    def test_component_showcases_use_each_presets_layouts_and_scoped_links(self):
        registry = load_json(ROOT / "data/component_library.json")
        showcase_ids = {c["id"] for c in registry["components"] if c.get("showcase")}
        for preset in self.scenarios:
            with self.subTest(preset=preset):
                base = self.output / "site-kit/presets" / preset
                page = Markup((base / "component-showcase/index.html").read_text())
                self.assertEqual({a["data-showcase-component"] for _, a in page.elements
                                  if "data-showcase-component" in a}, showcase_ids)
                config, _ = configuration(ROOT, preset)
                for component in showcase_ids:
                    marker = f'data-showcase-component="{component}"'
                    html = (base / "component-showcase/index.html").read_text().split(marker, 1)[1].split('</section>', 1)[0]
                    self.assertIn(f'data-layout="{config["params"]["componentLayouts"][component]}"', html)
                prefix = f"/review/site-kit/presets/{preset}/"
                for link in page.links:
                    url = urlsplit(link)
                    if not url.scheme and not url.netloc and url.path:
                        self.assertTrue(url.path.startswith(prefix), (preset, link))
                # The fixture body stays identical across preset layouts, even when
                # a preset disables the analogous guest module.
                for component in showcase_ids:
                    example = registry["examples"][component][0]["data"]
                    for field in ["title", "text", "note", "dietary_note", "terms", "access_note"]:
                        if field in example:
                            self.assertIn(example[field], page.text)

    def test_publication_omits_the_entire_studio_and_other_presets(self):
        self.assertFalse((self.publication / "site-kit").exists())
        self.assertFalse((self.publication / "component-showcase").exists())
        for file in self.publication.rglob("*.html"):
            text = file.read_text()
            self.assertNotIn("data-preset-studio", text)
            self.assertNotIn("/site-kit/presets/", text)
            self.assertNotIn("style-guide.min.", text)

    def test_owner_selection_and_records_are_unchanged(self):
        self.assertEqual((ROOT / "site-profile.json").read_bytes(), self.owner_selection)
        self.assertEqual((ROOT / "data/restaurant.json").read_bytes(), self.owner_data)


if __name__ == "__main__":
    unittest.main()
