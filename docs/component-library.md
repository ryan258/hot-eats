# Restaurant components and living style guide

Open `/site-kit/` with `./he preview`. The guide contains foundations, 18 reusable restaurant components in 54 layouts, their alternate states and input data, all 24 existing page-module contracts, and the operator commands. It is omitted from publication builds. Guide search, category filters, layout selectors, comparison controls, four palette previews, a narrow preview, and copy buttons run locally; they do not save preferences or submit information.

## Preview restaurant designs

Use the ten design cards at `/site-kit/#presets` to switch the guide and its component defaults. Compare two real restaurant pages at desktop or phone widths, select a shared page, and open either at full size. Comparison choices are kept in the URL; switching does not change the saved restaurant configuration. See [preset designs](preset-designs.md#preview-and-compare) for controls and routing. Choose **Component showcase** in the page selector to compare the six new components across any two presets, including presets where the related guest module is disabled. Each showcase uses the shared illustrative fixtures and the preset’s actual layout choices, at `/site-kit/presets/<preset>/component-showcase/`. The main preview also has `/component-showcase/`. These pages and the guide are omitted from publication builds.

## Source and integration

- `layouts/partials/components/` owns the reusable markup. `heading.html`, `link.html`, and `layout.html` are internal helpers.
- `presets/*.toml` selects the guest-page layouts through `params.componentLayouts`. `layouts/partials/component-layout.html` resolves them; `assets/css/presets.css` adds preset composition and styling.
- `assets/css/components.css` is bundled with the site stylesheet so these partials work outside the guide and in independent restaurant copies.
- `data/component_library.json` contains the guide registry and **illustrative fixtures only**. It is not client restaurant data and is not included in the guest search index.
- `layouts/_default/site-kit.html`, `assets/css/style-guide.css`, and `assets/js/style-guide.js` own the guide. Its CSS and JavaScript load only on that page.

Call a partial with an explicit `data` object and the appropriate heading level:

```go-html-template
{{ partial "components/dish-card.html" (dict "data" .Params.featuredDish "level" 2 "layout" "horizontal") }}
```

The living guide shows a copyable template call for each layout and exact JSON data for each component’s first example. `layout` is a presentation argument, separate from the content and its availability state. Omitting it, passing `default`, or passing an unsupported value uses the original layout. Pass that object's fields to `data`; replace illustrative content before use. `level` accepts 2–6 and defaults to 3. The quotation has no heading. FAQ answer cards use the next heading level, capped at 6. The presentation partials create no element IDs by default, so multiple instances can coexist without collisions. The guest FAQ adapter explicitly enables `locationAware` to attach validated FAQ IDs and location filters. The optional `headingURL` argument links a component heading to its record detail page. Links use `{ "url": "/menu/", "label": "Explore the menu" }`; local routes respect Hugo's configured base path, and fragment links remain on the current page.

These are presentation components. Version-2 restaurant records now support optional validated `presentation` fields for tasting menus, beverage flights, team profiles, and dining spaces; see [the data contract](data-model.md#restaurant-component-details). The guest renderers already use these components for announcements, menus, service handoffs, visits/hours, specials, gatherings, calendars/truck stops, reviews, FAQs, and contact details. For further integration, map existing validated fields to the component input or extend `scripts/model.py` before adding new restaurant data fields. Guest menu-section calls pass template-rendered `menu-dishes.html` markup through the partial’s internal `content` argument; restaurant data cannot provide this argument. The optional internal `category` argument retains category IDs and filter hooks. Validate real provider destinations and feature availability through the existing model/action flow; do not bypass it with guide fixtures. Preview controls only change the guide examples. A narrow component preview is not a substitute for testing a whole page on a device.

## Components

| Partial | Purpose | Supported states and behavior |
| --- | --- | --- |
| `notice.html` | Service announcements | Information or warning; static content without an assertive live region |
| `dish-card.html` | Featured menu item | Available, sold out, unavailable; optional image, tags, price and modifiers |
| `dietary-key.html` | Explain menu labels | Plain-language labels, preparation note and optional contact link |
| `service-card.html` | Pickup, delivery or reservation handoff | Available requires a labeled URL; paused/missing configuration shows a fallback |
| `location-card.html` | Address and access facts | Confirmed content or address-pending fallback |
| `hours-panel.html` | Static hours and exceptions | Split service, closures, timezone and missing-schedule fallback |
| `offer-card.html` | Special or recurring offer | Available, sold out, unavailable; schedule, pricing basis and terms |
| `package-card.html` | Catering or private dining | Inclusions, price basis, minimum, lead time and inquiry link |
| `event-card.html` | Event summary | Available, sold out, cancelled, unavailable and automatic past-event state |
| `quote-card.html` | Attributed guest quotation | Quote, attribution, context and optional original-source link |
| `faq-list.html` | Guest questions | Native keyboard disclosures, multiple open answers, empty fallback |
| `contact-panel.html` | Contact and response expectation | Telephone/email app links or missing-details fallback |
| `menu-section.html` | A group of dishes | Prices, dietary labels, sold-out/unavailable item labels and missing-menu fallback |
| `tasting-menu.html` | Ordered courses | Price basis, service schedule, dietary arrangements and booking terms; action requires available state |
| `beverage-flight.html` | Drink selections | Serving sizes, tasting notes, caffeine/alcohol information and terms; action requires available state |
| `team-profile.html` | Chef, baker, barista or host | Optional image and areas of focus; biography-pending fallback |
| `dining-space.html` | Private room or patio | Capacity by arrangement, access conditions, planning terms and inquiry link; missing-details fallback |
| `visit-steps.html` | Plan and arrive | Native ordered instructions, optional step links and missing-guidance fallback |

The hours panel does not calculate “open now.” The existing `shared/hours.html` remains the location-aware component for approved live schedule status. Event timestamps must be valid ISO timestamps with UTC offsets; past-event evaluation happens at build time, so a static deployment needs rebuilding after time-dependent changes. These partials do not process orders, bookings, payments, or inquiry submissions.

## Layout choices

Each component has three layouts. The guide renders all 108 layout/state combinations.

| Component | `default` | Second layout | Third layout |
| --- | --- | --- | --- |
| Service notice | Inset notice | `banner`: Wide banner | `centered`: Centered announcement |
| Featured dish | Photo card | `horizontal`: Image beside copy | `compact`: Compact menu row |
| Dietary key | Stacked glossary | `grid`: Label tiles | `inline`: Inline definitions |
| Service handoff | Service card | `horizontal`: Service panel | `compact`: Compact service row |
| Visit card | Location card | `split`: Split visit panel | `compact`: Location directory row |
| Hours & exceptions | Schedule list | `board`: Day tiles | `compact`: Compact hours strip |
| Special & promotion | Specials poster | `split`: Split promotion | `ribbon`: Promotion ribbon |
| Catering package | Package card | `split`: Package comparison panel | `compact`: Compact package row |
| Event listing | Date beside copy | `stacked`: Date-band card | `row`: Agenda row |
| Guest quotation | Editorial quotation | `centered`: Centered feature | `compact`: Compact pull quote |
| Questions & answers | Accordion list | `split`: Split FAQ panel | `cards`: Open answer cards |
| Contact & response | Contact card | `split`: Split contact panel | `bar`: Contact strip |
| Menu section | Menu list | `board`: Menu board | `compact`: Counter menu |
| Tasting menu | Course sequence | `split`: Invitation and courses | `cards`: Course cards |
| Beverage flight | Tasting notes | `board`: Flight board | `compact`: Drinks list |
| Team profile | Profile card | `horizontal`: Portrait beside profile | `compact`: Team directory row |
| Private dining space | Room feature | `split`: Room and arrangements | `compact`: Venue directory row |
| Visit planning steps | Numbered steps | `timeline`: Arrival timeline | `tiles`: Planning tiles |

Layouts retain the same facts and action availability. Compact layouts reduce spacing and rearrange content; they retain dietary notes, modifiers, terms, access facts, and response expectations. Wide layouts wrap to fit their container, and grids collapse when needed. No variant requires guide JavaScript to select its layout: the partial’s `layout` argument and the shared component stylesheet provide it.

Use the per-component selector to try one layout or toggle **Compare all layouts** to show its three options. Palette and width previews apply to every variant. Each layout has a linkable heading, such as `/site-kit/#layout-dish-card-horizontal`. Opening that link reveals the component and selects its layout even if filters hid it. Every layout includes the existing alternate content states and its own **Use this layout** snippet. **Reset view** restores the active preset’s layouts and clears comparison mode. Each selector labels that choice as **Preset choice**. See [preset designs](preset-designs.md) for the nine compositions and their configuration.

The six additions also render on guest pages. Menu categories use menu sections around the existing dish cards, preserving all dish filters, context, modifiers, prices, and permalinks. Typed Specials records use tasting menus or beverage flights; team and private-event records use profiles and dining spaces. Access information and location detail pages derive visit steps from each location’s access facts. The same adapters serve all nine presets, with enabled modules determining which routes exist and the preset’s component choices determining their layouts. Explicit partial calls remain available for independent reuse. New team and room SVGs are labeled illustrations, not staff portraits or venue photographs. Menu item states other than `available` render unavailable labels (`sold-out` has its own label). Tasting-menu and beverage-flight links require an explicit `state=available`; an omitted or unrecognized state remains unavailable. Visit steps use an ordered list with no input or saved progress.

## Design and accessibility

Components inherit `--paper`, `--red` (the active accent), `--ink`, `--muted`, `--line`, `--pink`, and `--green`. They introduce `--restaurant-surface`, `--restaurant-radius`, and `--restaurant-space`. Layout classes are prefixed `restaurant-`; guide-only classes are prefixed `sg-`. New styles do not replace existing module selectors.

Use plain-language state labels alongside visual treatments. Keep prices and availability next to the relevant dish or service. Use specific access facts and confirmed dietary guidance. Meaningful artwork needs descriptive alt text. Action links, native disclosures, visible focus, text wrapping, reduced motion inherited from the site, and forced-colors rules are included; real assistive-technology acceptance still requires human checking.

Without JavaScript, all 54 layouts and their native state disclosures remain available. Inert guide controls stay hidden. Copy failures select the code and report the fallback. Following a component or layout anchor reveals it if filtering or layout selection had hidden it.

## Maintaining the guide

Add a focused partial and its styles, then a registry entry, `layouts` list, and examples in `data/component_library.json`. Keep the partial’s layout allowlist, `scripts/model.py` configuration allowlist, and registry in sync. The guide renders every layout/state combination without duplicating fixture data or component markup. Include useful unavailable or missing-content states. Do not add fictional claims to client records. All source files are retained by the existing sculpting workflow; publication excludes the guide route, assets unique to that route, and fixture content from rendered output.

Targeted rendered checks:

```sh
python3 -m unittest discover -s scripts/tests -p 'test_component_library.py'
node --check assets/js/style-guide.js
```

The full preset, copy, publication, and recovery suite remains an owner-run command: `./he test`.
