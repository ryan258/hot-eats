"""Versioned public restaurant model, configuration resolution and preflight checks.

No network access or mutations. Python 3.11+; all failures identify a field.
"""

from __future__ import annotations
import copy
import datetime as dt
import json
from pathlib import Path
import re

try:
    import tomllib
except ModuleNotFoundError:
    raise SystemExit(
        "Hot Eats requires Python 3.11 or newer. Use a Python 3.11+ interpreter for these commands."
    )
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

VERSION = 2
COMPONENT_LAYOUTS = {
    "notice": {"default", "banner", "centered"},
    "dish-card": {"default", "horizontal", "compact"},
    "dietary-key": {"default", "grid", "inline"},
    "service-card": {"default", "horizontal", "compact"},
    "location-card": {"default", "split", "compact"},
    "hours-panel": {"default", "board", "compact"},
    "offer-card": {"default", "split", "ribbon"},
    "package-card": {"default", "split", "compact"},
    "event-card": {"default", "stacked", "row"},
    "quote-card": {"default", "centered", "compact"},
    "faq-list": {"default", "split", "cards"},
    "contact-panel": {"default", "split", "bar"},
    "menu-section": {"default", "board", "compact"},
    "tasting-menu": {"default", "split", "cards"},
    "beverage-flight": {"default", "board", "compact"},
    "team-profile": {"default", "horizontal", "compact"},
    "dining-space": {"default", "split", "compact"},
    "visit-steps": {"default", "timeline", "tiles"},
}
KINDS = {
    "menu",
    "locations",
    "action",
    "planner",
    "gallery",
    "faq",
    "contact",
    "records",
}
SHARED = {"visit", "search", "announcement", "quicklinks"}
SECTIONS = {
    "hero",
    "announcement",
    "ticker",
    "menu",
    "story",
    "visit",
    "directory",
    "schedule",
}
STATES = {
    "demo",
    "available",
    "unavailable",
    "paused",
    "sold-out",
    "cancelled",
    "expired",
}
ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CLOCK = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
PUBLIC_KEYS = {
    "schema_version",
    "meta",
    "brand",
    "announcement",
    "contacts",
    "locations",
    "services",
    "actions",
    "menu",
    "collections",
    "faq",
    "gallery",
    "policies",
    "publication",
}


class Invalid(ValueError):
    pass


def fail(path, message):
    raise Invalid(f"{path}: {message}")


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise Invalid(f"{path}: {error}") from error


def text(value, path, required=False, limit=20000):
    if (
        not isinstance(value, str)
        or len(value) > limit
        or any(ord(c) < 32 and c not in "\n\r\t" for c in value)
    ):
        fail(
            path,
            f"expected text of at most {limit} characters without control characters",
        )
    if required and not value.strip():
        fail(path, "required text is empty")
    return value


def sequence(value, path):
    if not isinstance(value, list):
        fail(path, "expected a list")
    return value


def mapping(value, path):
    if not isinstance(value, dict):
        fail(path, "expected an object")
    return value


def identifier(value, path):
    if not isinstance(value, str) or not ID.fullmatch(value):
        fail(path, "use a lowercase hyphenated ID")
    return value


def records(value, path):
    seen = set()
    for i, row in enumerate(sequence(value, path)):
        at = f"{path}[{i}]"
        mapping(row, at)
        key = identifier(row.get("id"), at + ".id")
        if key in seen:
            fail(at + ".id", "duplicate ID")
        seen.add(key)
    return seen


def references(value, allowed, path):
    sequence(value, path)
    if any(not isinstance(x, str) for x in value):
        fail(path, "references must be text IDs")
    if len(value) != len(set(value)):
        fail(path, "duplicate references")
    if any(not isinstance(x, str) or x not in allowed for x in value):
        fail(path, "unknown reference")


def url(value, path, required=False):
    text(value, path, required, 2048)
    if not value:
        return
    try:
        u = urlsplit(value)
    except ValueError:
        fail(path, "invalid URL")
    if (
        u.scheme != "https"
        or not u.hostname
        or u.username
        or u.password
        or any(c.isspace() for c in value)
    ):
        fail(path, "use an absolute HTTPS URL without credentials or whitespace")


def email(value, path):
    text(value, path, limit=254)
    if value and (
        not re.fullmatch(r"[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+", value)
        or any(c in value for c in "?&#")
    ):
        fail(path, "invalid email address")


