"""Rendered regression: location navigation follows enabled route generation."""

import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from model import load_json, load_validated
from verify import build
from test_preset_layouts import Markup


class LocationNavigationTests(unittest.TestCase):
    def test_multiple_locations_do_not_link_to_disabled_location_routes(self):
        with tempfile.TemporaryDirectory(prefix="hot-eats-location-navigation-") as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            for folder in ["assets", "content", "data", "layouts", "presets", "profiles", "static"]:
                shutil.copytree(ROOT / folder, source / folder)
            for name in ["hugo.toml", "site-profile.json"]:
                shutil.copy2(ROOT / name, source / name)
            scenarios = load_json(source / "data/scenarios.json")
            for preset in ["food-truck", "kitchen-sink"]:
                first = scenarios[preset]["locations"][0]
                second = copy.deepcopy(first)
                second.update(id="location-fixture-second", name="Second synthetic location",
                              address="", phone="", map_url="")
                scenarios[preset]["locations"].append(second)
            (source / "data/scenarios.json").write_text(json.dumps(scenarios))
            # Current client data also stays synthetic even if the owner has a client selected.
            (source / "data/restaurant.json").write_text(json.dumps(scenarios["kitchen-sink"]))
            selection = load_json(source / "site-profile.json")
            selection["use_examples"] = True
            (source / "site-profile.json").write_text(json.dumps(selection))
            data, _, _, _, active = load_validated(source, "food-truck")
            self.assertGreaterEqual(len(data["locations"]), 2)
            self.assertNotIn("locations", active)
            output = Path(tmp) / "site"
            build(source, output, preset="food-truck", example=True)
            truck = Markup((output / "menu/index.html").read_text())
            self.assertFalse(truck.matching("location-toggle"))
            self.assertFalse((output / "locations").exists())
            enabled = Markup((output / "site-kit/presets/kitchen-sink/menu/index.html").read_text())
            self.assertEqual(len(enabled.matching("location-toggle")), 1)
            self.assertTrue((output / "site-kit/presets/kitchen-sink/locations/location-fixture-second/index.html").is_file())


if __name__ == "__main__":
    unittest.main()
