# Hot Eats remediation and enhancement register

Updated October 3, 2026. This is the implementation handoff for the project review and the request to fix the findings and take the next steps.

**Status: implementation written; runtime verification pending.** At Ryan's request, the agent did not run tests, Hugo builds, browser checks, or GitNexus analysis for this revision. Source inspection and formatting are not passing test evidence. The single owner-run command is `./he test`; the acceptance scope is in [verification.md](verification.md).

## Where the project now stands

The project is a local-first restaurant website library with 24 selectable page modules and nine illustrative restaurant presets. It combines a static public site, an editable versioned restaurant model, a short owner CLI, and independent client-copy tooling. Hugo renders the public site; Python handles local validation, changes, copying, and fresh artifacts; browser JavaScript adds filters, calendar exports, and a private gathering brief.

The implementation now gives the same location, service, menu, and content records to public pages and owner tools. Example and client data are separate. Provider actions have explicit availability and fallback contacts. Publication has a separate local build gate. These are useful foundations for the kitchen-sink exemplar, but they do not turn illustrative records into real business facts or establish that an outside provider completed a transaction.

The active working folder did not expose `.git` or `.gitnexus` to this session. No Git history or fresh graph analysis is claimed. No staging, commit, push, deployment, external messages, provider transactions, or shared-factory edits were performed.

## Corrections from the review

Every correction below has a local implementation. Each remains **awaiting verification** until the owner-run command and relevant browser journey pass.

| ID | Finding | Implemented correction | Evidence to obtain |
| --- | --- | --- | --- |
| C01 | The search prompt suggested “hours,” but search could return nothing. | Shared search vocabulary includes guest synonyms and restaurant content; directory and JSON search output use the same helper. | Search index contract plus browser searches for hours, parking, allergies, and a dish. |
| C02 | Unicode names, particularly emoji, could become invalid TOML surrogate escapes. | Client identity and resolved configuration use Unicode-preserving serialization. | Unicode/quoted-name client parsing and Hugo build. |
| C03 | An SVG under `assets/` could reach raster-only image methods. | Image metadata and processing capability guards; static/SVG fallback with explicit dimensions. | SVG-in-assets build fixture, then visual inspection. |
| C04 | A copy failure after destination creation could leave an unusable destination that blocked retry. | Stage transformations and validation first; reserve an absent destination; roll back an ordinary partial move failure. | Staged-failure and partial-finalization regressions; existing-destination sentinel preservation. Forced termination remains a documented recovery case. |
| C05 | Templates carried diner-specific brand/content assumptions. | Brand, menu, schedules, content, and service selection come from the chosen dataset; nine illustrative datasets; neutralized client contacts/connections/approval. | Preset matrix, client copy, and editorial inspection. Artwork is still shared illustrative concept artwork, not nine finished visual identities. |
| C06 | The food-truck preset inherited a fixed-location visit section. | Explicit home sections, schedule-led truck homepage, and disabled fixed visit block. | Preset configuration and generated-page regression. |
| C07 | The planner depended on events and failed for catering-only configurations. | Any-of dependencies: catering or private events enables the planner; only enabled gathering services appear. | Catering-only and neither-service regressions, plus client build. |
| C08 | Verification assumed the original dish count and default selection. | Verification derives routes from active modules, validates the current selection, builds all example presets, and edits a copied menu. | Owner-run verification with changed dish count, zero price, and client configuration. |
| C09 | Malformed data, references, and module dependencies reached templates unchecked. | Schema version 2 preflight validates types, IDs, references, URLs, money strings, media confinement, timezones, schedules, dates, and dependency cycles. | Positive/negative contract fixtures. Plain Hugo remains an engine entry point without Python preflight. |
| C10 | Flipping release flags did not consistently remove preview UI, guide pages, or indexing restrictions. | Named demo/preview/publication lifecycle; publication preflight; publication-only canonical/schema/social metadata and sitemap; operator guide absent from publication output. | Synthetic publication build and artifact review; actual host headers remain unverified. |
| C11 | Standalone menu headings skipped from h1 to h3. | Context-specific category/item heading levels on the home and standalone menus. | Menu heading-sequence assertion and assistive-technology review. |
| C12 | Existing `public/` files could survive a changed module selection. | Supported builds reserve a new destination outside source; refuse existing destinations; record source/data/output hashes; refuse a success manifest if source changed during the build. | Fresh build and route matrix, overwrite refusal, manifest regression. Old `public/` was preserved and is not current output. |

## Implemented enhancement workstreams

