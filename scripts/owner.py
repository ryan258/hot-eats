#!/usr/bin/env python3
"""Local owner tools. Changes show a diff unless --apply is supplied; nothing publishes."""

import argparse
from contextlib import contextmanager
import copy
import csv
import datetime as dt
from decimal import Decimal, InvalidOperation
import difflib
import io
import json
import os
from pathlib import Path
import tempfile
import uuid
from model import (
    Invalid,
    load_json,
    load_validated,
    validate,
    date,
    mapping,
    sequence,
    text,
)

ROOT = Path(__file__).resolve().parents[1]


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def lock(root):
    local = root / ".local"
    local.mkdir(mode=0o700, exist_ok=True)
    p = local / "owner.lock"
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise Invalid(
            "Another owner operation may be active. If interrupted, inspect .local/owner.lock and remove it only after confirming no owner command is running."
        )
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        p.unlink(missing_ok=True)


def items(data):
    return [item for c in data["menu"]["categories"] for item in c["items"]]


def save_change(root, before, after, modules, config, apply, label):
    if before == after:
        print("No content differences. Nothing was saved.")
        return
    after["meta"]["status"] = "draft"
    after["publication"]["approved"] = False
    selected = copy.deepcopy(config)
    selected["params"]["useExamples"] = False
    validate(after, modules, selected, root)
    diff = "".join(
        difflib.unified_diff(
            encoded(before).splitlines(True),
            encoded(after).splitlines(True),
            fromfile="current",
            tofile="proposed",
        )
    )
    print(diff or "No content differences.")
    if not apply:
        print("Preview only. Add --apply to save this change.")
        return
    selection = load_json(root / "site-profile.json")
    new_selection = dict(selection, use_examples=False)
    key = (
        dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "-"
        + uuid.uuid4().hex[:8]
    )
    snapshot = {
        "id": key,
        "reason": label,
        "data": before,
        "selection": selection,
        "raw_restaurant": load_json(root / "data/restaurant.json"),
    }
    atomic(root / ".local/history" / f"{key}.json", encoded(snapshot))
    try:
        atomic(root / "data/restaurant.json", encoded(after))
        atomic(root / "site-profile.json", encoded(new_selection))
    except BaseException:
        atomic(root / "data/restaurant.json", encoded(snapshot["raw_restaurant"]))
        atomic(root / "site-profile.json", encoded(selection))
        raise
    print(
        f"Saved locally. Recovery snapshot: {key}. Publication approval reset. Run ./he preview."
    )


def decimal(value, label, positive=False):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise Invalid(f"{label}: expected a decimal number")
    if not result.is_finite() or result < 0 or (positive and result <= 0):
        raise Invalid(
            f"{label}: expected a finite {'positive' if positive else 'nonnegative'} number"
        )
    return result


