# Restaurant experience and editorial guide

Use this guide to turn a Hot Eats preset into a website that feels like the restaurant. The guest journey starts with the menu, the right place and time, and the next action. The restaurant’s name, colors, photography, and voice carry that journey.

## Design the visit

| Guest question | Put it here | Check it with |
| --- | --- | --- |
| What can I eat, and what will it cost? | A text menu with sensible categories, prices and units, availability, and shareable dish links | Find a dish, check its availability, and print the relevant menu. |
| Where and when can I go? | Location pages with address, service hours, schedule exceptions, arrival and access details | Find the right location from a shared link and check an upcoming holiday. For trucks, use the stop and date. |
| Can I order, book, or ask a question? | A clearly named action associated with the right location and service | Follow an approved destination or find a specific fallback when the service is paused. |
| Will the visit work for me? | Reviewed information about the entrance, parking, seating, restrooms, and a reliable contact | Use the information to plan arrival and find who can answer a remaining question. |
| Can I bring a group? | Event or catering facts such as capacity, lead time, menu options, and terms | Find the capacity, share the facts, and locate the next inquiry step. |

Use menu and visit information early on mobile. Start a café with menu and hours, a truck with stops and times, and a multi-location restaurant with location choice. Add specials, story, private dining, and other pages when the restaurant has content and a person to keep it current. Compare real presets under [the living guide](http://127.0.0.1:1417/site-kit/#presets) during `./he preview`.

## Apply the restaurant’s visual identity

1. Choose a preset for the business pattern and guest path. Review its home composition, menu layout, location experience, and service actions.
2. Record the restaurant’s logo versions, colors and approved pairings, type styles, photography, and contact details in one client reference. Use the Hot Eats identity for product collateral.
3. Adapt type and color with actual guest content. Check a long dish name, a price with a unit, an updated schedule, a service notice, and a long location name. Keep links recognizable and state labels visible when color is absent.
4. Use photos of the actual food, people, and space with the restaurant’s permission. Pair a food photo with its name, description, and price in text. Show a real approach or entrance when a photo helps guests plan a visit.
5. Check phone, desktop, keyboard, text enlargement, and printed menu use against the accepted restaurant facts. Put visit details in page text so guests can read, copy, and share them.

Use a 44 px target for key touch controls in new designs, generous spacing, visible keyboard focus, and predictable reading order. Pair icons with text where a guest needs to understand a service or state. Provide meaningful alternatives for informative images and captions for video. Keep motion optional and away from tasks guests need to finish.

## Write for a service day

Examples below use placeholders or illustrative content. Check facts with the responsible person before release.

| Field or state | Example | Review |
| --- | --- | --- |
| Dish | “Mushroom melt. Roasted mushrooms, Swiss, and mustard on sourdough. $14.” | Verify ingredients, price, portion, and which location offers it. |
| Sold out | “Mushroom melt · Sold out today” | Keep the name and status readable together. Confirm when availability should reset. |
| Schedule exception | “Thursday, November 26 · Closed for Thanksgiving. Open Friday at 8 a.m.” | Confirm location, day, date, time zone, and next opening. |
| Service paused | “Pickup ordering is paused. Call [location phone] with a pickup question.” | Confirm the fallback is staffed and appropriate for the service. |
| Provider action | “Continue to [Provider] to reserve a table at [Location].” | Confirm the destination matches the location and the provider shows current terms. |
| Entrance | “The step-free entrance is on [street]. The door opens outward. Call [location phone] if you need help.” | Walk the route and check dimensions or assistance details where relevant. |
| Dietary information | “Ask staff about ingredients and cross-contact before ordering.” | Use the restaurant’s verified ingredient and handling information. |
| Group inquiry | “The garden room seats 18. Contact [team] at least [lead time] before your event.” | Confirm capacity, arrangement, terms, and a responsive contact. |

Choose labels such as “Menu,” “Hours and directions,” “Order pickup,” “Book a table,” and “Call [Location].” Give two similar links distinct labels when they lead to different services. Publish an “open now” state only when the schedule and exceptions are reviewed. Use explicit dates for events and seasonal notices. Use genuine, approved reviews and attributions if reviews are enabled.

## Content and handoff

- Assign an owner for menu and prices, hours and closures, service availability, arrival information, and provider destinations. Give each person a concrete update and review path.
- Keep canonical restaurant facts in the [public data model](../data-model.md). Use the [owner guide](../owner-guide.md) for daily updates, preview diffs, snapshots, and menu CSV work.
- Choose layouts from [the component library](../component-library.md). Review the displayed guest facts and action in both the ordinary and unavailable states.
- Before release, check the same menu, hours, address, and provider information in the restaurant’s other active channels. Review the [publication and provider checks](../publication.md) with the owner. Record actual acceptance in the project that owns the client site.
