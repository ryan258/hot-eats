"""Focused rendered checks for the living guide; no full preset/copy suite."""

from html.parser import HTMLParser
from html import unescape
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from verify import build, Page


class Previews(HTMLParser):
    """Collect each rendered preview without counting its escaped usage snippet."""

    def __init__(self, html):
        super().__init__()
        self.items = []
        self.current = None
        self.depth = 0
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.current is not None:
            if tag == "div":
                self.depth += 1
            if tag == "a":
                self.current["links"].append(attrs["href"])
        elif "sg-demo" in attrs.get("class", "").split():
            self.current = {
                "text": "", "links": [],
                "component": attrs["data-preview-component"],
                "layout": attrs["data-preview-layout"],
                "state": attrs["data-preview-state"],
            }
            self.depth = 1

    def handle_endtag(self, tag):
        if self.current is not None and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.items.append(self.current)
                self.current = None

    def handle_data(self, text):
        if self.current is not None:
            self.current["text"] += text


class ComponentLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="hot-eats-components-")
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.output = Path(cls.tmp.name) / "site"
        # Food truck intentionally disables locations and several other modules.
        # Existing build checks also verify subpath links, assets and duplicate IDs.
        build(ROOT, cls.output, preset="food-truck", example=True)
        cls.html = (cls.output / "site-kit/index.html").read_text()
        cls.previews = Previews(cls.html).items

    def preview(self, text, layout="default"):
        matches = [p for p in self.previews if text in p["text"] and p["layout"] == layout]
        self.assertEqual(len(matches), 1, text)
        return matches[0]

    def test_every_registered_component_and_state_is_rendered(self):
        data = json.loads((ROOT / "data/component_library.json").read_text())
        self.assertEqual(len(self.previews), sum(
            len(c["layouts"]) * len(data["examples"][c["id"]]) for c in data["components"]
        ))
        ids = Page(self.html).ids
        for component in data["components"]:
            self.assertIn("component-" + component["id"], ids)
            for layout in component["layouts"]:
                self.assertIn(f"layout-{component['id']}-{layout['id']}", ids)
                self.assertIn(f"code-{component['id']}-{layout['id']}", ids)
        self.assertNotIn('href="/review/locations/"', self.html)

    def test_unavailable_states_have_no_action(self):
        for text in [
            "Sunday cinnamon roll", "Seasonal fruit bowl",
            "Delivery is paused", "Reserve a table",
            "The last slice went fast", "A neighborhood supper",
            "Patio music evening", "We’re getting things ready",
            "The next seasonal table", "The next tasting flight",
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.preview(text)["links"], [])
        self.assertIn("Past event", self.preview("A neighborhood supper")["text"])
        self.assertIn("Cancelled", self.preview("Patio music evening")["text"])

    def test_every_layout_preserves_content_and_action_guards(self):
        # Compare all state/layout combinations against the original layout.
        # A visual choice must never remove facts or resurrect an unavailable CTA.
        defaults = {(p["component"], p["state"]): p for p in self.previews if p["layout"] == "default"}
        for preview in self.previews:
            with self.subTest(component=preview["component"], layout=preview["layout"], state=preview["state"]):
                original = defaults[preview["component"], preview["state"]]
                self.assertEqual(preview["links"], original["links"])
                self.assertEqual(" ".join(preview["text"].split()), " ".join(original["text"].split()))

    def test_available_actions_and_contact_links(self):
        self.assertEqual(self.preview("The slow morning")["links"], ["/review/menu/"])
        self.assertEqual(self.preview("Supper & a little live music")["links"], ["/review/contact/"])
        self.assertEqual(self.preview("A real conversation helps")["links"], [
            "tel:+12025550142", "mailto:hello@example.com",
        ])
        self.assertEqual(self.preview("An evening in three courses")["links"], ["/review/contact/"])
        self.assertEqual(self.preview("Three ways to take your coffee")["links"], ["/review/menu/"])
        self.assertEqual(self.preview("A visit with fewer surprises")["links"], [
            "/review/menu/", "/review/contact/",
        ])

    def test_new_components_keep_planning_details_and_empty_fallbacks(self):
        for title, details in {
            "From the morning kitchen": ["Sold out", "$12 / plate", "cross-contact"],
            "An evening in three courses": ["$68 / person", "cancellation", "dietary needs"],
            "Three ways to take your coffee": ["90 ml", "30 ml", "Contains caffeine"],
            "Alex Rivera": ["Fictional person", "Naturally leavened bread"],
            "The garden room": ["18 guests", "26 guests", "doorway width", "does not reserve"],
        }.items():
            with self.subTest(title=title):
                for detail in details:
                    self.assertIn(detail, self.preview(title)["text"])
        for title, fallback in {
            "A menu in the making": "Menu items are being confirmed",
            "The next seasonal table": "Courses are being confirmed",
            "The next tasting flight": "Flight selections are being confirmed",
            "Meet the next member of the team": "Profile details are being confirmed",
            "A new space to gather": "Capacity and room arrangements are being confirmed",
            "Planning information coming soon": "Visit steps are being confirmed",
        }.items():
            with self.subTest(title=title):
                preview = self.preview(title)
                self.assertIn(fallback, preview["text"])
                self.assertEqual(preview["links"], [])

    def test_no_javascript_reading_and_guide_asset_isolation(self):
        self.assertIn('data-kit-controls hidden', self.html)
        self.assertIn('<details><summary>Can I just walk in?</summary>', self.html)
        self.assertIn('>Usage & input data</summary>', unescape(self.html))
        self.assertIn('style-guide.min.', self.html)
        for route in ["index.html", "menu/index.html", "contact/index.html"]:
            guest = (self.output / route).read_text()
            self.assertNotIn('style-guide.min.', guest)
            self.assertNotIn('Fictional guest', guest)


if __name__ == "__main__":
    unittest.main()
