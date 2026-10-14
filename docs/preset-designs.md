# Restaurant preset designs

Every preset selects a complete example dataset, enabled modules, homepage section order, and a layout for each of the 18 restaurant components. These choices are applied on guest pages and selected by default in the living style guide. Preset styling also changes typography, surfaces, borders, buttons, and hero composition.

| Preset | Design | Composition and component choices |
| --- | --- | --- |
| `kitchen-sink` | The full toolkit | Original cream-and-cherry composition, every module, and original component layouts as a reference. |
| `diner` | Counter classics | Bold serif heading, double rules, compact menu rows, day-tile hours, horizontal service panels, and promotion ribbons. Menu and visit details lead. |
| `cafe` | Neighborhood journal | Warm paper, restrained borders, a rectangular illustration, story before menu, horizontal dishes, split visit/contact panels, and compact hours. |
| `fine-dining` | Evening editorial | Centered italic hero, circular illustration, generous space, a single-column compact menu, split promotions and private-event packages, and stacked calendar cards. |
| `fast-casual` | Fresh & direct | Bold sans-serif headings, green-and-cream surfaces, pill buttons, a two-column dish-card menu, horizontal service panels, day-tile hours, and open FAQ cards. |
| `bar` | After hours | Dark hero, plum accents, arched illustration, horizontal dishes, split specials, stacked calendar cards, and a contact strip. |
| `bakery` | From the oven | Honey tones, soft rounded cards, italic hero, dashed menu borders, poster specials, split catering packages, day-tile hours, and open FAQ cards. |
| `food-truck` | Next stop | Bold signboard type, orange-and-cream surfaces, strong borders, schedule before menu, agenda event rows, compact service information, and a contact strip. |
| `multi-location` | Around the neighborhood | Sage and teal, clear sans-serif headings, location details before the menu, split visit panels, compact menu rows, and horizontal service panels. |
| `taco-lesters` | Salsa bar | Parody taco shop. Masa paper, salsa-red sans-serif headings, a papel-picado header stripe, a round tortilla illustration, dashed and dotted panel borders, board menu sections, and horizontal dishes. Its invented crew (Lester, Marisol, and Tilly the tortilla press), fictional reviews, and optional closed character notes are labelled as parody. See [Taco Lester’s](taco-lesters.md). |

The six showcase components follow these compositions too: diner and food-truck use compact lists; café uses a flight board, horizontal team profile, split room panel, and arrival timeline; fine dining pairs split courses and room panels; fast casual and multi-location use menu boards and planning tiles; bar uses course cards and a flight board; bakery uses menu boards and stacked profile and room features. Kitchen-sink keeps the default layouts.

A layout is also selected for components belonging to disabled modules. Enabling that module later gives it a consistent starting style; selecting a layout never enables a module by itself. Examples continue to use the existing illustrative data and shared artwork. No photography, business claims, provider destinations, or guest reviews are invented by choosing a preset.

## Preview and compare

Open `/site-kit/#presets` in the existing preview. Choose any of the ten design cards to open that design’s guide, with its palette and component layout defaults. Each selection has its own URL under `/site-kit/presets/<preset>/site-kit/`. Switching does not write to `site-profile.json`, change the client’s records, or restart the server.

- **Open full example** opens the selected restaurant. Navigation, menu filters, location details, record pages, and privacy stay within that preset’s preview.
- **Compare two designs** adds a second independent preview. The page selector lists only pages enabled in both designs and falls back to Home when a previous page is unavailable.
- **Component showcase** in the page selector opens six illustrative restaurant components using each preset’s configured layouts. It is available in every design, with a full-page link and no guide toolbar inside the preview. The component gallery below still provides all three layouts and alternate states.
- **Search** and **Privacy** are also available in the page selector. Search appears when enabled in the selected designs; Privacy is available in every preset.
- **Screen width** sets both embedded pages to an actual 1280 px desktop viewport or 390 px phone viewport, scaled to fit. On narrow screens the comparison panels stack. The full-page links provide an unscaled view.
- Scroll and follow links within either preview. **Open full page** follows that preview’s current page. Changing screen width preserves its position and inputs; **Reset previews** returns both to the selected page.
- The comparison, page, and screen width are stored in the guide URL (`compare`, `page`, and `width`), so a link reopens that comparison. No browser storage is used. Choosing a new primary design retains these choices where available.
- Without JavaScript, all ten design links and the full-example link still work. The interactive comparison controls stay hidden.

The component gallery below uses the selected design’s choices. **Preset choice** marks the selected layout; **Reset view** restores those choices. Component controls are independent of the design comparison, and neither set of controls saves changes to the preset.

To start the main restaurant preview with a particular preset, the CLI remains available:

```sh
./he preview --preset cafe
```

The guide and every preview route are generated in the same Hugo build using the existing page templates. They update with the preview server; there are no screenshot substitutes, extra preview servers, or prebuilt snapshots to maintain. Publication builds omit the entire `/site-kit/` tree.

## Change a selection

Edit `presets/<preset>.toml`. For example, these are part of the café's choices:

```toml
[params.componentLayouts]
dish-card = "horizontal"
location-card = "split"
hours-panel = "compact"
contact-panel = "split"
```

