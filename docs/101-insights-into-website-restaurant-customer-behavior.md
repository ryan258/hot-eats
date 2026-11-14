# 101 insights into website restaurant customer behavior

These are guest-behavior notes for planning, writing, and reviewing a Hot Eats restaurant site. They come from common restaurant-website patterns. They are not measured data, because Hot Eats collects no analytics. Treat each one as something to check with the owner, the questions staff hear, and provider reports. This page quotes no figures. Check any statistic against its primary source before publishing it.

Each item names the behavior, then what the site should do about it. "Hot Eats:" points to an existing feature that already handles it.

## Why guests arrive (1–10)

1. **Most visits are a single errand.** Guests come with one question: are you open, what's on the menu, where are you, can I order? Then they leave. Put those answers above any story. Hot Eats: home schedule, menu, and visit sections.
2. **The decision is often half-made already.** Visitors usually arrive from maps, a friend, or social media. The site confirms the choice more often than it persuades. Design it to confirm, not to help them discover.
3. **Hunger leaves little patience.** Someone picking a place for the next hour will put up with very little friction. Load speed and tap count matter more than visual flourish.
4. **Planners and impulse diners behave differently.** Someone planning Saturday dinner reads. Someone getting lunch now scans. Serve both with a quick-to-scan top layer and detail one tap deeper.
5. **Guests land on deep pages.** Search results and shared links drop people on a dish, location, or event page, not the homepage. Every page needs a route to hours, location, and the primary action. Hot Eats: stable dish links, location detail pages.
6. **Guests search in their own words.** "Gluten free," "GF," "celiac." "Takeout," "to go," "pickup." Search should match synonyms as well as the restaurant's own terms. Hot Eats: guest-task search with synonyms.
7. **Many visits are re-checks.** Regulars come back to confirm hours or today's special, not to browse. Keep facts that change often in the same place every time.
8. **Guests often check for someone else.** One person looks at the menu for a group, a parent, or a colleague. Make the menu easy to share and print. Hot Eats: full and filtered menu printing.
9. **The next visit is often on another device.** Guests plan on a desktop and act on a phone. Stable URLs let them pick up where they left off.
10. **Some visitors are not diners.** Job seekers, press, suppliers, and event organizers each have their own task. Give them separate, clear paths that stay out of the guest's way. Hot Eats: careers, press, and catering records.

## On the phone, on the move (11–20)

11. **The phone is the default device.** Design and review at phone width first. Desktop is the variant.
12. **Thumbs, not cursors.** Call, directions, order, and menu should be large tap targets within easy thumb reach. Hot Eats: mobile quick actions.
13. **Tap-to-call is expected.** A phone number that isn't a link looks broken. Hot Eats: click-to-call.
14. **The address should open maps.** Guests tap addresses more than they copy them. Link straight to directions.
15. **Signal is unreliable.** Parking garages, rural roads, and crowded venues all drop signal. Light pages and a reading view that works without JavaScript keep the core facts reachable. Hot Eats: no-JavaScript reading fallbacks.
16. **PDF menus frustrate phone users.** Pinch-zooming a scanned PDF is a common reason guests give up. Publish the menu as real page text and offer printing as a second option.
17. **Guests are often nearby already.** They ask "where do I park?" and "which entrance?" from the car. Put access facts on the location page. Hot Eats: access facts.
18. **Pop-ups cost more on small screens.** An email sign-up box that covers the hours on a phone blocks the reason the guest came. Keep pop-ups off guest pages.
19. **Autoplay video and heavy hero images slow the page.** They delay the one thing the guest wants. Images should build appetite, not hold up the menu.
20. **Guests take screenshots.** Menus, hours, and specials get screenshotted and texted to friends. Keep each key fact readable on one screen.

## The menu (21–35)

21. **The menu is usually the most visited page.** Treat it as the main product page, not an attachment.
22. **Price drives the decision more than description does.** When prices are hidden or missing, guests assume the worst. Show them.
23. **Guests scan instead of reading.** Short dish names, a one-line description, and clear categories beat paragraphs.
24. **Guests look up dishes they've heard about.** A searchable menu with a link for each dish answers "do they still have the…?" Hot Eats: menu search and stable dish links.
25. **An outdated menu breaks trust fastest.** Finding a dish gone or a price changed on arrival feels like a broken promise. Make the menu easy to keep current. Hot Eats: `./he menu`, CSV export and import.
26. **"Sold out" beats silence.** Guests trust an item marked unavailable more than one that quietly disappears. Hot Eats: explicit sold-out states.
27. **Guests filter by situation.** Brunch or dinner, dine-in or takeout, this location or that one. Filters should match how service actually differs. Hot Eats: category, service, and location filters.
28. **Photos sell dishes, and bad photos unsell them.** One honest photo beats many inconsistent ones. No photo beats a misleading one.
29. **Too many choices slow the decision.** Long menus need clear sections and highlighted signature dishes.
30. **First-timers look for guidance.** Labels like "popular" or "house favorite" give new guests a recommendation inside the menu itself.
31. **Specials give guests a reason to come back to the site.** A visible, dated specials section rewards checking again. Hot Eats: specials records.
32. **An undated special looks stale.** Guests can't tell whether it has ended. Show when it runs.
33. **Drink programs draw a different reader.** Drink-focused visitors want producers, styles, and flights, not just a price list. Hot Eats: beverage-flight component.
34. **Tasting menus need the full picture up front.** Price per person, length, number of courses, pairing options, and dietary flexibility answer the booking question. Hot Eats: tasting-menu component.
35. **Parents look for kids' options and portion sizes.** Label them clearly so they are easy to find.

