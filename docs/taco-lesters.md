# Taco Lester's (parody preset)

Taco Lester's is the tenth Hot Eats preset. It is a parody taco shop, in the same spirit as the Jeff Does Doors parody. Everything about the shop is invented: the crew, reviews, menu, prices, hours, and location. No real restaurant is offered. `./he preview` now opens it by default (see `site-profile.json`).

## The crew

| Character | Joke | Where they show up |
| --- | --- | --- |
| Lester | Obsessed with tacos. Remembers every one and very few customers' names. | Team page, menu note |
| Marisol | Keeps the orders and books. Closes Friday's receipts on Friday. Goes home on time. | Team page, team note |
| Tilly | A tortilla press. The final word on thickness; unavailable for comment on anything else. | Team page, home note |

## Where the files live

| Source | Responsibility |
| --- | --- |
| `profiles/taco-lesters.toml` | Name, title, and the parody notice text (`parody`, `parodyNotice`) |
| `presets/taco-lesters.toml` | Modules, home sections, and component layouts |
| `data/scenarios.json` (`taco-lesters`) | Brand copy, menu, crew, reviews, FAQ, gallery |
| `data/parody_notes.json` | The three optional character notes |
| `layouts/partials/parody-note.html` | Renders a note as a closed native disclosure, only for this preset |
| `assets/css/presets.css` | Look: masa paper, salsa red, papel-picado header stripe, tortilla-round art |
| `static/images/taco.svg`, `counter.svg`, `order-pad.svg`, `tortilla-press.svg` | Project-authored illustrations |
| `static/images/taco-icons.svg`, `data/icons.json` | The 36-icon sprite and its catalogue |
| `layouts/partials/icon.html`, `layouts/partials/icon-set.html` | Draw one icon; the review-only specimen sheet in the style guide |
| `scripts/tests/test_taco_lesters.py` | Disclosure, labelling, and note-placement checks |

## Rules that keep the joke safe

- A parody notice appears above the footer on every page when the profile sets `parody = true`.
- Crew and reviews are labelled fictional. Reviews have no source URL.
- Notes are closed disclosures with no script and no saved state. They stay out of forms, buttons, and order or contact feedback.
- Menu items carry no ingredient, allergen, or dietary claims.
- Prices, hours, and access facts are placeholders. Replace them before any real use.
- Using another profile (for example `profiles/lucyd.toml`) removes the notice. The notes follow the preset, not the profile, so they appear only with `taco-lesters`.

## Try it

```sh
./he preview
./he preview --preset diner
```

The second command shows the diner design. The parody notice still appears, because the profile is still Taco Lester's. The character notes do not appear, because they follow the preset.

## Icon set

There are 36 icons on a 24 by 24 grid with a 2 px round line. Twenty cover site functions (menu, order, visit, hours, phone, catering, events, questions, contact, access, gallery, reviews, team, search, print, specials, story, plan, info, go). Sixteen are taco-world icons (taco, salsa jar, lime, chili, tortilla press, order pad, five o'clock, inspect, corn cup, horchata, chips, beans, avocado, cilantro, flat-top, tortilla).

```gotemplate
{{ partial "icon.html" (dict "name" "taco") }}
```

- Icons use `currentColor`, so they follow the text color. Size follows the text size.
- They are hidden from assistive technology. Keep the visible text label next to every icon.
- The sprite loads over HTTP, so `./he preview` and built sites work. Opening a built file directly from disk will not show them.
- See the specimen sheet at `/site-kit/#icons` when the Taco Lester's preset is active.
- `./he test` checks that every icon reference points at a real sprite symbol.
- Placement (Taco Lester's preset only): the logo uses the taco icon instead of the star; the main menu and the More menu, the phone quick links, and the "Find what you need" cards each show an icon beside the label.
- `layouts/partials/module-icon.html` maps each page module id to an icon and renders nothing for other presets. Change the mapping there.
- Other presets keep their text-only links and the star.
