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

The six showcase components follow these compositions too: diner and food-truck use compact lists; café uses a flight board, horizontal team profile, split room panel, and arrival timeline; fine dining pairs split courses and room panels; fast casual and multi-location use menu boards and planning tiles; bar uses course cards and a flight board; bakery uses menu boards and stacked profile and room features. Kitchen-sink keeps the default layouts.

A layout is also selected for components belonging to disabled modules. Enabling that module later gives it a consistent starting style; selecting a layout never enables a module by itself. Examples continue to use the existing illustrative data and shared artwork. No photography, business claims, provider destinations, or guest reviews are invented by choosing a preset.

## Preview and compare

Open `/site-kit/#presets` in the existing preview. Choose any of the nine design cards to open that design’s guide, with its palette and component layout defaults. Each selection has its own URL under `/site-kit/presets/<preset>/site-kit/`. Switching does not write to `site-profile.json`, change the client’s records, or restart the server.

- **Open full example** opens the selected restaurant. Navigation, menu filters, location details, record pages, and privacy stay within that preset’s preview.
- **Compare two designs** adds a second independent preview. The page selector lists only pages enabled in both designs and falls back to Home when a previous page is unavailable.
- **Component showcase** in the page selector opens six illustrative restaurant components using each preset’s configured layouts. It is available in every design, with a full-page link and no guide toolbar inside the preview. The component gallery below still provides all three layouts and alternate states.
- **Screen width** sets both embedded pages to an actual 1280 px desktop viewport or 390 px phone viewport, scaled to fit. On narrow screens the comparison panels stack. The full-page links provide an unscaled view.
- Scroll and follow links within either preview. **Open full page** follows that preview’s current page. Changing screen width preserves its position and inputs; **Reset previews** returns both to the selected page.
- The comparison, page, and screen width are stored in the guide URL (`compare`, `page`, and `width`), so a link reopens that comparison. No browser storage is used. Choosing a new primary design retains these choices where available.
- Without JavaScript, all nine design links and the full-example link still work. The interactive comparison controls stay hidden.

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
- FAQs retain location context in both disclosure and open-card layouts. Contact panels keep actual contact details and response expectations.

No component choice changes the publication gates or connects a provider. The living guide remains absent from publication output.

## Focused verification

```sh
python3 -m unittest discover -s scripts/tests -p 'test_preset*.py'
python3 -m unittest discover -s scripts/tests -p 'test_component_library.py'
node --check assets/js/style-guide.js
```

The preset test uses one temporary synthetic site with all modules enabled and alternate layouts. It checks preflight validation, rendered selections, zero-priced and sold-out dishes, service pauses and fallbacks, expired events and download hooks, hours, contact details, FAQ context, and guide defaults. The component test covers all 108 guide layout/state combinations. The switcher test also checks all nine scoped examples, subpath navigation, unchanged owner records, and omission from a local synthetic publication build. The broader copy and recovery suite remains owner-run through `./he test`.