## Hours, location, and "are you open right now?" (36–48)

36. **"Are you open now?" is the most urgent question.** A clear open-or-closed line beats a weekly table. Hot Eats: current-status display based on the approved schedule.
37. **Weekly tables get misread.** Guests read the wrong day's row. Show today first.
38. **Split hours confuse people.** Show the lunch close and the dinner reopening explicitly. Hot Eats: split schedules.
39. **Holiday and one-off closures are where trust breaks.** The worst result is a guest at a locked door the site said was open. Hot Eats: date exceptions, `./he today --closed`.
40. **The kitchen closes before the doors do.** Guests want the last-order time, not just the closing time.
41. **Guests trust map listings when they disagree with the site.** Keep hours identical everywhere. Update the site first, then copy the hours to every listing.
42. **Guests of multi-location restaurants need the right location fast.** Ask for the location before showing its hours, menu, or ordering. Hot Eats: location cards and handoffs for each location.
43. **Guests mix up similar locations.** Names based on the neighborhood or street beat "Location 2."
44. **Parking and transit decide whether a guest comes.** This matters most for a first visit or a group.
45. **Guests check accessibility before they arrive.** Step-free entry, restrooms, and seating options. Listing them prevents an awkward arrival. Hot Eats: access facts.
46. **Food trucks have a "where are you today?" problem.** The schedule is the product. Hot Eats: truck stop records.
47. **Temporary announcements need an end date.** A banner about a closure that has already passed makes the site look abandoned. Hot Eats: `./he today --announcement`.
48. **Visitors may be in another time zone.** Travelers planning from elsewhere can misread hours that give no time zone.

## Trust and the decision to come (49–60)

49. **A current-looking site signals a restaurant that's still open.** Old copyright years, past events, and dead links suggest it may have closed.
50. **Guests read reviews elsewhere first.** Quotes on the site add color but don't prove anything. Keep a few honest ones. Hot Eats: quote-card component.
51. **Made-up or uncredited praise backfires.** Guests trust quotes with a named source. They distrust anonymous superlatives.
52. **Story matters more for destination dining.** Guests read the story at fine-dining and chef-driven places, rarely at quick-service ones. Give the story more space in some presets than others.
53. **Faces build trust.** Profiles of owners, chefs, and staff make a place feel accountable. Hot Eats: team profiles.
54. **Sourcing claims need specifics.** "Local" means little. Named farms and suppliers mean something. Hot Eats: sourcing records.
55. **Press works mostly as a shortcut to credibility.** Guests skim the outlet names and headlines. Journalists need a backgrounder. Hot Eats: press records and backgrounder.
56. **Interior photos answer "what's it like?"** The room's atmosphere decides date nights, business meals, and group dinners.
57. **Guests of nicer places ask about dress code and noise.** Answer both in the FAQ before they turn into phone calls.
58. **Make the price range obvious before the menu.** Guests rule themselves in or out early. A mismatch wastes everyone's time.
59. **Clear policies reduce anxiety.** Say plainly how reservation holds, cancellations, corkage, and large-party gratuity work. Guests dislike surprises.
60. **Respecting privacy is a small trust signal.** No tracking banners and no surprise data collection. Hot Eats: no analytics, privacy page.

## Ordering, reservations, and handoffs (61–72)

