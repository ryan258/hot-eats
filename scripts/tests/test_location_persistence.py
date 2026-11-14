"""Twenty-two whole-site.js cases over generated Menu/Privacy/Gallery HTML.

The JS runner uses a deliberately limited DOM adapter; it does not establish
native select restoration, native storage, keyboard, layout or browser behavior.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys

VOID = set("area base br col embed hr img input link meta param source track wbr".split())


class TreeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tree = {"tag": "document", "attrs": {}, "children": []}
        self.stack = [self.tree]

    def handle_starttag(self, tag, attrs):
        item = {"tag": tag, "attrs": {key: value or "" for key, value in attrs}, "children": []}
        self.stack[-1]["children"].append(item)
        if tag not in VOID:
            self.stack.append(item)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1]["children"].append(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True, type=Path, help="Actual synthetic Hugo output root")
    parser.add_argument("--script", required=True, type=Path, help="Entire actual production assets/js/site.js")
    parser.add_argument("--node", required=True, type=Path, help="Existing approved Node executable")
    args = parser.parse_args()
    documents = {}
    for preset in ["food-truck", "kitchen-sink"]:
        documents[preset] = {}
        for name in ["menu", "privacy", "gallery"]:
            route = f"/site-kit/presets/{preset}/{name}/"
            page = args.site / route.strip("/") / "index.html"
            parsed = TreeParser()
            parsed.feed(page.read_text())
            parsed.close()
            documents[preset][name] = {"route": route, "tree": parsed.tree}
    payload = {"documents": documents, "source": args.script.read_text(), "scriptPath": str(args.script.resolve())}
    command = [str(args.node), str(Path(__file__).with_name("location_persistence_runtime.cjs"))]
    result = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
