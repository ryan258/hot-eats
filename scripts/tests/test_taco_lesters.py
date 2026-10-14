"""Taco Lester's parody preset: disclosure, labelling, and where the optional notes appear."""

import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from model import load_validated
from verify import build

SCENARIO = json.loads((ROOT / "data/scenarios.json").read_text())["taco-lesters"]
NOTES = json.loads((ROOT / "data/parody_notes.json").read_text())


class TacoLestersData(unittest.TestCase):
    def test_preset_selection_validates(self):
        data, _, config, _, active = load_validated(ROOT, "taco-lesters")
        self.assertEqual(config["params"]["preset"], "taco-lesters")
        self.assertEqual(config["params"]["companyName"], "Taco Lester's")
        self.assertTrue({"menu", "team", "reviews", "faq"} <= active)

    def test_invented_people_reviews_and_menu_are_labelled(self):
        for row in SCENARIO["collections"]["team"]:
            self.assertIn("fictional", row["title"].lower(), row["id"])
            self.assertIn("Fictional", row["presentation"]["note"], row["id"])
        for row in SCENARIO["collections"]["reviews"]:
            self.assertIn("Fictional reviewer", row["attribution"], row["id"])
            self.assertEqual(row["url"], "")
        self.assertIn("invented", SCENARIO["menu"]["note"].lower())
        self.assertIn("no ingredient, allergen, or dietary claims", SCENARIO["menu"]["allergen_note"])
        for category in SCENARIO["menu"]["categories"]:
            for item in category["items"]:
                self.assertEqual(item["dietary"], [], item["id"])

    def test_notes_are_short_and_only_three_exist(self):
        self.assertEqual(set(NOTES), {"tilly", "lester", "marisol"})
        for key, note in NOTES.items():
            self.assertTrue(note["label"], key)
            self.assertTrue(1 <= len(note["lines"]) <= 3, key)


ICONS = json.loads((ROOT / "data/icons.json").read_text())


class TacoLestersIcons(unittest.TestCase):
    def test_sprite_symbols_match_the_catalogue(self):
        sprite = (ROOT / "static/images/taco-icons.svg").read_text()
        symbols = re.findall(r'<symbol id="tl-([a-z0-9-]+)" viewBox="0 0 24 24"', sprite)
        self.assertEqual(symbols, [icon["id"] for icon in ICONS])
        self.assertEqual(len(symbols), len(set(symbols)))
        self.assertEqual({icon["group"] for icon in ICONS}, {"Site functions", "Taco world"})
        for icon in ICONS:
            self.assertTrue(icon["label"] and icon["use"], icon["id"])
        self.assertEqual(sprite.count("<title>"), len(ICONS))
        self.assertNotRegex(sprite, r'(?i)(fill|stroke)="#')


class TacoLestersRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="hot-eats-taco-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.output = Path(cls.tmp.name) / "site"
        build(ROOT, cls.output, preset="taco-lesters", example=True)

    def read(self, route):
        return (self.output / route / "index.html").read_text() if route else (self.output / "index.html").read_text()

    def test_parody_notice_is_on_every_checked_page(self):
        for route in ["", "menu", "team", "faq", "contact"]:
            with self.subTest(route=route):
                page = self.read(route)
                self.assertIn('class="wrap parody-notice"', page)
                self.assertIn("No real restaurant is offered here.", page)

    def test_notes_are_closed_disclosures_on_their_own_pages(self):
        for route, note in [("", "tilly"), ("menu", "lester"), ("team", "marisol")]:
            with self.subTest(route=route):
                page = self.read(route)
                tags = re.findall(r'<details class="parody-note"[^>]*>', page)
                self.assertEqual(len(tags), 1)
                self.assertIn(f'data-parody-note="{note}"', tags[0])
                self.assertNotIn(" open", tags[0])
        for route in ["faq", "contact", "planner", "ordering"]:
            with self.subTest(route=route):
                self.assertNotIn("parody-note", self.read(route).replace("parody-notice", ""))

    def test_icon_sheet_is_in_the_taco_guide_only_and_icons_are_decorative(self):
        guide = (self.output / "site-kit/index.html").read_text()
        self.assertEqual(guide.count('class="sg-icon-card"'), len(ICONS))
        sheet = guide.split('id="icons"', 1)[1].split('id="library"', 1)[0]
        self.assertEqual(sheet.count('<svg class="icon" aria-hidden="true" focusable="false">'), len(ICONS))
        diner = (self.output / "site-kit/presets/diner/site-kit/index.html").read_text()
        self.assertNotIn('id="icons"', diner)
        self.assertNotIn('sg-icon-card', diner)

    def test_icons_sit_beside_visible_labels_in_navigation_cards_and_logo(self):
        home = self.read("")
        mark = re.search(r'<a class="wordmark"[^>]*>.*?</a>', home, re.S).group(0)
        self.assertIn('#tl-taco', mark)
        self.assertNotIn("\u2733", mark)
        quick = re.search(r'<nav class="quicklinks".*?</nav>', home, re.S).group(0)
        links = re.findall(r"<a [^>]*>(.*?)</a>", quick, re.S)
        self.assertTrue(links)
        for link in links:
            self.assertEqual(link.count("<svg class=\"icon\""), 1, link)
            self.assertTrue(re.sub(r"<svg.*?</svg>", "", link, flags=re.S).strip(), link)
        cards = re.findall(r'<a class="directory-card"[^>]*>(.*?)</a>', home, re.S)
        self.assertTrue(cards)
        for card in cards:
            self.assertEqual(card.count("<svg class=\"icon\""), 1, card)
        self.assertEqual(len(re.findall(r"<svg(?![^>]*aria-hidden=\"true\")[^>]*class=\"icon\"", home)), 0)

    def test_other_presets_do_not_show_icons_or_the_taco_mark(self):
        diner = (self.output / "site-kit/presets/diner/index.html").read_text()
        self.assertNotIn('<svg class="icon"', diner)
        self.assertIn("\u2733", diner)

    def test_other_presets_do_not_show_the_notes(self):
        page = (self.output / "site-kit/presets/diner/index.html").read_text()
        self.assertNotIn('data-parody-note=', page)
        taco = (self.output / "site-kit/presets/taco-lesters/index.html").read_text()
        self.assertIn('data-parody-note="tilly"', taco)


if __name__ == "__main__":
    unittest.main()
