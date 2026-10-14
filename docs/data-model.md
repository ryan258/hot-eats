# Public restaurant data contract

The authoritative validator is `scripts/model.py`. Run `./he check` for schema errors and content-review statuses. Python 3.11+ is required for TOML parsing. No third-party Python package is required.

Both client and example records use `schema_version: 2`:

| Field | Responsibility |
| --- | --- |
| `meta` | `status` (`demo`, `draft`, `approved`, `stale`), `reviewed_on` (YYYY-MM-DD), and source/review evidence |
| `brand` | Headline, intro, eyebrow, tagline, note, image, story title/paragraphs, decorative ticker |
| `announcement` | Text plus optional paired ISO start/end timestamps with explicit offsets |
| `locations` | Unique ID, name, address, phone, HTTPS map URL, IANA timezone, weekly hours, date exceptions, access facts, metadata |
| `services` | Stable service ID, label, state, supported location IDs |
| `actions` | Module/service/location association, state, HTTPS provider URL, name, note, terms, fallback email/phone, metadata |
| `menu` | Currency, review date, menu/allergen notes, categories and uniquely identified items |
| `collections` | Module-keyed editorial, catering, event, review, job, sourcing, and press records |
| `faq` | Stable ID, question, answer, location scope |
| `gallery` | Unique ID, local image path, alt text, caption, collection, credit, permission notes, metadata |
| `contacts` | General email/phone/response expectation and labeled contact channels |
| `policies` | Reviewed privacy and service-specific text |
| `publication` | Actual HTTPS domain and explicit owner approval, privacy review, and contact review flags |

Item prices are nonnegative decimal strings (including `"0"`) or empty strings. IDs use lowercase letters, numbers, and single hyphens. Empty item location/service lists mean all. Empty service location lists mean all locations; a provider action must reference a location supported by its service. `available`, `sold-out`, and `unavailable` are the menu-item states. Dietary text is supplied and reviewed by the restaurant; it is never inferred from ingredient names.

Weekly hours use `day: 0` for Monday through `day: 6` for Sunday, and `intervals: [["08:00", "15:00"]]`. Empty intervals mean closed; a missing day means unknown. Date exceptions use `date`, `intervals`, and `note`. Split overnight hours into two days; `24:00` is allowed only as an interval end. Duplicate days/dates, inverted intervals, and overlapping periods are rejected. The browser computes current status only for approved schedules, in the location's timezone. Printed schedules remain available without JavaScript. Rebuild when schedules change.

Collection records contain `id`, `title`, `text`, `state`, `location_ids`, `facts` (label/value pairs), `url`, `attachments` (local static-file path/label), and `meta`. Add `attribution` for reviews. Calendar, specials, and food-truck records also require offset-aware `start` and `end`, an IANA `timezone`, and can include `venue`. Other dated records use the same paired timestamp contract. Source dates determine display order; past entries remain visible as expired, with transactional actions removed. The browser refreshes current hours and expiry on load, once a minute, and when a tab becomes visible again. Static output must be rebuilt when source changes and for future announcements to appear; this is not a scheduled backend.

Use facts for package sizes, prices, minimums, service area, lead times, capacities, compensation, employment type, application deadline, roles, credits, and terms. Use record detail pages for longer text. A job application or ticket destination belongs in `url`; it remains external. Press files belong in `static/` and require explicit permission. Review records need source URLs and attribution before publication.

Images may live under `assets/` (responsive processing when supported) or `static/` (served directly). SVG resources are not raster-resized. Use accurate alt text and image dimensions; the default fallback size is not evidence of a real image's aspect ratio.

Legacy `data/diner.json` was consolidated into the menu/brand model. An untouched migration reference is retained as `examples/legacy-diner.json`; it is not read by Hugo. Existing old clients require a deliberate version-2 migration before adopting these scripts.