def date(value, path, required=False):
    text(value, path, required)
    if not value:
        return None
    try:
        if not DAY.fullmatch(value):
            raise ValueError()
        return dt.date.fromisoformat(value)
    except ValueError:
        fail(path, "use YYYY-MM-DD")


def instant(value, path):
    text(value, path, True)
    try:
        if not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:\d{2})",
            value,
        ):
            raise ValueError()
        result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            raise ValueError()
        return result
    except ValueError:
        fail(path, "use an ISO date/time with an explicit UTC offset")


def local_file(value, path, root, folders):
    src = text(value, path, True)
    relative = Path(src)
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or any(c in src for c in "%?#\\")
        or urlsplit(src).scheme
    ):
        fail(path, "use a local path without traversal, URL parameters, or fragments")
    if root and not any(
        (Path(root) / folder / relative).is_file()
        and (Path(root) / folder / relative)
        .resolve()
        .is_relative_to((Path(root) / folder).resolve())
        for folder in folders
    ):
        fail(path, "file must exist inside " + ", ".join(folders))
    return relative


def metadata(value, path, publication=False):
    mapping(value, path)
    if value.get("status") not in {"demo", "draft", "approved", "stale"}:
        fail(path + ".status", "unknown content status")
    reviewed = date(value.get("reviewed_on", ""), path + ".reviewed_on")
    text(value.get("source", ""), path + ".source")
    if reviewed and reviewed > dt.date.today():
        fail(path + ".reviewed_on", "review date is in the future")
    if publication and (
        value.get("status") != "approved" or not reviewed or not value.get("source")
    ):
        fail(path, "publication needs approved status, review date, and source")


def merge(a, b):
    result = copy.deepcopy(a)
    for key, value in b.items():
        result[key] = (
            merge(
                result.get(key, {}) if isinstance(result.get(key), dict) else {}, value
            )
            if isinstance(value, dict)
            else copy.deepcopy(value)
        )
    return result


def configuration(root, preset=None):
    root = Path(root).resolve()
    selection = load_json(root / "site-profile.json")
    mapping(selection, "site-profile.json")
    chosen = f"presets/{preset}.toml" if preset else selection.get("preset")
    names = ["hugo.toml", selection.get("profile"), chosen]
    config = {}
    for name in names:
        if not isinstance(name, str) or "," in name:
            fail("configuration", "expected a TOML path without commas")
        path = (root / name).resolve()
        if not path.is_relative_to(root) or path.suffix != ".toml":
            fail(name, "configuration must be inside this project")
        try:
            config = merge(config, tomllib.loads(path.read_text(encoding="utf-8")))
        except (ValueError, OSError) as error:
            fail(name, str(error))
    config.setdefault("params", {})["useExamples"] = selection.get("use_examples", True)
    if type(config["params"]["useExamples"]) is not bool:
        fail("use_examples", "expected true or false")
    return config, names


def enabled(modules, features):
    by_id = {m["id"]: m for m in modules}
    memo = {}
    visiting = set()

    def check(key):
        if key in visiting:
            fail("modules.requires", f"cyclic dependency at {key}")
        if key in memo:
            return memo[key]
        if key not in by_id:
            fail("modules.requires", f"unknown module {key}")
        visiting.add(key)
        m = by_id[key]
        all_on = all([check(x) for x in m.get("requires", [])])
        any_on = (
            any([check(x) for x in m.get("requires_any", [])])
            if m.get("requires_any")
            else True
        )
        memo[key] = features.get(key, False) and all_on and any_on
        visiting.remove(key)
        return memo[key]

    return {m["id"] for m in modules if check(m["id"])}


def read_site(root, preset=None):
    root = Path(root)
    config, names = configuration(root, preset)
    modules = load_json(root / "data/modules.json")
    p = config["params"]
    data = (
        load_json(root / "data/scenarios.json").get(p.get("preset"))
        if p["useExamples"]
        else load_json(root / "data/restaurant.json")
    )
    if data is None:
        fail("params.preset", "no demonstration dataset for preset")
    return copy.deepcopy(data), modules, config, names


