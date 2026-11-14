# Hot Eats visual identity

**Brand direction · November 2026**

Hot Eats looks like a good restaurant's welcome sign. The identity pairs a dark green doorway with warm paper, a clear wordmark, and a short route to the information people need. The open door doubles as a menu board. Use the identity on materials that explain the Hot Eats website kit, its demos, and the work involved in making a restaurant site.

Each restaurant supplies its own identity for its guest site. Lucyd, the diner example, has its own red palette and typography. In a product presentation, use Hot Eats on the cover and surrounding frame, then show the restaurant example at its original colors and proportions with a visible **Illustrative demo** label. Keep both names readable when they appear together.

## Logo system

![Hot Eats primary logo, with an open doorway beside the name](../../assets/brand/hot-eats-lockup.svg)

| Asset | Use |
| --- | --- |
| [Primary lockup](../../assets/brand/hot-eats-lockup.svg) | The default for Paper, White, Mint, and similarly light solid backgrounds |
| [Reverse lockup](../../assets/brand/hot-eats-lockup-reverse.svg) | Ink or Porch backgrounds, including closing slides and dark website headers |
| [One-color Ink](../../assets/brand/hot-eats-lockup-ink.svg) and [one-color White](../../assets/brand/hot-eats-lockup-white.svg) | Single-ink production, grayscale documents, or light-on-dark signage. The symbol's cutouts show the substrate. |
| [Square mark](../../assets/brand/hot-eats-mark.svg) | Social avatars, square tiles, and compact spaces where the name appears elsewhere |
| [Small favicon](../../assets/brand/hot-eats-favicon.svg) | Product tab or 16–32 px icon slot. Simplified door details are legible at this scale. |

- The horizontal lockups use a 300 × 80 SVG canvas. Keep at least one-quarter of the tile height clear of adjacent text, frame edges, and imagery, measured from the visible mark. At the source size this is 16 units. Use the same proportion at other sizes.
- Start at 144 CSS px wide for the full lockup or 36 mm wide for print. Use the square mark from 32 CSS px. Below 32 px, use the favicon variant and keep an adjacent or programmatic Hot Eats label.
- Scale uniformly. The lettering is drawn as paths and travels with the asset. Keep the proportions, fill colors, spacing, and internal doorway details intact. Avoid outlines, shadows, gradients, rotations, and placing the mark directly over busy photography.
- Use “Hot Eats” as alt text when the image is the only brand name or link label. If a visible Hot Eats label already names the same destination, use empty alt text for the repeated image. Give an icon-only link a specific accessible name such as “Hot Eats home.”
- For an approved partner's identity, place the two marks side by side with a gap of at least half the Hot Eats tile height. Use the partner's approved asset and name the relationship in copy. Size them for comparable legibility.

## Color

Paper and Ink carry the content. Porch identifies the product and its primary actions. Mint groups supporting information. Brick marks a callout or focus on light surfaces. Use Honey for the door detail, occasional graphic emphasis, and focus on dark surfaces.

| Color | sRGB | Use |
| --- | --- | --- |
| Paper | `#F9F4E8` | Primary canvas |
| Ink | `#192D27` | Text, dark canvas, one-color mark |
| Porch | `#275344` | Primary action fill, brand tile, dark section |
| Brick | `#9F3E29` | Emphasis, warning labels, focus on light surfaces |
| Mint | `#DDE9D8` | Supporting panel or specimen background |
| Honey | `#F6C96B` | Graphic accent and focus on dark surfaces |
| Muted | `#45584D` | Secondary text on light surfaces |
| Line | `#778B7C` | Rules and control boundaries on Paper or White |
| White | `#FFFFFF` | High-contrast button text or neutral canvas |

Use [the token registry](../../assets/brand/brand-tokens.json) for design handoff and [the scoped CSS tokens](../../assets/brand/brand-tokens.css) for product web surfaces. Assign `hot-eats-brand` to the container that owns the product styling. Keep restaurant pages on their selected preset and client tokens. Use sRGB for digital exports. For print, give the vendor the vector artwork and ask for a proof using its output profile and stock. Approve Paper and Honey on that proof because the stock affects how both reproduce.

### Contrast pairs