| Workstream | Local implementation | Remaining acceptance or extension |
| --- | --- | --- |
| Shared restaurant model | Stable location/service/item/record IDs, metadata, schedules, exceptions, provider actions, contact/policy fields, versioned validation. | A real restaurant's records and evidence; deliberate migrations for older clients. |
| Owner ergonomics | `he` entrypoint; short today/menu commands; diff-before-save; per-change snapshots; restore; no-op handling; approval reset after changes. | Use with Ryan's actual aliases, dictation, and preferred input workflow; no shell profile was changed. |
| Bulk menu management | CSV export/import with formula-prefix escaping, stable IDs, exact columns, validation, and snapshot recovery. | New-item creation remains a structured-data edit; arbitrary spreadsheet layouts are not imported. |
| Menu usefulness | Text/category/location/service filtering, stable dish links, clear availability, zero-price support, currency and review date, full/filtered print controls. | Browser and print acceptance; restaurant-reviewed option and dietary text. No automatic allergen inference. |
| Location continuity | Location detail pages, context carried across guest paths, location-specific actions and FAQ/record scope. | Actual addresses, maps, phone numbers, access facts, and service assignments. |
| Hours and urgent changes | Split hours, special dates, unknown/closed distinction, approved-data current status, periodic refresh, owner exception command. | Real schedules and timezone review; source changes still require a build. |
| Provider handoffs | Explicit action and service states; HTTPS links; alternative contact paths; paused-service suppression; available service choices. | Actual booking/order/rewards/gift-card/newsletter providers and authorized acceptance of each destination. |
| Gathering planner | Catering/events selection; location/date/guest/budget prompts; editable brief; copy/text export; validated local draft import/export; optional mail-app draft. | Browser downloads/clipboard/mail-app behavior. Nothing is silently sent or booked. |
| Dated content | Structured specials, calendar entries, truck stops, stable details, expiry states, namespaced calendar exports. | Real dates and venues; recurring events and automatic remote rebuild scheduling are not implemented. |
| Editorial depth | Structured facts, text, attachments, source/review metadata, and detail pages for the record-based modules. | The authoring structure is implemented; restaurant-specific stories, people, sourcing, compensation, permissions, and photos remain content work. |
| Search and navigation | Guest-task groups, direct common tasks, shared search terms/content, keyboard-close behavior, mobile quick actions. | Narrow-screen, zoom, keyboard, and assistive-technology acceptance. |
| Accessibility | Semantic menu headings, labels/status messages, native FAQ/details, focus treatment, large controls, readable fallbacks, location access facts. | Automated checks do not establish conformance. Actual guest journeys and physical access facts require acceptance. |
| Professional utilities | Pre-service brief; compatible-unit recipe scaling; yield/waste ingredient-cost estimates; private prep/stock/waste/handoff log and totals. | These are local arithmetic and records. POS reconciliation, food-safety management, payroll, accounting, and inventory depletion are separate systems. |
| Content provenance | Demo/draft/approved/stale metadata, sources/dates, publication review flags, copy resets, source/data/output manifests. | Review status is supplied by the owner; a validator cannot determine truth or permission. |
| Recovery and independence | Staged copying, frozen shared helper, provenance receipt, no overwrite, private-state exclusion, local change snapshots. | Forced-kill recovery and client upgrades need the documented procedure; no automatic remote updater. |
| Documentation | Rewritten quick start, architecture, data contract, owner guide, module registry reference, copy/publication runbooks, and verification scope. | Update these alongside model/renderer changes; don't carry historical passing results forward. |

## Coverage of the 24 modules

| Module(s) | Exemplar capability | Business-specific completion |
| --- | --- | --- |
| Menu | Structured categories/items, filtering, links, printing. | Approved menu, prices, options, dietary wording, currency. |
| Specials | Dated, location-scoped records and expiry. | Actual offers, eligibility, prices, terms. |
| Locations | Hours, exceptions, access, contact/map paths, detail pages. | Physical facts and current schedules. |
| Reservations, ordering | Location/service provider actions and availability. | Connected, accepted booking/order destinations. |
| Catering, events | Packages/capacity/terms as facts and detail pages; planner entry. | Actual service areas, lead times, capacities, minimums, deposits. |
| Planner | Local reusable gathering brief. | Actual contact or an explicitly chosen intake service. |
| Gallery | Local media, alt text, dimensions, captions, credits, permission records. | Finished restaurant media; collection labels are recorded, but a gallery collection filter/lightbox is not implemented. |
| Story, team, sourcing | Structured editorial records with stable detail routes. | Real origin, permissioned people/portraits, verified suppliers and sourcing claims. |
| Reviews | Source URL and attribution required for publication. | Real permissioned/source-linked reviews. Empty by default; no invented endorsements. |
| Gift cards, loyalty, newsletter | Clearly available/unavailable provider handoffs and terms. | Provider setup, eligibility, redemption, consent, support, privacy. |
| News, calendar | Detail records and dated calendar downloads. | Actual editorial updates and events. |
| Careers | Role/compensation/terms as structured facts; external application URL. | Actual opening and application process. Empty by default; no invented vacancies. |
| FAQ, contact | Native questions, location scope, labeled contact channels. | Owner-reviewed answers and monitored public contacts. |
| Accessibility | Location access facts and an editorial module. | Verified entrance, seating, restroom, parking, sensory and communication information. |
| Press | Facts, credits, and downloadable static attachments. | Permissioned photos/logos, approved fact sheet, monitored press contact. |
| Food truck | Schedule-first homepage, dated stops, locations/venue, expiry. | Real stops, weather/cancellation procedures, pickup service details. |

