#!/usr/bin/env python3
"""Stage and validate an independent restaurant copy before reserving its destination."""

import argparse
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
from model import Invalid, identifier, load_validated, text

ROOT = Path(__file__).resolve().parents[1]


def copy_helper():
    if not (ROOT / "scripts/scaffold_core.py").is_file():
        owner = ROOT.parent / "the-website-factory/scripts"
        if not (owner / "scaffold_core.py").is_file():
            raise Invalid(
                "Shared helper missing: keep the sibling the-website-factory checkout, or use a generated client with scripts/scaffold_core.py."
            )
        sys.path.insert(0, str(owner))
    from scaffold_core import copy_sources

    return copy_sources


def sculpt(destination, name, slug, preset):
    target = Path(destination).expanduser().absolute()
    resolved = target.resolve()
    if resolved == ROOT or resolved.is_relative_to(ROOT):
        raise Invalid("Choose a destination outside the source project.")
    if target.exists() or target.is_symlink():
        raise Invalid(
            "Destination must not exist. Existing files are never overwritten."
        )
    if not target.parent.is_dir():
        raise Invalid("Destination parent must already exist.")
    text(name, "name", True, 150)
    identifier(slug, "slug")
    identifier(preset, "preset")
    data, modules, config, _, _ = load_validated(ROOT, preset)
    # All potentially failing transformations occur before the final destination exists.
    data = copy.deepcopy(data)
    data["meta"] = {"status": "draft", "reviewed_on": "", "source": ""}
    data["contacts"] = {
        "email": "",
        "phone": "",
        "response": "Response times to be confirmed.",
        "channels": [],
    }
    data["publication"] = {
        "domain": "",
        "approved": False,
        "privacy_reviewed": False,
        "contact_reviewed": False,
    }
    data["announcement"] = {"text": "", "start": "", "end": ""}
    for action in data["actions"]:
        action.update(
            url="",
            provider="",
            state="unavailable",
            fallback_email="",
            fallback_phone="",
            note="Service details and destination to be confirmed.",
            meta={"status": "draft", "reviewed_on": "", "source": ""},
        )
    for loc in data["locations"]:
        loc.update(
            address="",
            phone="",
            map_url="",
            hours=[],
            exceptions=[],
            meta={"status": "draft", "reviewed_on": "", "source": ""},
        )
        loc["access"] = {k: "To be confirmed." for k in loc["access"]}
    data["collections"]["reviews"] = []
    data["collections"]["careers"] = []
    for rows in data["collections"].values():
        for record in rows:
            record["url"] = ""
    for service in data["services"]:
        service["state"] = "unavailable"

    # Copying content never inherits approval or connected services.
    def reset(value):
        if isinstance(value, dict):
            if "meta" in value:
                value["meta"] = {"status": "draft", "reviewed_on": "", "source": ""}
            for item in value.values():
                reset(item)
        elif isinstance(value, list):
            for item in value:
                reset(item)

    reset(data)
    with tempfile.TemporaryDirectory(
        prefix=f".{slug}-stage-", dir=target.parent
    ) as tmp:
        stage = Path(tmp) / "source"
        copy_helper()(
            ROOT,
            stage,
            (
                "assets",
                "content",
                "data",
                "layouts",
                "static",
                "scripts",
                "docs",
                "presets",
                "examples",
            ),
            ("hugo.toml", ".gitignore", "README.md", "he"),
        )
        (stage / "profiles").mkdir()
        profile = f"profiles/{slug}.toml"
        quoted = json.dumps(name.strip(), ensure_ascii=False)
        (stage / profile).write_text(
            f"title = {quoted}\n[params]\ncompanyName = {quoted}\nprofileID = {json.dumps(slug)}\n",
            encoding="utf-8",
        )
        # Persist the resolved selection as the client's engine defaults too.
        client_config = copy.deepcopy(config)
        client_config["title"] = name.strip()
        client_config["baseURL"] = "/"
        client_config["params"].update(
            companyName=name.strip(),
            profileID=slug,
            useExamples=False,
            mode="preview",
            reviewOnly=True,
            noindex=True,
            publicationValidated=False,
        )

        def toml_table(value, prefix=()):
            lines = []
            if prefix:
                lines.append("[" + ".".join(json.dumps(k) for k in prefix) + "]")

            def is_tables(item):
                return (
                    isinstance(item, list)
                    and item
                    and all(isinstance(row, dict) for row in item)
                )

            for key, item in value.items():
                if not isinstance(item, dict) and not is_tables(item):
                    lines.append(
                        json.dumps(key) + " = " + json.dumps(item, ensure_ascii=False)
                    )
            for key, item in value.items():
                if isinstance(item, dict):
                    lines.extend([""] + toml_table(item, prefix + (key,)))
                elif is_tables(item):
                    # Arrays of tables, such as [[module.mounts]].
                    name = ".".join(json.dumps(k) for k in prefix + (key,))
                    for row in item:
                        lines.extend(["", "[[" + name + "]]"])
                        lines.extend(toml_table(row))
            return lines

        (stage / "hugo.toml").write_text(
            "\n".join(toml_table(client_config)) + "\n", encoding="utf-8"
        )
        (stage / "site-profile.json").write_text(
            json.dumps(
                {
                    "profile": profile,
                    "preset": f"presets/{preset}.toml",
                    "use_examples": False,
                },
                indent=2,
            )
            + "\n"
        )
        (stage / "data/restaurant.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        )
        (stage / "CLIENT-START.md").write_text(
            f"# {name.strip()}\n\nPreset: {preset}. Run `./he preview`. Edit `data/restaurant.json` or use `./he today` and `./he menu`. All retained menu, narrative, policy, and artwork examples require replacement or review. Contacts, schedules, provider connections, reviews, jobs, and approvals were cleared.\n\nUse `./he check` before review and `./he test` for the verification suite. Publication is a separate local build gate and never deploys. Read `docs/owner-guide.md`.\n"
        )
        load_validated(stage)
        reserved = False
        try:
            target.mkdir()
            reserved = True
            for child in stage.iterdir():
                shutil.move(str(child), str(target / child.name))
        except BaseException:
            if reserved:
                shutil.rmtree(target)
            raise
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--preset", default="diner")
    args = parser.parse_args()
    print(
        f"Created restaurant starter: {sculpt(args.destination, args.name, args.slug, args.preset)}"
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit(f"Cannot create starter: {error}")