Calculated using the WCAG relative-luminance formula for flat sRGB colors. Use 4.5:1 or higher for ordinary text and 3:1 or higher for required control boundaries and graphics. Inspect the finished composition when photos, opacity, or other backgrounds change adjacent colors. [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

| Foreground on background | Ratio | Application |
| --- | ---: | --- |
| Ink on Paper | 13.23:1 | Default text |
| Muted on Paper | 6.94:1 | Captions and secondary copy |
| Porch on Paper | 7.95:1 | Links and secondary actions |
| Brick on Paper | 5.99:1 | Warning label or light-surface focus |
| White on Porch | 8.72:1 | Primary button |
| White on Brick | 6.57:1 | Strong callout |
| Ink on Mint | 11.56:1 | Text in a supporting panel |
| Porch on Mint | 6.95:1 | Link or functional border on Mint |
| Ink on Honey | 9.33:1 | Text on an accent panel |
| Honey on Ink | 9.33:1 | Focus ring on Ink |
| Honey on Porch | 5.60:1 | Focus ring on Porch |
| Line on Paper | 3.32:1 | Functional boundary on Paper |
| Line on White | 3.64:1 | Functional boundary on White |

Line on Mint measures 2.90:1. Use Porch for meaningful dividers and control outlines on Mint. Pair every status color with a written label such as **Ordering paused**. Use a 3 px visible focus ring offset 3 px from controls, with Brick on light surfaces and Honey on dark surfaces. Check the adjacent color in each final placement. These measurements cover palette pairings. Full pages and exports need their own review.

## Typography

- **Bricolage Grotesque** for campaign headlines, section titles, and short display statements. Use 650–750 at normal width. Local fallback is Avenir Next, then the system sans serif. [Bricolage Grotesque by Mathieu Triay](https://ateliertriay.github.io/bricolage/)
- **Atkinson Hyperlegible Next** for paragraphs, controls, labels, captions, and numerals. Use 400 for body and 650–700 for emphasis. Local fallback is the system sans serif, then Arial. [Atkinson Hyperlegible Next by Braille Institute](https://www.brailleinstitute.org/freefont/)
- Use these families from local installations when available. The current assets and CSS fall back to local system faces and make no font requests. If a future public site needs consistent web typography, use approved self-hosted files with their license notices and recheck line wraps after loading. Keep live text editable until preparing an export. Keep the outlined logo files as supplied.

| Role | Size / line height | Use |
| --- | --- | --- |
| Campaign title | 40–76 px / 1.06–1.15 | One thought, usually two lines on a large canvas |
| Section heading | 28–44 px / 1.12–1.20 | A clear label for the following material |
| Card heading | 20–26 px / 1.2–1.3 | The action, capability, or fact people are looking for |
| Body | 17–20 px / 1.5–1.65 | Aim for 45–70 characters per line |
| Labels and captions | 15–17 px / 1.35–1.5 | Readable in context, including screenshot captions and form labels |

Use relative sizing for web layouts and permit wrapping. Set longer copy flush left. Keep controls, instructions, prices, and business hours in sentence case. For a slide or projected demo, start with at least 28 px for supporting copy and judge from the back of the room. For a letter-size one-sheet, start at 12 pt for body text.

## Layout and graphic language

- Use a 4 px base step with common gaps of 8, 12, 16, 24, 32, 48, and 64 px. On wide web layouts start from a 12-column grid with a max content width of about 1,160 px. Keep the reading column closer to 68 characters. On narrow screens, use a single column with 16–24 px side margins and put the main action before a supporting image.
- Lead with one headline, one description, and one main action. Place a guest task or actual demo screen alongside it on wide layouts. Put proof after the promise. Use the doorway arch to frame a single useful example. Group related facts with Mint or a thin rule. The logo remains the most compact expression of the arch.
- Use 8 px radii for controls and 12 px for panels. Favor simple borders and flat surfaces. Use at least a 44 × 44 CSS px actionable area for touch controls. Underline inline text links and place specific visible labels beside icons.
- Draw action icons on a 24 px grid with approximately 2 px strokes and simple shapes. Use menu rows, a clock, a map pin, and an arrow where their labels clarify an action. Reserve the open-door mark for identity. Keep functional icons legible at 16–24 px and use native buttons or links for interactions.
- Use motion to explain a change of state or location in the interface. Keep it short, respect reduced-motion settings, and provide an equivalent still or textual explanation for a motion-led demo. Leave campaign illustrations still by default.

## Photography, screenshots, and captions

Use real restaurant details with permission. Prioritize an entry guests can recognize from the street, food as served, and an arrival or service detail that explains the experience. Keep color natural and show enough context to recognize the place. An inviting counter, a readable menu, or an actual front door can explain the product better than a generic overhead food spread.

For product proof, capture the rendered website using the selected restaurant example. Frame the exact task, such as finding today's hours or locating pickup details. Capture a narrow and a wide view when the layout behavior matters. Keep screenshots aligned to the same viewport, use a neutral border, and give the caption a verb. Example caption **Find the location and today's hours before leaving home.** Label illustrative content clearly. Separate a screenshot of an example site from any approved customer quotation or result.

Keep rights and permission details with each supplied image. Keep text as HTML when someone needs to act on it. Repeat important screenshot or image text in nearby copy or alt text as appropriate. For an animated walkthrough, caption narration and keep the underlying path available in text.

## Collateral masters

| Master | Adaptation |
| --- | --- |
| [Social and link-preview card](../../assets/brand/hot-eats-social-card.svg) | 1,200 × 630 px. Editable headline, descriptor, and guest-task labels. [Download the sRGB PNG](../../assets/brand/hot-eats-social-card.png) for the supplied copy. Its text uses the approved local fallbacks. Keep the logo and headline inside the outer margin. If a feed uses a square crop, recompose in a square artboard with the brand, headline, and one useful detail. |
| [Sales one-sheet](../../assets/brand/hot-eats-one-sheet.svg) | US Letter with about a half-inch live margin. Editable headline, guest jobs, operator details, and closing action. Add an approved destination or sender's details when distributing it. Print one copy at 100% scale to check line wraps and margins. |

1. Duplicate the SVG master. Edit the labeled text groups in your vector editor and keep the brand marks as supplied. Confirm the accompanying caption, link, and descriptive text.
2. Export social artwork as a 1,200 × 630 sRGB PNG. Inspect it at feed size. Export a print copy at actual letter size using the vendor's specifications. For an emailed one-sheet, include the core copy and next action in the email body as well.
3. Check the final artwork at its actual display size. Review type substitutions, line breaks, margins, contrast, destination links, and permissions. Record the asset version and destination with the channel materials.

**Social description**  
Hot Eats. Make it easy to come in. A website kit for restaurants. A doorway frames three guest tasks: Menu, Hours, and Directions.

**One-sheet text**

Make it easy to come in. Hot Eats is a configurable website kit for independent restaurants and the web partners who build for them. Guests can browse dishes, prices, and availability, find hours and location details, then get directions, call, or follow the restaurant's ordering or booking link where offered.

Explore nine illustrative designs and select the pages your restaurant needs. Replace the examples with your own menu, hours, details, and photos. With local owner tools, preview a change to hours or menu availability before applying it. Your website setup controls how changes go live.

See the restaurant examples. Ask for a walkthrough of the guest experience.
