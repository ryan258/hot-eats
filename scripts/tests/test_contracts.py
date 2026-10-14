"""Targeted regression cases. Run through scripts/verify.py or unittest discovery."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from model import Invalid, load_json, load_validated, validate, configuration
import sculpt
from owner import save_change


class ModelTests(unittest.TestCase):
    def setUp(self):
        # Synthetic example fixtures stay independent of an owner's editable client.
        self.data = load_json(ROOT / "data/scenarios.json")["kitchen-sink"]
        self.modules = load_json(ROOT / "data/modules.json")
        self.config, _ = configuration(ROOT, "kitchen-sink")
        self.config["params"]["useExamples"] = True

    def reject(self, needle):
        with self.assertRaisesRegex(Invalid, needle):
            validate(self.data, self.modules, self.config, ROOT)

    def test_all_preset_contracts(self):
        scenarios = load_json(ROOT / "data/scenarios.json")
        for file in (ROOT / "presets").glob("*.toml"):
            with self.subTest(preset=file.stem):
                config, _ = configuration(ROOT, file.stem)
                config["params"]["useExamples"] = True
                validate(scenarios[file.stem], self.modules, config, ROOT)

    def test_current_selection_contract(self):
        load_validated(ROOT)

    def test_dependency_cycle_even_if_disabled(self):
        self.modules[0]["requires"] = [self.modules[1]["id"]]
        self.modules[1]["requires"] = [self.modules[0]["id"]]
        self.reject("cyclic")

    def test_unknown_reference(self):
        self.data["actions"][0]["location_id"] = "missing"
        self.reject("unknown location")

    def test_provider_service_location_must_match(self):
        action = next(a for a in self.data["actions"] if a.get("service_id"))
        service = next(
            s for s in self.data["services"] if s["id"] == action["service_id"]
        )
        service["location_ids"] = [
            l["id"] for l in self.data["locations"] if l["id"] != action["location_id"]
        ]
        self.reject("does not support")

    def test_duplicate_item(self):
        self.data["menu"]["categories"][0]["items"].append(
            copy.deepcopy(self.data["menu"]["categories"][0]["items"][0])
        )
        self.reject("duplicate item")

    def test_zero_price_is_valid(self):
        self.data["menu"]["categories"][0]["items"][0]["price"] = "0"
        validate(self.data, self.modules, self.config, ROOT)

    def test_invalid_price(self):
        self.data["menu"]["categories"][0]["items"][0]["price"] = "NaN"
        self.reject("decimal")

    def test_overlapping_hours(self):
        self.data["locations"][0]["hours"][0]["intervals"] = [
            ["08:00", "12:00"],
            ["11:00", "15:00"],
        ]
        self.reject("nonoverlapping")

    def test_overnight_split(self):
        self.data["locations"][0]["hours"][0]["intervals"] = [["22:00", "24:00"]]
        validate(self.data, self.modules, self.config, ROOT)

    def test_duplicate_exception(self):
        self.data["locations"][0]["exceptions"] = [
            {"date": "2026-10-12", "intervals": []},
            {"date": "2026-10-12", "intervals": []},
        ]
        self.reject("duplicate date")

    def test_provider_requires_https(self):
        self.data["actions"][0]["url"] = "javascript:alert(1)"
        self.reject("HTTPS")

    def test_provider_available_requires_url(self):
        self.data["actions"][0]["state"] = "available"
        self.reject("empty")

    def test_publication_blocks_demo(self):
        with self.assertRaises(Invalid):
            validate(self.data, self.modules, self.config, ROOT, True)

    def test_planner_catering_without_events(self):
        self.config["params"]["features"]["events"] = False
        self.config["params"]["features"]["catering"] = True
        self.config["params"]["features"]["planner"] = True
        self.assertIn("planner", validate(self.data, self.modules, self.config, ROOT))

    def test_planner_requires_one_gathering_service(self):
        features = self.config["params"]["features"]
        features.update(events=False, catering=False, planner=True)
        self.assertNotIn(
            "planner", validate(self.data, self.modules, self.config, ROOT)
        )

    def test_food_truck_has_schedule_not_fixed_visit(self):
        _, _, config, _, _ = load_validated(ROOT, "food-truck")
        self.assertFalse(config["params"]["features"]["visit"])
        self.assertIn("schedule", config["params"]["homeSections"])

    def test_changed_menu_size_is_valid(self):
        item = copy.deepcopy(self.data["menu"]["categories"][0]["items"][0])
        item["id"] = "another-dish"
        self.data["menu"]["categories"][0]["items"].append(item)
        validate(self.data, self.modules, self.config, ROOT)

    def test_unknown_public_root_field(self):
        self.data["private_staff_notes"] = "private"
        self.reject("unsupported public fields")

    def test_reserved_module(self):
        self.modules[0]["id"] = "privacy"
        self.config["params"]["features"]["privacy"] = True
        self.config["params"]["features"].pop("menu")
        self.reject("reserved")

    def test_naive_event_time(self):
        self.data["collections"]["calendar"][0]["start"] = "2026-10-10T11:00:00"
        self.reject("UTC offset")

    def test_nonstandard_date_separator_is_rejected(self):
        self.data["collections"]["calendar"][0]["start"] = "2026-10-10 11:00:00-05:00"
        self.reject("ISO date/time")

    def test_optional_dated_record_also_validated(self):
        self.data["collections"]["news"][0]["start"] = "2026-10-10T11:00:00"
        self.reject("UTC offset")

    def test_duplicate_gallery_id(self):
        self.data["gallery"].append(copy.deepcopy(self.data["gallery"][0]))
        self.reject("duplicate ID")

    def test_image_dimensions_are_positive_integers(self):
        self.data["gallery"][0]["width"] = -1
        self.reject("dimension")

    def test_attachment_symlink_cannot_escape_static(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "static").mkdir()
            (root / "private.txt").write_text("private")
            (root / "static/leak.txt").symlink_to(root / "private.txt")
            from model import local_file

            with self.assertRaisesRegex(Invalid, "inside static"):
                local_file("leak.txt", "attachment", root, ["static"])


class CopyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hot-eats-contract-")
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_unicode_and_frozen_helper(self):
        target = self.base / "cafe"
        sculpt.sculpt(target, 'Café 🍽 "Friends"', "test-cafe", "cafe")
        self.assertEqual(
            tomllib.loads((target / "profiles/test-cafe.toml").read_text())["params"][
                "companyName"
            ],
            'Café 🍽 "Friends"',
        )
        data, _, _, _, active = load_validated(target)
        self.assertIn("catering", active)
        self.assertNotIn("reservations", active)
        self.assertTrue((target / "scripts/scaffold_core.py").is_file())
        self.assertFalse(data["publication"]["approved"])
        self.assertFalse(any(a["url"] for a in data["actions"]))
        self.assertTrue(all(not l["hours"] for l in data["locations"]))
        self.assertFalse((target / ".local").exists())
        self.assertFalse((target / "public").exists())

    def test_existing_destination_survives(self):
        target = self.base / "existing"
        target.mkdir()
        sentinel = target / "keep"
        sentinel.write_text("owner")
        with self.assertRaises(Invalid):
            sculpt.sculpt(target, "Cafe", "cafe", "cafe")
        self.assertEqual(sentinel.read_text(), "owner")

    def test_late_validation_failure_leaves_no_destination(self):
        target = self.base / "failure"
        real = sculpt.load_validated

        def fail_stage(root, *args, **kwargs):
            if Path(root) != ROOT:
                raise Invalid("simulated staged failure")
            return real(root, *args, **kwargs)

        with patch.object(sculpt, "load_validated", side_effect=fail_stage):
            with self.assertRaisesRegex(Invalid, "staged failure"):
                sculpt.sculpt(target, "Cafe", "cafe", "cafe")
        self.assertFalse(target.exists())

    def test_partial_finalization_is_rolled_back(self):
        target = self.base / "partial"
        real = sculpt.shutil.move
        calls = 0

        def fail_move(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated move failure")
            return real(*args, **kwargs)

        with patch.object(sculpt.shutil, "move", side_effect=fail_move):
            with self.assertRaisesRegex(OSError, "move failure"):
                sculpt.sculpt(target, "Cafe", "cafe", "cafe")
        self.assertFalse(target.exists())

    def test_owner_edit_snapshots_and_invalidates_approval(self):
        target = self.base / "client"
        sculpt.sculpt(target, "Cafe", "cafe", "cafe")
        data, modules, config, _, _ = load_validated(target)
        data["publication"]["approved"] = True
        (target / "data/restaurant.json").write_text(json.dumps(data))
        after = copy.deepcopy(data)
        after["announcement"]["text"] = "Owner update fixture"
        with patch("builtins.print"):
            save_change(target, data, after, modules, config, True, "test announcement")
        current, _, _, _, _ = load_validated(target)
        self.assertEqual(current["announcement"]["text"], "Owner update fixture")
        self.assertFalse(current["publication"]["approved"])
        self.assertEqual(len(list((target / ".local/history").glob("*.json"))), 1)

    def test_owner_preview_does_not_mutate(self):
        target = self.base / "client"
        sculpt.sculpt(target, "Cafe", "cafe", "cafe")
        before = (target / "data/restaurant.json").read_bytes()
        data, modules, config, _, _ = load_validated(target)
        after = copy.deepcopy(data)
        after["announcement"]["text"] = "Temporary message"
        with patch("builtins.print"):
            save_change(target, data, after, modules, config, False, "preview")
        self.assertEqual((target / "data/restaurant.json").read_bytes(), before)


class BuildTests(unittest.TestCase):
    def test_existing_destination_survives(self):
        spec = importlib.util.spec_from_file_location(
            "hot_eats_site", ROOT / "scripts/site.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "existing"
            output.mkdir()
            (output / "keep").write_text("owner")
            with patch.object(module.shutil, "which", return_value="/test/hugo"):
                with self.assertRaisesRegex(Invalid, "existing output"):
                    module.run_site(destination=output)
            self.assertEqual((output / "keep").read_text(), "owner")

    def test_manifest_binds_fresh_output(self):
        spec = importlib.util.spec_from_file_location(
            "hot_eats_site", ROOT / "scripts/site.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        from types import SimpleNamespace
        import hashlib

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "new"

            def fake_hugo(*args, **kwargs):
                (output / "index.html").write_text("<p>Fixture</p>")
                return SimpleNamespace(returncode=0)

            with (
                patch.object(module.shutil, "which", return_value="/test/hugo"),
                patch.object(module.subprocess, "run", side_effect=fake_hugo),
                patch("builtins.print"),
            ):
                module.run_site(destination=output)
            manifest = load_json(Path(tmp) / "new-manifest.json")
            self.assertEqual(
                manifest["output_sha256"]["index.html"],
                hashlib.sha256((output / "index.html").read_bytes()).hexdigest(),
            )
            self.assertFalse(manifest["published"])


if __name__ == "__main__":
    unittest.main()
