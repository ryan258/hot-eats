#!/usr/bin/env python3
"""Preview, check dependencies, or build a fresh review/publication artifact."""

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from model import Invalid, load_validated

ROOT = Path(__file__).resolve().parents[1]


def source_hashes(root):
    paths = [
        p
        for folder in [
            "assets",
            "layouts",
            "content",
            "data",
            "profiles",
            "presets",
            "scripts",
            "static",
        ]
        for p in (root / folder).rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    ]
    paths += [root / name for name in ["hugo.toml", "site-profile.json", "he"]]
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }


def doctor(root=ROOT):
    if not shutil.which("hugo"):
        raise Invalid(
            "Hugo 0.166.0 extended is required; install it before serving or building."
        )
    version = subprocess.run(
        ["hugo", "version"], capture_output=True, text=True, check=True
    ).stdout.strip()
    if "v0.166." not in version or "extended" not in version:
        raise Invalid(f"Expected Hugo 0.166.x extended; found {version}")
    load_validated(root)
    print(
        f"Ready: {version}; Python {sys.version.split()[0]}; selected content and configuration are valid."
    )
    if (
        not (root / "scripts/scaffold_core.py").is_file()
        and not (root.parent / "the-website-factory/scripts/scaffold_core.py").is_file()
    ):
        print(
            "Copying unavailable: restore the sibling factory helper or use a generated client with its frozen helper. Preview/build remain available."
        )


def run_site(
    root=ROOT,
    command="build",
    preset=None,
    mode="preview",
    destination=None,
    port=1417,
    base_url=None,
):
    root = Path(root).resolve()
    sources = source_hashes(root)
    data, modules, config, names, active = load_validated(
        root, preset, mode == "publication"
    )
    if not shutil.which("hugo"):
        raise Invalid(
            "Hugo was not found. Run python3 scripts/site.py doctor for setup guidance."
        )
    if command == "serve" and mode == "publication":
        raise Invalid(
            "Use a publication build for final output; serve is a local review."
        )
    output = None
    if command == "build":
        requested = (
            Path(destination).expanduser()
            if destination
            else Path(tempfile.mkdtemp(prefix="hot-eats-build-")) / "site"
        )
        if requested.is_symlink():
            raise Invalid("Build destination must not be a symlink.")
        output = requested.resolve()
        if (
            output.exists()
            or (output.parent / (output.name + "-manifest.json")).exists()
        ):
            raise Invalid(
                f"{output}: choose a new destination; existing output is never overwritten"
            )
        if output == root or output.is_relative_to(root):
            raise Invalid(
                "Build outside the source project to avoid stale or recursively copied artifacts."
            )
        output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="hot-eats-config-") as tmp:
        overlay = Path(tmp) / "mode.toml"
        publication = mode == "publication"
        base = (
            data["publication"]["domain"].rstrip("/") + "/"
            if publication
            else (base_url or config.get("baseURL", "/"))
        )
        overlay.write_text(
            "baseURL = "
            + json.dumps(base, ensure_ascii=False)
            + "\n"
            + "disableKinds = "
            + json.dumps(
                ["taxonomy", "term", "RSS"] + ([] if publication else ["sitemap"])
            )
            + "\n"
            + "[params]\nmode = "
            + json.dumps(mode)
            + "\n"
            + "useExamples = "
            + str(config["params"]["useExamples"]).lower()
            + "\n"
            + "reviewOnly = "
            + str(not publication).lower()
            + "\nnoindex = "
            + str(not publication).lower()
            + "\n"
            + "publicationValidated = "
            + str(publication).lower()
            + "\n",
            encoding="utf-8",
        )
        args = [
            "hugo",
            "--noBuildLock",
            "--config",
            ",".join(names + [str(overlay)]),
            "--panicOnWarning",
            "--environment",
            "production" if publication else "development",
        ]
        if command == "serve":
            args += [
                "server",
                "--bind",
                "127.0.0.1",
                "--port",
                str(port),
                "--disableFastRender",
                "--renderToMemory",
            ]
        else:
            args += ["--destination", str(output)]
        result = subprocess.run(args, cwd=root)
        if result.returncode:
            raise Invalid(
                "Hugo failed; review the diagnostics above. A failed output must not be published."
            )
    if output:
        if source_hashes(root) != sources:
            raise Invalid(
                "Source changed during the build. This output has no provenance manifest; build again to a new destination after edits finish."
            )
        manifest = {
            "schema_version": 2,
            "mode": mode,
            "preset": config["params"]["preset"],
            "base_url": base,
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "modules": sorted(active),
            "data_sha256": hashlib.sha256(
                json.dumps(data, sort_keys=True).encode()
            ).hexdigest(),
            "source_sha256": sources,
            "output_sha256": {
                str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in output.rglob("*")
                if p.is_file()
            },
            "published": False,
        }
        with (output.parent / (output.name + "-manifest.json")).open(
            "x", encoding="utf-8"
        ) as stream:
            stream.write(json.dumps(manifest, indent=2) + "\n")
        print(
            f"Built {mode} artifact: {output}\nManifest: {output.parent / (output.name + '-manifest.json')}\nNo files were published."
        )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["serve", "build", "doctor"])
    parser.add_argument(
        "--preset", choices=[p.stem for p in (ROOT / "presets").glob("*.toml")]
    )
    parser.add_argument(
        "--mode", choices=["demo", "preview", "publication"], default="preview"
    )
    parser.add_argument("--port", type=int, default=1417)
    parser.add_argument("--destination")
    parser.add_argument(
        "--base-url",
        help="Preview URL including any subpath; publication uses the reviewed domain",
    )
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        raise Invalid("Port must be between 1 and 65535.")
    if args.command == "doctor":
        doctor()
    else:
        run_site(
            command=args.command,
            preset=args.preset,
            mode=args.mode,
            destination=args.destination,
            port=args.port,
            base_url=args.base_url,
        )


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Cannot run site: {error}")
