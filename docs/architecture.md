# Architecture and maintenance

Hot Eats is a static Hugo restaurant library. Python 3.11+ resolves the selected configuration, validates public data, manages local edits and copying, and creates fresh build artifacts. Browser JavaScript progressively enhances rendered HTML; there is no application server, checkout, reservation engine, analytics collector, or implicit email delivery.

## Sources and output

- `hugo.toml` supplies engine defaults. The selected profile layers identity over them; the selected preset layers service/module selection and presentation after that. `site-profile.json` selects both and controls `use_examples` for the wrapper.
- `data/modules.json` owns module IDs, titles, labels, search terms, groups, renderer kinds, all-of dependencies, and any-of dependencies. `scripts/model.py` rejects unknown references and cycles.
- `data/scenarios.json` contains nine complete illustrative datasets. `data/restaurant.json` is the editable client model. `site-data.html` selects the same source as Python. Owner changes materialize the selected example into the client model and set `use_examples` false.
- `content/_content.gotmpl` and `generate-restaurant-pages.html` generate enabled module, record-detail, location-detail, search, and guide pages. In preview mode they also generate the nine complete examples under `/site-kit/presets/<preset>/`. The `previewpreset` page parameter scopes `site-config.html`, `site-data.html`, feature checks, component choices, and `site-url.html` to that example. Static assets stay shared. The `presets/` directory is mounted as Hugo data for live reload and read by `preset-library.html`; no second registry or mutable global state is used. Disabled modules have no generated route. Publication omits the entire guide and preview tree.
- `layouts/partials/modules/` contains focused renderers. `shared/` contains record, location-schedule, metadata, and search helpers. Brand prose lives in the data model, not the templates.
- `presets/*.toml` selects all 18 component layouts and homepage section order. `component-layout.html` resolves those choices and `assets/css/presets.css` adds scoped visual treatments; `scripts/model.py` validates the configuration. See `docs/preset-designs.md`.
- `layouts/partials/components/` contains reusable presentation components. `data/component_library.json` supplies illustrative fixtures for the `/site-kit/` living style guide; it remains separate from client data. Optional public record `presentation` fields are validated by `scripts/model.py` and mapped by `shared/record-card.html`; no style-guide fixtures are used on guest pages. See `docs/component-library.md` for contracts and integration.
- `site.py` checks selected data before Hugo, creates a transient mode configuration, and writes fresh output outside the source with a sibling provenance manifest. A manifest records source/data hashes and mode; it is not proof of real-provider behavior or deployment.
- Guest menu sections wrap `menu-dishes.html`, retaining dish-card choices and filtering/print hooks. Typed Specials records use tasting-menu or beverage-flight components; team and events use team-profile and dining-space components. `visit-planning.html` derives ordered steps from location access facts on location detail and accessibility pages. New record provider/calendar actions require explicit current availability. The same adapters serve the main restaurant and all preset previews.
- The browser maintains selected location/service in URL parameters, not persistent storage. Menu filtering, searchable task cards, calendar export, and editable gathering drafts are local enhancements.
- `.local/` contains owner snapshots, a concurrency lock, and optional private operational logs. Hugo does not mount it. Sculpting does not copy it.

## Copy boundaries

The master imports the sibling factory's `scaffold_core.py`; a generated client includes its exact frozen copy and hash receipt. The restaurant adapter validates source data, copies to an owned staging area, transforms identity and content, validates again, then reserves a previously absent destination. Copying never overwrites an existing destination. On an ordinary finalization failure the adapter removes only the destination it reserved; interruption by forced process termination may require inspecting and removing an incomplete destination before retrying.

Do not edit a destination while it is being created. Shared factory ownership remains in the sibling project; no changes to that project are needed for the restaurant adapter.

## Changing the model

The public schema is version 2 and validated by `scripts/model.py`. Add fields there before consuming them in templates or owner commands. Keep private fields in `.local/`, not `data/`. Maintain template output allowlists; never serialize the whole restaurant model into browser JavaScript. Supported renderer kinds are explicit, not inferred from a file path supplied by data.

When adding a module, add its registry record and an explicit feature value to each preset and engine defaults. Add a focused fixture to verification. A catering or private-events module can independently enable the planner through `requires_any`.

## Upgrade a client

Record the source version and copy receipt. Compare engine/template changes in a separate copy, preserve the client data/profile, migrate schema deliberately, and run the verification command. Do not replace a customized client's whole directory. This project has no automatic remote updater.