Retain the other entries in that table. Supported values are listed in [the component guide](component-library.md#layout-choices). `scripts/model.py` rejects unknown component names and unsupported layout values before a wrapper build. Missing entries fall back to `default`; calling a presentation partial directly with an unsupported layout also falls back to its original design.

`params.homeSections` sets page order. `params.designName` and `params.designDescription` describe the design in the guide. `assets/css/presets.css` owns the guest-page composition and styles scoped to `body[data-preset]`. `components.css` owns reusable component layouts. Keep typography, spacing, and colors here rather than adding presentation fields to restaurant records.

## Guest-page integration

Templates map validated restaurant records into the presentation components:

- Menu items keep their filter attributes, dietary tags, options, price including zero, state, and dish permalink.
- Provider handoffs check both the action and its service before showing a destination, and retain fallback contacts and terms.
- Location cards retain address, directions, phone, access facts, and detail links. The hours wrapper retains reviewed-schedule status, timezone, split intervals, and date exceptions.
- Specials, catering/private events, calendars/truck stops, and reviews use their corresponding presentation partials. Record metadata, attachments, expiry checks, provider links, and calendar downloads remain in the shared record wrapper.
- Menu categories additionally use the menu-section layout, independently of the individual dish-card layout. Typed Specials records select tasting-menu or beverage-flight from validated `presentation` fields; the shared record wrapper retains dates, state, location context, attachments, review metadata, and provider/calendar guards.
- Team records use team-profile; private-event records use dining-space, with capacity/access facts and terms retained. Access information and location detail pages use visit-steps derived from actual location access records, including extra access fields. Optional fields are described in [the data contract](data-model.md#restaurant-component-details). Existing feature switches continue to decide which modules each preset exposes.
- FAQs retain location context in both disclosure and open-card layouts. Contact panels keep actual contact details and response expectations.

No component choice changes the publication gates or connects a provider. The living guide remains absent from publication output.

## Component fit on desktop and phones

The six additions inherit each preset's composition as well as its palette. Diner uses double rules and compact rows; café uses open panels and quiet dividers; fine dining uses restrained widths, italic feature headings, and neutral illustration panels. Fast casual uses bold sans-serif course/flight details and rounded tiles. Bar uses plum tasting boards; bakery uses soft cards, italic headings, and dashed details. Food truck uses square signboard panels and sans-serif detail type. Multi-location uses directory typography and compact facts; kitchen-sink retains the reference card treatment.

The selected menu-section layout controls category grouping independently of the dish-card layout. Board sections arrange dishes across the available width, while compact sections stay in a single list even when individual dishes use a horizontal layout. Phone spacing is reduced around nested cards without changing content. Dish permalinks have a minimum 44 px target. Course/flight descriptions and supporting notes use bounded reading widths on desktop.

Single profile and room records fill their component grid rather than leaving a second empty column. Compact thumbnails align with the start of the copy instead of stretching with its height; larger illustration panels reduce to 170 px image height on narrow screens. Record status, dates, timezone, venue, review information, attachments, and actions remain visible, with metadata wrapping into a more compact arrangement.

The shared detail-type tokens are `--restaurant-detail-font` and `--restaurant-detail-weight` in `components.css`; preset overrides live in `presets.css`. These styles apply in the guide and guest pages. Layout values, enabled modules, record data, and action guards are unchanged by the fit refinements.

## Consistency across the remaining pages

Service handoffs (reservations, ordering, gift cards, rewards, and newsletters), catering packages, calendars/truck schedules, quotations, FAQs, contact panels, hours/location listings, generic editorial records, galleries, search, privacy, and record details use the same guest-page spacing and preset treatments. The shared heading tokens are `--restaurant-heading-font` and `--restaurant-heading-weight`; `--restaurant-panel-rule` supplies the preset's top border. Diner uses bold serif headings and double rules, café uses open dividers, fine dining uses italic headings and restrained panels, fast casual uses bold rounded surfaces, bar uses plum rules, bakery uses dashed soft cards, food truck uses square signboard borders, and multi-location uses directory typography. Kitchen-sink remains the neutral reference.

Generic editorial records use readable body text and bounded widths. Single records and single gallery images no longer leave a reserved second or third grid column. Gallery images use `object-fit: contain`, so captions/credits and the whole image stay together. Metadata remains visible and wraps with consistent spacing. Shared module headings, detail/privacy headings, section padding, example disclosures, policies, and gathering calls to action use a common rhythm on desktop and phones.

The planner uses a bounded single column before a brief is prepared, then two columns on wider screens and a stack below 850 px. Form labels are 15 px and fields 16 px, with the active preset's surfaces and borders. The prepared brief remains editable; its save/download/copy/email behavior is unchanged. Navigation links and footer links have comfortable targets, and the expanded phone menu is height-bounded and scrollable above the fixed quick actions. Search and FAQ controls retain their existing local/native behavior.

Print output normalizes preset screen surfaces across all designs to clean black text on white paper with a half-inch margin. During print, disclosure accordions expand automatically, editable textarea fields convert to full inline text, and an active scope note marks whether the full menu or filtered selection was printed. Interactive UI controls, search boxes, and action buttons are suppressed while preserving dish cards, headings, and page flow without awkward page splits.

## Focused verification

```sh
python3 -m unittest discover -s scripts/tests -p 'test_preset*.py'
python3 -m unittest discover -s scripts/tests -p 'test_component_library.py'
node --check assets/js/style-guide.js
```

The preset test uses one temporary synthetic site with all modules enabled and alternate layouts. It checks preflight validation, rendered selections, zero-priced and sold-out dishes, service pauses and fallbacks, expired events and download hooks, hours, contact details, FAQ context, and guide defaults. The component test covers all 108 guide layout/state combinations. The switcher test also checks all nine scoped examples, subpath navigation, unchanged owner records, and omission from a local synthetic publication build. The broader copy and recovery suite remains owner-run through `./he test`.
