# Owner guide

Run commands from the project directory. The executable `he` provides short, voice-friendly entry points without changing your shell configuration. Nothing publishes, deploys, commits, or sends mail.

```sh
./he preview
./he check
./he today
./he menu
```

`preview` starts a loopback-only site at http://127.0.0.1:1417/. `check` reports model errors and records awaiting review. `today` and `menu` show short IDs you can reuse. Changes show a diff first; append `--apply` to save. Each saved content change creates a recovery snapshot and resets publication approval. On the master, the first saved change materializes the selected example into client data, leaving the example library intact.

```sh
./he today --announcement "Kitchen closes at 2 today" --apply
./he today --location location-1 --date 2026-10-12 --closed --apply
./he today --location location-1 --date 2026-10-13 --hours 08:00-12:00,13:00-16:00 --apply
./he today --service pickup --state paused --apply
./he menu --item item-1 --state sold-out --apply
./he menu --item item-1 --price 12.50 --apply
```

The dates and IDs above are examples. Omitting a date on a location update uses that location's current date. Service state gates connected actions; resuming a service does not connect an unavailable action or invent a provider URL.

## Bulk menu edits and recovery

```sh
./he export-menu /tmp/menu-edit.csv
./he import-menu /tmp/menu-edit.csv
./he import-menu /tmp/menu-edit.csv --apply
./he history
./he restore SNAPSHOT-ID
./he restore SNAPSHOT-ID --apply
```

CSV import updates existing IDs only and never deletes omitted dishes. Required column order: `id,name,description,price,state`. Unknown IDs, duplicate rows, invalid prices/states, and malformed columns are refused before saving. Spreadsheet formula prefixes are escaped on export and reversed on import. Add new items/categories through the structured model until an explicit addition interface is available.

Restoration restores the snapshot's effective restaurant data under the current selected preset, creates its own recovery snapshot, and resets publication approval. It does not roll back source code or silently restore a different preset. Inspect that context before applying.

If a process is killed while saving, inspect `.local/history/` and `site-profile.json` before continuing. A leftover `.local/owner.lock` is intentionally not removed automatically: confirm no owner process remains before removing it. Regular exceptions roll back a two-file content update; forced termination is a documented recovery case.

## Professional utilities

```sh
./he brief
./he brief --date 2026-10-12
./he scale 500 g --from-servings 4 --to-servings 12 --to-unit kg
./he cost examples/recipe.json --servings 24
./he log waste "Example ingredient" --quantity 0.5 --unit kg --note "End of service"
./he report --kind waste
```

The pre-service brief uses public records and labels their schedule/state. The cost tool calculates ingredient estimates with yield/waste assumptions; it excludes labor, overhead, tax and service. Scaling supports g/kg/oz/lb, ml/l/US tsp/tbsp/cup, and counts. It refuses mass-to-volume conversion without density. Review cooking method, seasoning, and actual costs yourself.

Logs support prep, stock, waste, and handoff records in `.local/operations.jsonl`. Reports sum like kinds/items/units; they are not a perpetual inventory ledger, financial accounting system, or proof of a completed provider transaction. Private staff notes must stay in `.local/` and never in public restaurant data.

## Patron brief tool

The planner supports the enabled gathering services, location, date, guest count, budget, and questions. Prepare, edit, copy, download text, or save/reopen a JSON draft. Drafts stay in files chosen by the guest; the site does not persist them automatically. When a general contact email exists, short briefs can open a mail-app draft for review. Long briefs use copy/download because mail clients impose different URL limits. No action silently sends an inquiry.
