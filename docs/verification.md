# Verification evidence and owner handoff

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
