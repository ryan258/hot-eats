# Verification evidence and owner handoff

## October 13 remaining-page consistency pass

The remaining restaurant pages were reviewed across all nine presets: service handoffs (ordering/reservations/gift cards/rewards/newsletters), catering, calendars/truck schedules, quotations, FAQs, contact, hours/location listings, editorial records (story/sourcing/news/careers/press), galleries, search, privacy, and record details. A route manifest derived from the current preset feature switches and illustrative data contained 258 guest pages: kitchen-sink 42, diner 29, café 26, fine dining 32, fast casual 24, bar 25, bakery 27, food truck 23, and multi-location 30. Guides and component-showcase routes were excluded from that count.

The pass changed preset styles and the comparison catalog, plus documentation. It added shared heading/panel tokens, consistent module/detail spacing, readable editorial cards, preset styling for the remaining components, wrapped metadata, better single-record composition, whole-image gallery frames, larger form labels, a single-column planner before preparation, responsive prepared-brief columns, and bounded expanded phone navigation. Search and Privacy were added to the comparison selector. Restaurant data, feature switches, selected component layouts, availability/expiry guards, and JavaScript action logic were preserved.

Final browser probes covered all 258 guest pages at 1280, 390, and 320 px (774 page/width combinations), with no horizontal overflow, clipped card/panel containers, or missing primary headings. Visual review covered representative remaining page families across the enabled presets. Additional workflow probes covered brief preparation, empty-search/recovery, and expanded navigation across nine presets and three widths (81 checks), with no failures or phone menu overlap with fixed quick actions. The café planner changed from one 760 px column to two 576 px columns at 1280 px after preparation, retained the supplied local test notes, and reported that nothing was sent or saved. A native keyboard check opened More with Enter and closed it with Escape, retaining focus on its summary. No email, booking, download, or clipboard action was invoked.

Search and Privacy comparison frames rendered the correct scoped pages at 390 px. All 108 guide layout/state examples fit the guide's 360 px previews. All 29 targeted component, guest-integration, and preset checks passed; `git diff --check` passed. No console errors/warnings appeared in the checked planner/comparison journeys. The existing synthetic publication-isolation checks passed with the expanded comparison catalog.

GitNexus file impacts for both stylesheets and the preset-switcher template returned `UNKNOWN`, with no resolved callers/processes. Direct inspection confirmed the shared stylesheet bundle and the guide's direct call to the switcher; absent graph edges were not treated as a safety result. The installed CLI was used without installing or reanalyzing.

These are local illustrative-page and automated-browser results. The full suite, real devices, human assistive-technology use, print, factual/media review, real providers, deployment, and release acceptance remain unconfirmed. Unrelated local changes were preserved; no staging, commit, push, deployment, or publication was performed.

## October 13 desktop and phone component refinement

The integrated pages were reviewed across all nine presets. Before changes, browser measurements covered 45 affected pages at 1280 and 390 px (90 page/width combinations), with visual comparisons of menu sections, tasting menus, flights, team profiles, rooms, and visit guidance. The review found compact menu sections being overridden by dish-grid composition, excess nested menu padding, serif detail headings in sans-serif designs, compact thumbnail backgrounds stretching with biographies, and single profile/room records leaving an empty grid column.

Refinements were limited to the two component/preset stylesheets and documentation. They correct category grouping, reduce nested spacing, keep dish permalinks at least 44 px high, bound desktop reading widths, refine mobile headings and image heights, prevent thumbnail stretch, improve single-record composition, wrap metadata more closely, and give the six components preset-specific type, borders, and surfaces. No record text, data fields, feature switches, layout selections, or action logic changed in this pass.

For the first three-dish category in each illustrative menu at 390 px, the rendered heights changed as follows (pixels, including the category heading and dish permalinks):

| Preset | Before | After |
| --- | ---: | ---: |
| Bakery | 861 | 722 |
| Bar | 836 | 653 |
| Café | 783 | 721 |
| Diner | 912 | 653 |
| Fast casual | 782 | 720 |
| Fine dining | 771 | 653 |
| Food truck | 979 | 653 |
| Kitchen-sink | 1007 | 793 |
| Multi-location | 959 | 712 |

