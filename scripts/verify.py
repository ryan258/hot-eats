#!/usr/bin/env python3
"""Owner-run regression suite: contracts, JS syntax, fresh Hugo output and preset matrix.

No network calls, publishing, browser downloads, or changes to source data.
"""

from html.parser import HTMLParser
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit, unquote
from model import load_validated, load_json, validate, Invalid
import sculpt

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://restaurant.test/review/"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.noindex = False
        self.headings = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        for key in ["href", "src"]:
            if key in a:
                self.links.append(a[key])
        if "srcset" in a:
            self.links.extend(
                part.strip().split()[0] for part in a["srcset"].split(",")
            )
        if tag == "meta" and a.get("name") == "robots":
            self.noindex = "noindex" in a.get("content", "")
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self.headings.append(int(tag[1]))


def require(condition, message):
    if not condition:
        raise Invalid(message)


def run(args, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        raise Invalid(f"Command failed: {args}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def build(root, output, preset=None, publication=False, example=False):
    data, modules, config, names, active = load_validated(root, preset, publication)
    if example:
        data = load_json(root / "data/scenarios.json")[preset]
        config["params"]["useExamples"] = True
        active = validate(data, modules, config, root)
    mode = output.parent / (output.name + "-mode.toml")
    mode.write_text(
        "disableKinds = "
        + json.dumps(["taxonomy", "term", "RSS"] + ([] if publication else ["sitemap"]))
        + "\n[params]\nmode = "
        + json.dumps("publication" if publication else "preview")
        + "\nuseExamples = "
        + str(config["params"]["useExamples"]).lower()
        + "\npublicationValidated = "
        + str(publication).lower()
        + "\n"
    )
    run(
        [
            "hugo",
            "--noBuildLock",
            "--config",
            ",".join(names + [str(mode)]),
            "--destination",
            str(output),
            "--baseURL",
            BASE,
            "--panicOnWarning",
        ],
        root,
    )
    pages = {p: Page(p.read_text()) for p in output.rglob("*.html")}
    for path, page in pages.items():
        require(page.noindex != publication, f"Wrong indexing mode: {path}")
        require(len(page.ids) == len(set(page.ids)), f"Duplicate IDs: {path}")
        if path == output / "menu/index.html":
            main = Page(path.read_text().split("<main", 1)[1])
            for previous, current in zip(main.headings, main.headings[1:]):
                require(
                    current <= previous + 1,
                    f"Heading level skipped in menu: {previous} to {current}",
                )
        for link in page.links:
            u = urlsplit(link)
            if u.scheme or u.netloc:
                continue
            require(
                not u.path or u.path.startswith("/review/"), f"Subpath escape: {link}"
            )
            target = (
                path
                if not u.path
                else output / unquote(u.path.removeprefix("/review/"))
            )
            if target.is_dir():
                target /= "index.html"
            require(target.exists(), f"Broken local link: {link} in {path}")
            if u.fragment and target.suffix == ".svg":
                # Sprite references such as images/taco-icons.svg#tl-menu.
                require(
                    f'id="{unquote(u.fragment)}"' in target.read_text(encoding="utf-8"),
                    f"Missing sprite symbol: {link}",
                )
            elif u.fragment:
                require(
                    target in pages and unquote(u.fragment) in pages[target].ids,
                    f"Broken anchor: {link}",
                )
    require((output / "sitemap.xml").exists() == publication, "Wrong sitemap mode")
    for m in modules:
        require(
            (output / m["id"] / "index.html").exists() == (m["id"] in active),
            f"Wrong route state: {m['id']}",
        )
    index = json.loads((output / "index.json").read_text())
    require(len(index) == len(active), "Search index disagrees with enabled modules")
    require(
        (output / "site-kit/index.html").exists() != publication,
        "Operator guide mode leak",
    )
    for entry in index:
        if entry["url"].endswith("/locations/"):
            require("hours" in entry["keywords"].lower(), "Hours missing from search")
    home = (output / "index.html").read_text()
    if config["params"]["preset"] == "food-truck":
        require(
            'id="location-location-' not in home,
            "Fixed visit leaked into food-truck home",
        )
    return len(pages)


def main():
    print("Running data, copy, and recovery contracts…", flush=True)
    run([sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-v"])
    if not shutil.which("node"):
        raise Invalid(
            "Node is required only for the JavaScript syntax check; install/use an existing Node runtime and rerun."
        )
    run(["node", "--check", "assets/js/site.js"])
    counts = {}
    with tempfile.TemporaryDirectory(prefix="hot-eats-verify-") as tmp:
        temp = Path(tmp)
        counts["current-selection"] = build(ROOT, temp / "selected")
        for preset in sorted((ROOT / "presets").glob("*.toml")):
            counts[preset.stem] = build(
                ROOT, temp / preset.stem, preset.stem, example=True
            )
        client = temp / "client"
        sculpt.sculpt(client, "Unicode Café 🍽", "test-cafe", "cafe")
        build(client, temp / "client-build")
        # A real SVG resource exercises capability guards, not just the static fallback.
        (client / "assets/images").mkdir(exist_ok=True)
        shutil.copyfile(
            client / "static/images/breakfast.svg", client / "assets/images/asset.svg"
        )
        # Media/menu fixtures must not assume an owner's client has any dishes or photos.
        data = load_json(ROOT / "data/scenarios.json")["cafe"]
        data["gallery"][0]["src"] = "images/asset.svg"
        extra = copy.deepcopy(data["menu"]["categories"][0]["items"][0])
        extra["id"] = "extra-dish"
        extra["price"] = "0"
        data["menu"]["categories"][0]["items"].append(extra)
        (client / "data/restaurant.json").write_text(
            json.dumps(data, ensure_ascii=False)
        )
        build(client, temp / "asset-and-menu-edit")
        # Frozen client helper must create a second generation without a sibling factory.
        run(
            [
                sys.executable,
                "scripts/sculpt.py",
                "--destination",
                str(temp / "second-generation"),
                "--name",
                "Second Cafe",
                "--slug",
                "second-cafe",
                "--preset",
                "cafe",
            ],
            client,
        )

        # Publication fixture is intentionally synthetic and is never deployed.
        def approve(value):
            if isinstance(value, dict):
                if "meta" in value:
                    value["meta"] = {
                        "status": "approved",
                        "reviewed_on": "2026-10-03",
                        "source": "Synthetic local test fixture",
                    }
                if value.get("state") == "demo":
                    value["state"] = "unavailable"
                for item in value.values():
                    approve(item)
            elif isinstance(value, list):
                for item in value:
                    approve(item)

        approve(data)
        data["brand"].update(
            headline="A neighborhood table",
            intro="Restaurant fixture",
            eyebrow="Welcome",
            note="",
        )
        data["publication"] = {
            "domain": "https://restaurant.test/",
            "approved": True,
            "privacy_reviewed": True,
            "contact_reviewed": True,
        }
        data["contacts"]["email"] = "hello@restaurant.test"
        data["menu"]["reviewed_on"] = "2026-10-03"
        for loc in data["locations"]:
            loc["address"] = "1 Test Street"
        (client / "data/restaurant.json").write_text(
            json.dumps(data, ensure_ascii=False)
        )
        build(client, temp / "publication", publication=True)
        require(
            "preview-bar" not in (temp / "publication/index.html").read_text(),
            "Preview bar leaked into publication",
        )
    print(
        "PASS: contract regressions, JavaScript syntax, all ten preset builds, links/assets/anchors, Unicode client, frozen helper, SVG asset, edited menu, and publication output."
    )
    print("HTML page counts: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    print(
        "Still required: browser/assistive-technology checks, print and downloads, real business review, provider acceptance, and deployed headers."
    )


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError, ValueError) as error:
        raise SystemExit(f"FAIL: {error}")