def validate(data, modules, config, root=None, publication=False):
    """Reject malformed state before templates or owner mutations consume it."""
    mapping(data, "restaurant")
    unknown = set(data) - PUBLIC_KEYS
    if unknown:
        fail(
            "restaurant",
            f"unsupported public fields: {sorted(unknown)}; keep private data in .local",
        )
    if data.get("schema_version") != VERSION:
        fail("schema_version", f"expected {VERSION}; see docs/data-model.md")
    metadata(data.get("meta"), "meta", publication)
    ids = records(modules, "modules")
    p = mapping(config.get("params"), "params")
    layouts = mapping(p.get("componentLayouts", {}), "params.componentLayouts")
    for component, layout in layouts.items():
        if component not in COMPONENT_LAYOUTS or not isinstance(layout, str) or layout not in COMPONENT_LAYOUTS[component]:
            fail("params.componentLayouts." + component, "unknown component or unsupported layout")
    for key in ["designName", "designDescription"]:
        text(p.get(key, ""), "params." + key)
    features = mapping(p.get("features"), "params.features")
    for key, value in features.items():
        if key not in ids | SHARED or type(value) is not bool:
            fail("params.features." + key, "unknown feature or non-boolean value")
    for m in modules:
        if m.get("kind") not in KINDS:
            fail("modules." + m["id"] + ".kind", "unsupported renderer")
        for key in ["title", "description", "label", "group", "keywords", "inputs"]:
            text(m.get(key), f"modules.{m['id']}.{key}", True)
        for key in ["requires", "requires_any"]:
            references(m.get(key, []), ids, f"modules.{m['id']}.{key}")
    if ids & {"privacy", "search", "site-kit"}:
        fail("modules.id", "ID collides with a reserved route")
    active = enabled(modules, features)
    sections = sequence(p.get("homeSections"), "params.homeSections")
    if len(sections) != len(set(sections)) or any(s not in SECTIONS for s in sections):
        fail("params.homeSections", "unknown or duplicate section")
    text(p.get("companyName"), "params.companyName", True, 150)
    brand = mapping(data.get("brand"), "brand")
    for key in ["headline", "intro", "eyebrow", "tagline", "note", "story_title"]:
        text(brand.get(key), "brand." + key)
    for key in ["story", "ticker"]:
        for value in sequence(brand.get(key), "brand." + key):
            text(value, "brand." + key)

    def image(row, path):
        mapping(row, path)
        local_file(row.get("src"), path + ".src", root, ["assets", "static"])
        text(row.get("alt"), path + ".alt", True)
        for key in ["width", "height"]:
            if key in row and (type(row[key]) is not int or not 1 <= row[key] <= 50000):
                fail(
                    path + "." + key,
                    "use a positive integer dimension of at most 50000 pixels",
                )

    if brand.get("image"):
        image(brand["image"], "brand.image")
    loc_ids = records(data.get("locations"), "locations")
    service_ids = records(data.get("services"), "services")
    for loc in data["locations"]:
        at = "locations." + loc["id"]
        text(loc.get("name"), at + ".name", True)
        text(loc.get("address"), at + ".address", publication and "locations" in active)
        text(loc.get("phone"), at + ".phone")
        url(loc.get("map_url", ""), at + ".map_url")
        metadata(loc.get("meta"), at + ".meta", publication)
        try:
            ZoneInfo(loc["timezone"])
        except (KeyError, ZoneInfoNotFoundError, TypeError):
            fail(at + ".timezone", "use an IANA timezone")
        days = set()

        def intervals(value, path):
            previous = -1
            for interval in sequence(value, path):
                if (
                    not isinstance(interval, list)
                    or len(interval) != 2
                    or any(
                        not isinstance(t, str)
                        or not (CLOCK.fullmatch(t) or (n == 1 and t == "24:00"))
                        for n, t in enumerate(interval)
                    )
                ):
                    fail(path, "use [HH:MM, HH:MM] intervals")
                start, end = [int(t[:2]) * 60 + int(t[3:]) for t in interval]
                if start >= end or start < previous:
                    fail(
                        path,
                        "intervals must be ordered, nonoverlapping and within one day; split overnight hours at midnight",
                    )
                previous = end

        for row in sequence(loc.get("hours"), at + ".hours"):
            day = row.get("day")
            if type(day) is not int or day not in range(7) or day in days:
                fail(
                    at + ".hours", "days are unique integers 0=Monday through 6=Sunday"
                )
            days.add(day)
            intervals(row.get("intervals"), at + ".hours")
        exceptions = set()
        for row in sequence(loc.get("exceptions"), at + ".exceptions"):
            d = date(row.get("date"), at + ".exceptions.date", True)
            if d in exceptions:
                fail(at + ".exceptions", "duplicate date")
            exceptions.add(d)
            intervals(row.get("intervals"), at + ".exceptions")
            text(row.get("note", ""), at + ".exceptions.note")
        access = mapping(loc.get("access"), at + ".access")
        for k, v in access.items():
            text(v, at + ".access." + k)
    for service in data["services"]:
        references(service.get("location_ids"), loc_ids, "services.location_ids")
        text(service.get("label"), "services.label", True)
        if service.get("state") not in STATES:
            fail("services.state", "unknown state")
    by_service = {service["id"]: service for service in data["services"]}
    records(data.get("actions"), "actions")
    for action in data["actions"]:
        at = "actions." + action["id"]
        if action.get("module") not in ids:
            fail(at + ".module", "unknown module")
        if action.get("location_id") not in loc_ids:
            fail(at + ".location_id", "unknown location")
        if action.get("service_id") and action["service_id"] not in service_ids:
            fail(at + ".service_id", "unknown service")
        if action.get("service_id"):
            locations = by_service[action["service_id"]]["location_ids"]
            if locations and action["location_id"] not in locations:
                fail(at + ".location_id", "service does not support this location")
        if action.get("state") not in STATES:
            fail(at + ".state", "unknown state")
        url(action.get("url", ""), at + ".url", action.get("state") == "available")
        for k in ["label", "provider", "note", "terms", "fallback_phone"]:
            text(action.get(k, ""), at + "." + k)
        email(action.get("fallback_email", ""), at + ".fallback_email")
        metadata(
            action.get("meta"), at + ".meta", publication and action["module"] in active
        )
        if (
            publication
            and action["module"] in active
            and action["state"] == "available"
            and not (action.get("fallback_email") or action.get("fallback_phone"))
        ):
            fail(at, "available provider needs an accessible contact alternative")
    menu = mapping(data.get("menu"), "menu")
    if not re.fullmatch(r"[A-Z]{3}", menu.get("currency", "")):
        fail("menu.currency", "use a three-letter currency code")
    date(
        menu.get("reviewed_on", ""),
        "menu.reviewed_on",
        publication and "menu" in active,
    )
    for key in ["note", "allergen_note"]:
        text(menu.get(key), "menu." + key)
    records(menu.get("categories"), "menu.categories")
    item_ids = set()
    for category in menu["categories"]:
        if category["id"] == "all":
            fail("menu.category.id", "all is reserved for the filter")
        text(category.get("label"), "menu.category.label", True)
        text(category.get("eyebrow", ""), "menu.category.eyebrow")
        for item in sequence(category.get("items"), "menu.items"):
            at = "menu.items." + identifier(item.get("id"), "menu.items.id")
            if item["id"] in item_ids:
                fail(at, "duplicate item ID")
            item_ids.add(item["id"])
            for k in ["name", "description"]:
                text(item.get(k), at + "." + k, k == "name")
            price = item.get("price", "")
            if not isinstance(price, str) or (
                price and not re.fullmatch(r"\d{1,7}(?:\.\d{1,2})?", price)
            ):
                fail(at + ".price", "use a nonnegative decimal string or empty text")
            if item.get("state") not in {"available", "sold-out", "unavailable"}:
                fail(at + ".state", "unknown item state")
            references(item.get("location_ids"), loc_ids, at + ".location_ids")
            references(item.get("service_ids"), service_ids, at + ".service_ids")
            for key in ["options", "dietary"]:
                for v in sequence(item.get(key), at + "." + key):
                    text(v, at + "." + key)
            metadata(item.get("meta"), at + ".meta", publication and "menu" in active)
    collections = mapping(data.get("collections"), "collections")
    for key, rows in collections.items():
        if key not in ids:
            fail("collections." + key, "unknown module")
        records(rows, "collections." + key)
        for row in rows:
            at = "collections." + key + "." + row["id"]
            metadata(row.get("meta"), at + ".meta", publication and key in active)
            text(row.get("title"), at + ".title", True)
            text(row.get("text"), at + ".text")
            references(row.get("location_ids", []), loc_ids, at + ".location_ids")
            if row.get("state") not in STATES:
                fail(at + ".state", "unknown state")
            url(row.get("url", ""), at + ".url")
            if (
                key in {"calendar", "specials", "foodtruck"}
                or row.get("start")
                or row.get("end")
            ):
                if instant(row.get("end"), at + ".end") <= instant(
                    row.get("start"), at + ".start"
                ):
                    fail(at, "end must follow start")
                try:
                    ZoneInfo(row.get("timezone"))
                except (ZoneInfoNotFoundError, TypeError):
                    fail(at + ".timezone", "use an IANA timezone")
            for field in ["attribution", "venue"]:
                text(row.get(field, ""), at + "." + field)
            for fact in sequence(row.get("facts", []), at + ".facts"):
                text(fact.get("label"), at + ".facts.label", True)
                text(fact.get("value"), at + ".facts.value", True)
            for asset in sequence(row.get("attachments", []), at + ".attachments"):
                local_file(asset.get("src"), at + ".attachment.src", root, ["static"])
                text(asset.get("label"), at + ".attachment.label", True)
            if (
                publication
                and key == "reviews"
                and (not row.get("url") or not row.get("attribution"))
            ):
                fail(at, "review requires original source URL and attribution")
    records(data.get("gallery"), "gallery")
    for row in data["gallery"]:
        image(row, "gallery")
        metadata(row.get("meta"), "gallery.meta", publication and "gallery" in active)
        for k in ["caption", "credit", "permission", "collection"]:
            text(row.get(k, ""), "gallery." + k)
        if (
            publication
            and "gallery" in active
            and not row.get("permission", "").strip()
        ):
            fail("gallery.permission", "record media permission before publication")
    records(data.get("faq"), "faq")
    for q in data["faq"]:
        text(q.get("question"), "faq.question", True)
        text(q.get("answer"), "faq.answer", True)
        references(q.get("location_ids", []), loc_ids, "faq.location_ids")
    contacts = mapping(data.get("contacts"), "contacts")
    email(contacts.get("email", ""), "contacts.email")
    text(contacts.get("phone", ""), "contacts.phone")
    text(contacts.get("response", ""), "contacts.response")
    for channel in sequence(contacts.get("channels", []), "contacts.channels"):
        text(channel.get("label"), "contacts.channels.label", True)
        email(channel.get("email", ""), "contacts.channels.email")
        text(channel.get("phone", ""), "contacts.channels.phone")
    announcement = mapping(data.get("announcement"), "announcement")
    text(announcement.get("text"), "announcement.text")
    if announcement.get("start") or announcement.get("end"):
        if instant(announcement.get("end"), "announcement.end") <= instant(
            announcement.get("start"), "announcement.start"
        ):
            fail("announcement", "end must follow start")
    policies = mapping(data.get("policies"), "policies")
    for key, value in policies.items():
        text(value, "policies." + key)
    if publication:
        pub = mapping(data.get("publication"), "publication")
        url(pub.get("domain", ""), "publication.domain", True)
        domain = urlsplit(pub["domain"])
        if domain.query or domain.fragment:
            fail(
                "publication.domain",
                "domain must not have query parameters or a fragment",
            )
        if domain.hostname in {
            "localhost",
            "example.com",
            "example.invalid",
        } or domain.hostname.endswith(".invalid"):
            fail("publication.domain", "supply the actual public domain")
        for field in ["headline", "intro", "eyebrow", "note"]:
            if re.search(
                r"\b(illustrative|demonstration|example|replace with)\b",
                brand[field],
                re.I,
            ):
                fail("brand." + field, "replace demonstration copy before publication")
        for module, rows in collections.items():
            if module in active and any(row["state"] == "demo" for row in rows):
                fail("collections." + module, "demo records cannot be published")
        if p.get("useExamples"):
            fail(
                "use_examples", "materialize and review client data before publication"
            )
        for key in ["approved", "privacy_reviewed", "contact_reviewed"]:
            if pub.get(key) is not True:
                fail("publication." + key, "explicit owner review is required")
        if not contacts.get("email") and not contacts.get("phone"):
            fail("contacts", "publication needs a public contact")
        if not policies.get("privacy"):
            fail("policies.privacy", "reviewed privacy text is required")
    return active


def load_validated(root, preset=None, publication=False):
    data, modules, config, names = read_site(root, preset)
    try:
        active = validate(data, modules, config, root, publication)
    except (TypeError, KeyError, AttributeError) as error:
        raise Invalid(
            f"restaurant: malformed record ({error}); consult docs/data-model.md"
        ) from error
    return data, modules, config, names, active