Final browser probes covered the 45 affected component pages plus all nine homes at 1280, 390, and 320 px: 162 page/width combinations with no horizontal overflow. New component containers on the 135 component-page combinations showed no vertical clipping. The 36 new guide layout/state examples also fit their 360 px previews. Visual inspection covered the updated menu, tasting, flight, profile, room, and arrival treatments; the browser console reported no errors or warnings in the review session. Compact team thumbnail panels measured 88 px high instead of stretching to the biography. All 29 targeted component, guest-integration, and preset tests passed, including synthetic publication isolation; `git diff --check` passed.

GitNexus file impacts for both stylesheets returned `UNKNOWN`, no resolved callers/processes, and an explicit warning that absent edges do not prove safety. Direct inspection confirmed both stylesheets are bundled by the shared base template for all guest and guide pages. The generated runner attempted an unavailable npm lookup; impacts succeeded through the already-installed GitNexus CLI, without reanalysis or installation.

These are local illustrative-page and automated-browser results, not real-device, human assistive-technology, print, factual/media, provider, deployment, or release acceptance. The full suite was not run. Existing unrelated changes were preserved; no staging, commit, push, deployment, or publication was performed.

## October 13 guest-page component integration

The six additions now render from restaurant data on enabled guest pages across all nine presets. Menu-section wraps the existing dish-card markup; typed Specials records use tasting-menu/beverage-flight; team and events use team-profile/dining-space; accessibility and location detail pages derive visit-steps from the location's access facts. Preset layout selections and feature switches remain unchanged. The nine illustrative datasets gained clearly labeled sample component details; the client restaurant data and saved selection were preserved.

All 29 focused checks passed: 10 guest integration/data-contract tests, 13 preset-layout/switcher tests, and six component-library tests. New checks cover optional-field compatibility, component/collection allowlists, blocked identity/state/provider overrides, serving sizes and structured selections, local-image validation, configured guest layouts across all nine presets, record detail rendering, search fields, all access facts including extra keys, owner-data isolation, and provider/calendar guards for available, paused, expired, cancelled, sold-out, unavailable, and demo records. The existing synthetic publication test also passed with the expanded source.

Browser checks covered 45 enabled Menu, Specials, Team, Private events, Accessibility, and first-location detail pages across the nine presets at 320 px, with the expected components present and no horizontal overflow. Kitchen-sink and fast-casual menu comparisons at 390 px retained search, empty-result handling, and dish-permalink recovery. A fine-dining tasting menu was visually inspected in its split layout at 1280 px. Multi-location arrival steps followed location selection and updated URL context. No console errors or warnings appeared in the checked comparison and access journeys.

These are targeted local and automated-browser results. The full suite, real devices, human assistive-technology use, print acceptance, factual/media review, and real provider outcomes remain outside this verification. No external provider was called, and no Git, publication, or deployment action was performed.

## October 13 component library expansion

Six restaurant components were added: menu sections, tasting menus, beverage flights, team profiles, private dining spaces, and visit planning steps. Each has three layouts and populated/empty examples. The guide now renders 18 components, 54 layouts, and 108 layout/state combinations. All nine presets select layouts for the new components and expose a Component showcase in the design comparison page selector.

Focused verification passed: six component tests, seven preset-layout tests, and six preset-switcher tests. These cover the full guide rendering, content and action preservation across layouts, unavailable and empty states, preset configuration, scoped links under a base subpath, unchanged owner data/configuration, and omission of the guide and both root/preset showcase pages from a synthetic publication build. One new showcase assertion initially failed because its parser concatenated text across tags; it was corrected to compare fixture fields directly, and the six switcher checks passed on rerun.

Browser checks confirmed side-by-side showcase frames at 1280 px, phone frames at 390 px, all six examples in every preset, and no horizontal overflow across all nine showcases at 320 px. All 36 new layout/state examples fit the guide's 360 px component previews. Representative team and room layouts were visually inspected; the room panel was checked at an emulated 390 px mobile viewport. No console errors or warnings appeared on the checked comparison and showcase pages.

