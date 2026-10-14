# Restaurant module contracts

All 24 modules are available in the master. Presets select a coherent subset; the registry controls renderer, navigation group, search vocabulary, and dependencies.

| Module | Renderer | Group | Dependency | Required input |
| --- | --- | --- | --- | --- |
| menu | menu | Dining | — | Approved dishes, prices, modifiers, dietary statements, availability, and a menu review date. |
| specials | records | Dining | — | Approved copy, current availability, and a business owner responsible for updates. |
| locations | locations | Visit | — | Verified addresses, location-specific hours and contacts, accessibility details, and maps links. |
| reservations | action | Dining | — | Verified reservation provider URL, party limits, cancellation policy, and accessibility alternative. |
| ordering | action | Dining | — | Verified ordering provider URLs, fulfillment areas, fees, hours, and location routing. |
| catering | records | Gatherings | — | Actual packages, prices, minimums, lead times, service boundaries, allergen process, and inquiry contact. |
| events | records | Gatherings | — | Real spaces, capacity, accessibility, deposits, cancellation rules, and event contact. |
| planner | planner | Gatherings | one of events, catering | Verified event inquiry email and reviewed planning questions. Preparing a message is not a booking. |
| gallery | gallery | About | — | Actual photos, permission to publish, descriptive alt text, and truthful captions. |
| story | records | About | — | Approved copy, current availability, and a business owner responsible for updates. |
| team | records | About | — | Real names and roles, approved bios, and permissioned photographs. |
| sourcing | records | About | — | Verified suppliers, sourcing practices, and support for any sustainability claims. |
| reviews | records | About | — | Genuine quotes, source URLs, dates, attribution, and permission where required. |
| giftcards | action | Dining | — | Actual provider, redemption locations, terms, balance help, and approved purchase URL. |
| loyalty | action | Dining | — | Confirmed program benefits, eligibility, terms, privacy notice, and enrollment URL. |
| newsletter | action | About | — | Email provider signup URL, consent language, frequency, privacy notice, and unsubscribe process. |
| news | records | About | — | Approved copy, current availability, and a business owner responsible for updates. |
| calendar | records | Gatherings | — | Actual event dates, venue, ticketing, availability, restrictions, and cancellation details. |
| careers | records | About | — | Current vacancies, location, compensation details as applicable, requirements, and application destination. |
| faq | faq | Visit | — | Owner-confirmed answers on walk-ins, reservations, dietary needs, parking, children, pets, and accessibility. |
| contact | contact | Visit | — | Verified public email, phone, response expectations, and privacy handling. |
| accessibility | records | Visit | — | Location-specific access facts and an actual accessibility contact. |
| press | records | About | — | Approved copy, current availability, and a business owner responsible for updates. |
| foodtruck | records | Visit | — | Confirmed schedule, parking locations, service boundaries, booking terms, and current updates. |

Shared flags: `visit`, `search`, `announcement`, `quicklinks`. Homepage sections: `hero`, `announcement`, `ticker`, `menu`, `story`, `visit`, `schedule`, `directory`. Sections may appear once each.

Record modules use structured facts, dates where relevant, attachments, links, provenance, and generated detail pages. Reviews and careers begin empty. Action modules require an explicit available state, an available associated service, and an HTTPS destination before linking out.

Read `docs/data-model.md` for field contracts and `docs/verification.md` for the unexecuted verification handoff.
