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

## Restaurant component details

Version 2 accepts an optional `presentation` object on the following collection records. Old records remain valid without it. The renderer always takes identity, title, description, location scope, availability, dates, facts, attachments, metadata, and provider URL from the parent record. A presentation object cannot override those fields or supply its own action link.

| Collection | Component | Presentation fields |
| --- | --- | --- |
| `specials` | `component: "tasting-menu"` | `eyebrow`, `price` (display text including currency and basis), `schedule`, `courses: [{name, text}]`, `dietary_note`, `terms` |
| `specials` | `component: "beverage-flight"` | `eyebrow`, `price`, `items: [{name, portion, text}]`, `note`, `terms` |
| `team` | `team-profile` by default | `role`, `specialties: [text]`, `image`, `note` |
| `events` | `dining-space` by default | `eyebrow`, `image`, `access_note`, `terms`; capacity/arrangements remain in the record's `facts` |

Specials require the explicit `component` field when using `presentation`. Team and event records may omit it or explicitly select their default component. Unknown component/collection combinations and unknown presentation fields are rejected. Selection names must be nonempty, flight items require a serving-size `portion`, and available tasting menus/flights require at least one selection and a price. Empty selections in unavailable records render a readable pending-content fallback. These components expose a provider link and calendar action only for a current `available` parent record; paused, demo, sold-out, cancelled, unavailable, and expired records retain their copy with actions withheld.

Record images use the existing local `src`, descriptive `alt`, optional positive `width`/`height` contract and add a `permission` text field. Permission must be recorded before publishing an image on an enabled team/event page. The parent record's existing metadata review covers its component details. A field being structurally valid does not establish business or media approval.

For example, add this object to an existing Specials record (which still supplies its paired timestamps and timezone):

```json
"presentation": {
  "component": "tasting-menu",
  "price": "68 USD / person",
  "schedule": "Friday–Saturday, 6–9 pm",
  "courses": [
    {"name": "First course", "text": "Supply the reviewed dish description."},
    {"name": "Main course", "text": "Supply the reviewed dish description."}
  ],
  "dietary_note": "Supply the reviewed dietary and preparation guidance.",
  "terms": "Supply the reviewed fees, deposit, and cancellation terms."
}
```

The menu-section component groups the existing menu categories/items; no new menu fields are required. Visit steps are derived from each location's existing `access` facts, ordered as parking, entrance, seating, restroom, and sensory conditions, followed by any additional facts. They appear on Access information and location detail pages, including the mobile-kitchen access page when fixed-location routes are disabled. Preset feature switches and component layout choices remain independent of data.

Legacy `data/diner.json` was consolidated into the menu/brand model. An untouched migration reference is retained as `examples/legacy-diner.json`; it is not read by Hugo. Existing old clients require a deliberate version-2 migration before adopting these scripts.