def main(root=ROOT):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    sub.add_parser("history")
    today = sub.add_parser("today")
    today.add_argument("--announcement")
    today.add_argument("--location")
    today.add_argument("--date")
    today.add_argument("--closed", action="store_true")
    today.add_argument("--hours", help="HH:MM-HH:MM,HH:MM-HH:MM")
    today.add_argument("--service")
    today.add_argument(
        "--state", choices=["available", "unavailable", "paused", "demo"]
    )
    today.add_argument("--apply", action="store_true")
    menu = sub.add_parser("menu")
    menu.add_argument("--item")
    menu.add_argument("--state", choices=["available", "sold-out", "unavailable"])
    menu.add_argument("--price")
    menu.add_argument("--apply", action="store_true")
    restore = sub.add_parser("restore")
    restore.add_argument("snapshot")
    restore.add_argument("--apply", action="store_true")
    export = sub.add_parser("export-menu")
    export.add_argument("file")
    imp = sub.add_parser("import-menu")
    imp.add_argument("file")
    imp.add_argument("--apply", action="store_true")
    brief = sub.add_parser("brief")
    brief.add_argument("--date")
    cost = sub.add_parser("cost")
    cost.add_argument("recipe")
    cost.add_argument("--servings", type=str)
    scale = sub.add_parser("scale")
    scale.add_argument("quantity")
    scale.add_argument("unit")
    scale.add_argument("--from-servings", required=True)
    scale.add_argument("--to-servings", required=True)
    scale.add_argument("--to-unit")
    log = sub.add_parser("log")
    log.add_argument("kind", choices=["prep", "stock", "waste", "handoff"])
    log.add_argument("item")
    log.add_argument("--quantity", required=True)
    log.add_argument("--unit", required=True)
    log.add_argument("--note", default="")
    report = sub.add_parser("report")
    report.add_argument("--kind", choices=["prep", "stock", "waste", "handoff"])
    args = p.parse_args()
    with lock(root):
        data, modules, config, _, active = load_validated(root)
        after = copy.deepcopy(data)
        command = args.command
        if command == "check":
            warnings = []

            def inspect(value, path):
                if isinstance(value, dict):
                    if "meta" in value and value["meta"]["status"] != "approved":
                        warnings.append(path + ": " + value["meta"]["status"])
                    for k, v in value.items():
                        inspect(v, path + "." + k)
                elif isinstance(value, list):
                    for i, v in enumerate(value):
                        inspect(v, path + f"[{i}]")

            inspect(data, "restaurant")
            print(
                f"Valid schema {data['schema_version']}; {len(active)} enabled modules. {len(warnings)} content records need review."
            )
            print("\n".join(warnings))
            return
        if command == "history":
            for f in sorted((root / ".local/history").glob("*.json"), reverse=True):
                entry = load_json(f)
                print(f"{f.stem}  {entry['reason']}")
            return
        if command == "restore":
            if (
                "/" in args.snapshot
                or "\\" in args.snapshot
                or args.snapshot.startswith(".")
            ):
                raise Invalid("Use an exact snapshot ID from ./he history.")
            snapshot = load_json(root / ".local/history" / f"{args.snapshot}.json")
            after = snapshot["data"]
            save_change(
                root,
                data,
                after,
                modules,
                config,
                args.apply,
                "restore " + args.snapshot,
            )
            return
        if command == "today":
            if (args.date or args.closed or args.hours) and not args.location:
                raise Invalid(
                    "Hours, --closed, and --date require --location. Run ./he today to list locations."
                )
            if args.state and not args.service:
                raise Invalid(
                    "--state requires --service. Run ./he today to list services."
                )
            if not any([args.announcement is not None, args.location, args.service]):
                print(data["announcement"]["text"] or "No announcement.")
                for s in data["services"]:
                    print(f"{s['id']}: {s['state']}")
                for loc in data["locations"]:
                    print(f"{loc['id']}: {loc['name']} ({loc['timezone']})")
                return
            if args.announcement is not None:
                after["announcement"] = {
                    "text": args.announcement,
                    "start": "",
                    "end": "",
                }
            if args.location:
                loc = next(
                    (x for x in after["locations"] if x["id"] == args.location), None
                )
                if loc is None:
                    raise Invalid("Unknown location ID.")
                from zoneinfo import ZoneInfo

                day = (
                    args.date
                    or dt.datetime.now(ZoneInfo(loc["timezone"])).date().isoformat()
                )
                date(day, "date", True)
                if args.closed == bool(args.hours):
                    raise Invalid(
                        "Choose either --closed or --hours for a location exception."
                    )
                periods = (
                    []
                    if args.closed
                    else [part.strip().split("-") for part in args.hours.split(",")]
                )
                loc["exceptions"] = [
                    x for x in loc["exceptions"] if x["date"] != day
                ] + [
                    {
                        "date": day,
                        "intervals": periods,
                        "note": "Temporary closure" if args.closed else "Special hours",
                    }
                ]
                loc["meta"]["status"] = "draft"
            if args.service:
                service = next(
                    (s for s in after["services"] if s["id"] == args.service), None
                )
                if not service or not args.state:
                    raise Invalid("Choose an existing --service and its --state.")
                service["state"] = args.state
            save_change(root, data, after, modules, config, args.apply, "today")
            return
        if command == "menu":
            if (args.price is not None or args.state) and not args.item:
                raise Invalid(
                    "Choose --item when changing a price or availability. Run ./he menu to list IDs."
                )
            if not args.item:
                for item in items(data):
                    print(
                        f"{item['id']}: {item['name']} | {item['price']} {data['menu']['currency']} | {item['state']}"
                    )
                return
            item = next((i for i in items(after) if i["id"] == args.item), None)
            if not item:
                raise Invalid("Unknown item ID. Run ./he menu to list IDs.")
            if args.price is None and not args.state:
                print(
                    f"{item['id']}: {item['name']} | {item['price']} {data['menu']['currency']} | {item['state']}"
                )
                return
            if args.price is not None:
                item["price"] = args.price
            if args.state:
                item["state"] = args.state
            item["meta"]["status"] = "draft"
            after["menu"]["reviewed_on"] = ""
            save_change(
                root, data, after, modules, config, args.apply, "menu " + args.item
            )
            return
        if command == "export-menu":
            output = Path(args.file).expanduser()
            if output.exists():
                raise Invalid("Export destination exists; choose a new file.")
            with output.open("x", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["id", "name", "description", "price", "state"]
                )
                writer.writeheader()
                for item in items(data):
                    row = {k: item[k] for k in writer.fieldnames}
                    # Prevent formulas when opening the export in a spreadsheet.
                    for k, v in row.items():
                        if isinstance(v, str) and v.startswith(
                            ("=", "+", "-", "@", "\t", "\r")
                        ):
                            row[k] = "'" + v
                    writer.writerow(row)
            print(output)
            return
        if command == "import-menu":
            with Path(args.file).open(newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames != ["id", "name", "description", "price", "state"]:
                    raise Invalid("Use the columns and order produced by export-menu.")
                rows = list(reader)
            by_id = {i["id"]: i for i in items(after)}
            seen = set()
            for n, row in enumerate(rows, 2):
                key = row["id"]
                if (
                    key not in by_id
                    or key in seen
                    or None in row
                    or any(v is None for v in row.values())
                ):
                    raise Invalid(
                        f"CSV row {n}: unknown/duplicate ID or malformed columns; import updates existing items only."
                    )
                seen.add(key)
                for k, v in row.items():
                    if v.startswith("'") and len(v) > 1 and v[1] in "=+-@\t\r":
                        row[k] = v[1:]
                by_id[key].update(row)
                by_id[key]["meta"]["status"] = "draft"
            after["menu"]["reviewed_on"] = ""
            save_change(
                root, data, after, modules, config, args.apply, "menu CSV import"
            )
            return
        if command == "brief":
            from zoneinfo import ZoneInfo

            print(
                "PRE-SERVICE BRIEF — public data; confirm operational details with the team"
            )
            print(data["announcement"]["text"])
            for loc in data["locations"]:
                day = (
                    date(args.date, "date", True)
                    if args.date
                    else dt.datetime.now(ZoneInfo(loc["timezone"])).date()
                )
                exception = next(
                    (x for x in loc["exceptions"] if x["date"] == day.isoformat()), None
                )
                weekly = next(
                    (x for x in loc["hours"] if x["day"] == day.weekday()), None
                )
                schedule = exception if exception is not None else weekly
                print(
                    f"{loc['name']} | {day} | {schedule['intervals'] if schedule else 'Hours unknown'}"
                )
            for s in data["services"]:
                print(f"{s['label']}: {s['state']}")
            for item in items(data):
                if item["state"] != "available":
                    print(f"{item['name']}: {item['state']}")
            for key in ["specials", "calendar", "foodtruck"]:
                for row in data["collections"].get(key, []):
                    print(
                        f"{key}: {row['title']} | {row.get('start', '')} to {row.get('end', '')} | {row['state']}"
                    )
            return
        if command == "cost":
            recipe = mapping(load_json(args.recipe), "recipe")
            yield_count = decimal(recipe.get("yield_servings"), "yield_servings", True)
            total = Decimal(0)
            ingredients = sequence(recipe.get("ingredients"), "recipe.ingredients")
            if not ingredients:
                raise Invalid("Recipe needs at least one ingredient and its cost.")
            text(recipe.get("currency"), "recipe.currency", True, 30)
            for ingredient in ingredients:
                mapping(ingredient, "recipe.ingredient")
                text(ingredient.get("name"), "recipe.ingredient.name", True, 200)
                text(ingredient.get("unit"), "recipe.ingredient.unit", True, 50)
                quantity = decimal(ingredient["quantity"], "quantity")
                unit_cost = decimal(ingredient["cost_per_unit"], "cost_per_unit")
                waste = decimal(ingredient.get("waste_percent", 0), "waste_percent")
                if waste >= 100:
                    raise Invalid("waste_percent must be less than 100.")
                total += quantity * unit_cost / (1 - waste / 100)
            servings = (
                decimal(args.servings, "servings", True)
                if args.servings
                else yield_count
            )
            print(
                f"Ingredient estimate: {total / yield_count * servings:.2f} {recipe.get('currency', 'currency units')} for {servings} servings; {total / yield_count:.2f} per serving. Excludes labor, overhead, tax and service."
            )
            return
        if command == "scale":
            units = {
                "g": ("mass", "1"),
                "kg": ("mass", "1000"),
                "oz": ("mass", "28.349523125"),
                "lb": ("mass", "453.59237"),
                "ml": ("volume", "1"),
                "l": ("volume", "1000"),
                "tsp": ("volume", "4.92892159375"),
                "tbsp": ("volume", "14.78676478125"),
                "cup": ("volume", "236.5882365"),
                "piece": ("count", "1"),
            }
            source = units.get(args.unit)
            target = units.get(args.to_unit or args.unit)
            if not source or not target or source[0] != target[0]:
                raise Invalid(
                    "Use compatible units: g/kg/oz/lb, ml/l/tsp/tbsp/cup (US customary), or piece. Mass-to-volume needs ingredient density."
                )
            result = (
                decimal(args.quantity, "quantity")
                * decimal(args.to_servings, "to-servings", True)
                / decimal(args.from_servings, "from-servings", True)
                * Decimal(source[1])
                / Decimal(target[1])
            )
            print(
                f"{result.normalize()} {args.to_unit or args.unit}. Scaling arithmetic only; review preparation and seasoning."
            )
            return
        if command == "log":
            quantity = decimal(args.quantity, "quantity")
            entry = {
                "at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "kind": args.kind,
                "item": args.item,
                "quantity": str(quantity),
                "unit": args.unit,
                "note": args.note,
            }
            path = root / ".local/operations.jsonl"
            with os.fdopen(
                os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600),
                "a",
                encoding="utf-8",
            ) as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            print("Saved to the private local operations log.")
            return
        if command == "report":
            path = root / ".local/operations.jsonl"
            totals = {}
            for line in path.read_text().splitlines() if path.exists() else []:
                row = json.loads(line)
                if args.kind and row["kind"] != args.kind:
                    continue
                key = (row["kind"], row["item"], row["unit"])
                totals[key] = totals.get(key, Decimal(0)) + Decimal(row["quantity"])
            for (kind, item, unit), quantity in sorted(totals.items()):
                print(f"{kind}: {item}: {quantity} {unit}")
            print(
                "Handoffs are recorded actions, not evidence of completed orders or reservations."
            )
            return


if __name__ == "__main__":
    try:
        main()
    except (Invalid, OSError, KeyError, ValueError) as error:
        raise SystemExit(f"Cannot complete owner action: {error}")
