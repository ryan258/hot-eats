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