## Remaining opportunities and concrete solution proposals

These are enhancement options, not completed features or hidden release requirements. Prefer the smallest improvement that reduces the owner's or guest's effort.

| Priority | Opportunity | Proposed solution and completion evidence |
| --- | --- | --- |
| Next | Establish this revision's runtime evidence. | Run `./he test`, fix reported failures, then exercise the focused browser journeys in the verification guide. Record tool versions and results against this source. |
| Next | Replace scaffold prose with an exceptional reference restaurant. | Author one coherent, explicitly fictional kitchen-sink content pack with a consistent menu, service story, media direction, and illustrative operational scenarios; retain conspicuous demo status. Keep real client packs independently approved. |
| Next | Make everyday editing still easier. | Add a loopback-only editor on top of the same validator and snapshot transaction, with large controls, keyboard/dictation-friendly fields, simple today actions, diff/undo, and no account requirement. Do not duplicate business rules in the UI. |
| Next | Strengthen browser regression coverage. | Add an optional pinned browser harness for menu/context flows, draft round trips, expiry, keyboard navigation, responsive overflow, and print/download contents; run it through an owner-invoked command. Retain manual assistive-technology acceptance. |
| Soon | Support menu additions without JSON editing. | Extend the CLI/editor with add/archive item/category commands, explicit IDs, dry-run diffs, and snapshots. Preserve old dish URLs with archive explanations or redirects. |
| Soon | Improve media and gallery depth. | Add collection filtering, original-image links, team portraits, configurable aspect ratios, and a per-asset rights register. Produce preset-specific artwork only as explicitly labeled concepts or use permissioned real photos. |
| Soon | Add a shareable printed menu and visit sheet. | Build a dedicated print layout from the same data with identity, date, selected location, currency, availability and access contacts. Test common paper sizes and long menus; don't maintain duplicate PDFs by hand. |
| Soon | Improve discoverability metadata. | Add optional structured postal-address, coordinates, cuisine, social-image, and per-record metadata fields with validation. Validate the resulting structured data independently; do not promise a search-result treatment. |
| Soon | Expand professional arithmetic. | Add reusable recipes/ingredient units, cost assumptions, versioned estimates, explicit rounding, batch scaling, and CSV reports. Integrate a real inventory/POS system only through a reviewed import/export contract. |
| Optional | Multilingual guest content. | Use Hugo language content keyed by stable IDs, translation completeness checks, explicit fallback text, and preservation of location/service context. Decide which languages are actually needed first. |
| Optional | Recurring events and timely updates. | Represent recurrence separately from generated dated occurrences, with timezone-aware expansion and overrides; add an explicitly authorized rebuild schedule and failure reporting. No schedule was created here. |
| Optional | Hosted editing or CMS. | Keep the public schema/validation pipeline; choose a CMS only if local editing no longer meets the owner's needs. Add permissions, review previews, revisions, and export/restore before allowing hosted edits. |
| Optional | Real inquiry intake. | Choose an actual destination and define consent, data minimization, retention, validation, spam controls, delivery receipts, retry/failure handling, and an accessible fallback. A mail-app draft remains useful until this is warranted. |
| Optional | Provider integrations beyond links. | Define credentials outside public data, exact location/service mapping, idempotency, observable confirmation and outage behavior. Use hosted checkout or specialist providers where appropriate; never infer completion from clicks. |
| Optional | Deployment and rollback automation. | After a host is chosen and publication is explicitly delegated, upload only the accepted fresh artifact, verify headers/domain/routes, retain the previous artifact, and document rollback. No host setup or deployment was performed. |
| Optional | Client upgrade tooling. | Add schema migration commands with dry-run diffs, source version identifiers, fixture-based compatibility checks, and backups. Preserve custom client data and template changes instead of overwriting a whole copy. |

## Next action

Run this once from the project directory and report the concise result or failure output:

```sh
./he test
```

After that evidence is available, address its failures before broadening the feature set. Real business publication remains a separate owner-controlled decision.