These results cover this expansion only. The full `./he test` suite, real devices, human assistive-technology use, print, business facts, and real provider outcomes were not checked. No GitNexus tool or local index was accessible in this workspace, so dependencies were inspected directly in the owning templates and configuration. No publication, deployment, or Git action was performed.

## October 12 component and preset layout checks

The focused component/preset work was executed locally: all 12 targeted tests passed, both JavaScript files passed syntax checks, and all nine illustrative presets built successfully with warning failures enabled. Those builds checked local links/assets/anchors, duplicate IDs, menu heading order, module routes, and preview guide isolation. The synthetic integration fixture also covered zero prices, sold-out items, paused-provider fallbacks, expired events, calendar download attributes, hours, FAQs, contact details, and guide layout defaults.

Browser checks covered 320 px layouts across all nine presets, representative desktop compositions, menu search and permalink recovery in all three dish layouts, and the guide's deep-link, comparison, and preset-reset behavior. No page-level horizontal scrolling was found on the checked pages. These are browser automation checks, not real-device or assistive-technology acceptance. Actual calendar-app import, print acceptance, provider outcomes, copy/recovery/publication gates, and the full `./he test` suite were not rerun for this layout change.

## October 12 preset switcher checks

The switcher adds five focused tests for all nine examples, preset-specific content/layouts and enabled routes, navigation under a base subpath, guide defaults, unchanged owner configuration/data, and complete omission from a synthetic local publication build. This publication check is limited to the new route boundary; it does not establish release or provider readiness.

Browser checks cover the comparison controls, unavailable-page fallback, desktop/phone frame widths, scoped guest navigation, reset behavior, and the full-page link following the current embedded page. The studio retains normal design links without JavaScript. The existing component and preset-layout tests remain part of focused verification.

## Broader owner-run verification

The broader October 3 implementation previously remained unexecuted at Ryan's instruction. The targeted results above cover only the component and preset work; they do not establish a passing result for the entire revision.

Run from the project directory:

```sh
./he test
```

This runs contract tests and JavaScript syntax, then builds the current selection and all nine illustrative presets into temporary directories. It inspects local links, media references, anchors, duplicate IDs, enabled/disabled routes, menu heading order, search consistency, Unicode identity serialization, copy recovery, frozen client helper portability, an SVG under assets, a changed dish count/zero price, and a synthetic publication fixture. Build-contract tests also cover overwrite refusal and output hashes. It never publishes or calls providers. Failures report the relevant command or field; report those results back before treating this revision as verified. It does not execute browser interaction tests.

`./he check` is the short data-contract/readiness check. `./he doctor` checks selected data, runtime availability, and the supported Hugo version. No GitNexus analysis is part of verification.

## Browser acceptance after automated checks

Use `./he preview`. Check the following focused journeys on desktop and a narrow viewport, plus keyboard and the assistive technology you use:

- Search `hours`, `parking`, `allergies`, and an actual dish name.
- Select a location and service; follow menu/order/booking links and check context. Open a dish permalink and verify the dish is visible.
- Open navigation with the keyboard; close with Escape; check focus and fixed mobile actions at zoom and with the software keyboard open.
- Exercise empty menus/locations, long names, SVG/raster media, and schedule exceptions in the relevant timezone.
- Verify expired/cancelled event behavior and inspect the downloaded calendar in a calendar app.
- Prepare and edit a brief; change inputs; copy, download, save/import a draft, and clear it. Inspect actual downloaded contents. Test unavailable clipboard access. No inquiry should be sent.
- Print full and filtered menus and verify identity, prices/currency, availability, and review date.
- Review the local publication artifact: no operator guide or preview bar, correct canonical URLs, sitemap, actual contact and provider routes.

External acceptance remains separate: factual business review, media permissions, actual restaurant access details, real-provider outcomes, deployed header behavior, and host rollback.

## Historical baseline

The September 19, 2026 record described the earlier 24-module/28-HTML-page demo, selected disabled routes, cafe copying, JavaScript syntax, and limited browser checks. That result belongs to the earlier source. Current record/location detail pages change page counts; exact counts are derived during verification rather than hardcoded. The October 3 review also reproduced search, Unicode, SVG and copy-recovery issues. Neither historical record validates the new implementation.