61. **Guests want the action, not an explanation.** "Order pickup" and "Book a table" should be one tap away from any page.
62. **Every handoff to another site loses some guests.** Each redirect is a chance to drop off, so show clearly where the click goes before the guest taps.
63. **Say where the button goes.** "Order on [provider]" sets expectations better than a generic "Order now."
64. **Paused services need to say so.** An order button that looks normal but leads to a closed online store frustrates guests more than a clear "Pickup paused today." Hot Eats: available, paused, and unavailable service states.
65. **Always offer a fallback.** When online ordering or booking is down, show the phone number. Hot Eats: fallback contacts.
66. **Guests notice price differences between ordering channels.** Whether to use delivery apps is the owner's choice, but guests may ask why app prices are higher. Don't hide it.
67. **Orders placed at the wrong location are a real failure.** Name the location in every ordering handoff. Hot Eats: provider handoffs for each location and service.
68. **Walk-in guests want to know about waits.** If you don't take reservations, say so and explain how the waitlist works.
69. **Large parties don't fit online booking.** Give groups their own clear path.
70. **Gift card interest jumps around the holidays.** Make gift cards easy to find in that season.
71. **Guests distrust forms that don't say what happens next.** If a form only drafts an email, say so. Never suggest a booking was made. Hot Eats: gathering briefs that hand off to the guest's mail app, with no inquiries sent by the site.
72. **Confirmation matters more than speed.** Guests want to know an order or booking actually went through. The provider handles that confirmation, so the site should point there.

## Dietary needs, allergens, and accessibility (73–82)

73. **Many guests filter by diet first.** One person's restriction often decides where the whole group eats.
74. **Consistent symbols beat improvised labels.** Include a key that explains each symbol. Hot Eats: dietary-key component.
75. **"Can be made gluten-free" is not the same as "gluten-free."** Separate dishes that can be adjusted from dishes that already comply.
76. **Guests with allergies double-check in person anyway.** The site's job is to show the restaurant takes allergies seriously and tell guests how to confirm with staff. Avoid absolute guarantees.
77. **Guests trust cross-contact warnings more than silence.** Saying the kitchen handles nuts or gluten earns more trust than it costs.
78. **Screen-reader users need real text.** Image menus and text inside graphics are unusable for them. Hot Eats: menus published as page text.
79. **Contrast and font size matter in dim rooms.** Guests check the menu on a phone at the table, in low light.
80. **Every action should work with a keyboard and assistive tools.** That includes the order and booking buttons.
81. **Plain language beats culinary jargon.** It helps accessibility and translation. Explain unfamiliar terms briefly.
82. **Guests who speak other languages use browser translation.** Page text translates. Images don't.

## Groups, events, catering, and private dining (83–90)

83. **The organizer is doing a job for other people.** They need facts they can forward: capacity, minimum spend, menus, and deposits. Hot Eats: dining-space and package-card components.
84. **Capacity is the first filter.** Seated and standing counts for each space answer "will we fit?"
85. **Price ranges cut down on back-and-forth.** Even "from $X per person" helps an organizer decide whether to ask.
86. **Organizers want something to send.** A brief they can share or export helps them get approval. Hot Eats: gathering briefs with export.
87. **Events need an add-to-calendar option.** It turns interest into attendance. Hot Eats: calendar downloads.
88. **Past events should look past.** An expired event shown as upcoming damages trust. Hot Eats: expired-event states.
89. **Catering buyers plan days ahead and compare quotes.** Lead time, minimum order, delivery area, and setup are on their checklist. Hot Eats: catering records.
90. **Recurring events build habits.** Trivia night or a weekly special gives guests a reason to check back. List the days clearly.

## After the meal and return visits (91–96)

91. **Regulars want to know what's new.** News and seasonal changes reward a return visit. Hot Eats: news records.
92. **Guests look up a dish they ate.** "What was that dish?" A link for each dish helps them find and share it. Hot Eats: stable dish links.
93. **A direct feedback channel heads off public complaints.** A visible way to contact the restaurant gives guests an alternative to a public review.
94. **Guests often ask about lost items and receipts.** A clear contact route handles these without a phone queue.
95. **Seasonal menus create anticipation.** Telling guests when the menu changes gives them a reason to come back.
96. **Job seekers are often former guests.** A careers page with clear roles and a way to apply turns fans into staff. Hot Eats: careers records.

## What this means for the owner (97–101)

97. **Accuracy beats novelty.** The best guest experience is correct hours, a current menu, and a working action button, updated every time something changes.
98. **Phone calls are the measure.** Questions staff answer again and again show what the site leaves out. Add those answers to the FAQ. Hot Eats: FAQ pages.
99. **Small daily edits beat big redesigns.** A site kept true every week does better than a beautiful one left stale. Hot Eats: `./he today`, `./he menu`, recovery snapshots.
100. **Measure with the providers you already use.** Hot Eats collects no analytics. Ordering, booking, and map dashboards already show what guests did. Review those before adding tracking.
101. **Every claim on the site is a promise.** Guests hold the restaurant to its hours, prices, dietary labels, and availability. Review them before publishing. Hot Eats: review status and publication gates.

## Related

[Owner guide](owner-guide.md), [component library](component-library.md), [data model](data-model.md), [publication](publication.md).
