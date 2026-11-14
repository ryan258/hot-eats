# Hot Eats Roadmap

Hot Eats is a local-first, static Hugo restaurant website library and master. It combines a public site, an editable versioned restaurant data model, local owner CLI tools, and independent client-copy tooling.

---

## Completed Milestones

### Milestone 1: Core Engine & Data Model Consolidation
- **Consolidated Schema Version 2**: Authoritative validation in `scripts/model.py` covering types, IDs, references, pricing strings, media containment, timezones, and paired timestamps with explicit UTC offsets.
- **24 Selectable Modules**: Independent modules with dependency graph validation and registry definitions in `data/modules.json`.
- **9 Preset Configurations**: Fully configured illustrative presets (`kitchen-sink`, `diner`, `cafe`, `fine-dining`, `fast-casual`, `bar`, `bakery`, `food-truck`, `multi-location`) with custom compositions and data scenarios.
- **Local Owner Tools**: `./he` entrypoint providing diff-before-save, per-change snapshots, menu CSV export/import, operational logs, and recipe scaling.
- **Staged Sculpting Pipeline**: Copying stages and validates transformations before reserving clean destinations, rolling back partial failures, and isolating private state.

### Milestone 2: Living Component Style Guide & 18 Presentation Components
- **Living Style Guide**: `/site-kit/` living guide rendering 18 components across 54 layouts and 108 layout/state combinations with live search, filters, and code snippets.
- **Preset Studio & Side-by-Side Comparison**: Independent comparison frames for any two presets at desktop (1280 px) or phone (390 px) viewports with URL state tracking.
- **Component Showcase**: Scoped showcase route (`/site-kit/presets/<preset>/component-showcase/`) rendering all six advanced guest components under every preset's configured layouts.
- **Publication Boundary Isolation**: Living style guide and preview routes are strictly excluded from publication builds.

### Milestone 3: Guest-Page Component Integration
- **Menu Sectioning**: `menu-section.html` wrapping validated dishes with independent category layout support and filter preservation.
- **Typed Specials Presentations**: `tasting-menu.html` and `beverage-flight.html` integrated into Specials records via validated `presentation` fields.
- **Team & Event Enhancements**: `team-profile.html` for staff records and `dining-space.html` for private dining/event records with capacity and access facts.
- **Visit Planning Steps**: `visit-planning.html` deriving ordered step-by-step arrival guidance from location access facts for location detail and accessibility pages.
- **Public Data Protection**: Presentation fields cannot override core record identity, availability state, dates, or transactional provider destinations.

### Milestone 4: Multi-Preset Consistency & Responsive Polish
- **Preset Typography & Surfaces**: Cohesive heading fonts, detail weights, borders, and color tokens across all nine presets.
- **Responsive Geometry**: Reading width constraints on desktop, mobile heading scaling, compact thumbnail alignment, and 44 px touch targets for dish permalinks.
- **Remaining-Page Styling**: Unified design treatment extended to service handoffs, catering, calendars, quotes, FAQs, contact panels, and galleries across 258 guest routes.
- **Print Optimization**: Comprehensive `@media print` rules enforcing high-contrast black on white across all presets, automatically expanding accordion disclosures, converting textareas to readable inline copy, suppressing UI controls, and displaying active print scope indicators.
- **Accessibility & Interaction Polish**: Bounded, scrollable mobile navigation above fixed quick actions; native date subfield `:focus-within` outlines; keyboard-closeable details.

### Milestone 5: Multi-Location Experience & Presentation Refinements
- **Header Location Switcher & Persistence**: Header dropdown toggle for multi-location groups, persisting the guest's selected location in `localStorage` (`he-location`) across pages while preserving URL parameters and clearing on "All locations".
- **Location Detail Actions & Scoping**: Context-aware hero actions (Call, Directions, Menu scoped with query param, and online ordering actions), location-specific email, and location-scoped specials, private dining, stories, and catering.
- **12-Hour Schedule Formatting**: Friendly 12-hour AM/PM clock display (`clock.html`) across weekly hours tables and exception dates.
- **Available State Presentation**: Clean presentation hiding redundant "Available" state badges on live record cards while keeping expired/demo indicators.
- **Data Model & Engine Flexibility**: Client profiles override preset configurations (`hugo.toml`, preset, profile); ongoing specials can omit start/end timestamps; location email validation; array-of-tables `[[...]]` TOML serialization in sculpting.

### Milestone 6: Brand Identity, Marketing Kit & Customer Insights
- **Brand Assets & Tokens**: Complete brand identity suite in `assets/brand/` (vector SVG lockups in ink/white/reverse, mark, favicon, social card, tokens JSON/CSS).
- **Brand & Marketing Documentation**: Comprehensive strategy, voice, visual standards, restaurant experience, launch playbook, SWOT, sales kit, and operations in `docs/brand/` plus `101-insights-into-website-restaurant-customer-behavior.md`.
- **Interactive Brand Kit & Sales One-Sheet**: Dedicated preview routes at `/site-kit/brand` and `/site-kit/brand/one-sheet` (excluded from publication builds).

---

## Active & Next Horizons

### Milestone 7: Automated Verification & Regression Suite
- [x] 66-test automated Python and Node regression suite covering data contracts, location navigation, location persistence in `localStorage`, component library, brand preview, and preset switchers.
- [x] Node JavaScript syntax checks passing (`site.js`, `style-guide.js`).
- [x] Fresh Hugo build passing across all nine presets (`kitchen-sink`, `diner`, `cafe`, `fine-dining`, `fast-casual`, `bar`, `bakery`, `food-truck`, `multi-location`) with zero warnings.
- [x] Publication boundary verification ensuring preview routes and `/site-kit/` are strictly excluded from publication output.

### Milestone 8: Real-Device & Provider Acceptance
- [ ] Real-device testing across modern mobile and desktop browsers (iOS Safari, Android Chrome, desktop browsers).
- [ ] Human assistive-technology auditing (voiceover, screen readers, high-contrast themes).
- [ ] Physical print checks for full and filtered menus across paper formats.
- [ ] External provider acceptance for online ordering and reservation integrations.

### Milestone 9: Real-World Business Onboarding
- [ ] Client restaurant data entry replacing illustrative scenario fixtures in `data/restaurant.json`.
- [ ] Media licensing and photography permissions review for all imagery.
- [ ] Direct provider integration and acceptance (reservation platforms, online ordering, loyalty, gift cards).
- [ ] Production domain configuration, HTTPS enforcement, and security header validation.

---

## Key References

- [Architecture & Maintenance](docs/architecture.md)
- [Brand & Marketing Kit](docs/brand/README.md)
- [Customer Behavior Insights (101 Insights)](docs/101-insights-into-website-restaurant-customer-behavior.md)
- [Component Library Guide](docs/component-library.md)
- [Data Model & Presentation Contract](docs/data-model.md)
- [Preset Design Catalog](docs/preset-designs.md)
- [Verification Evidence](docs/verification.md)
- [Remediation & Enhancement Register](docs/remediation-status.md)
- [Owner Guide](docs/owner-guide.md)
