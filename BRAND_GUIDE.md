# Brand Guide — Widi Ginanjar
Reference doc for keeping colors, fonts, voice, and identity consistent across the website, documents (CV, decks, proposals), and any other external comms. Paste this into a new chat when starting a new document/deck, so Claude (or future-me) doesn't have to rediscover it each time.

## 1. Colors (official, from widiginanjar.com)
| Name | Hex | Use |
|---|---|---|
| Ink (primary text) | `#1C1F1B` | Body text, headings |
| Ink soft (secondary text) | `#565B54` | Captions, muted text |
| Accent (brand green) | `#2F6F5E` | Links, highlights, primary brand color |
| Accent soft | `#E7F0EB` | Light backgrounds, badges, tinted sections |
| Background | `#FAFAF7` | Page/slide background (light) |
| Paper (card background) | `#FFFFFF` | Cards, boxes on top of background |
| Rule (borders/dividers) | `#E1DED4` | Card borders, horizontal rules |

**Dark-mode extension** (used sparingly, title/closing slides only, see §4. Not on the website itself, since the site has no dark sections):
| Name | Hex | Use |
|---|---|---|
| Forest (dark bg) | `#1F3D33` | Dark slide backgrounds |
| Sage (light text on dark) | `#9FC8B8` | Secondary text on dark backgrounds |
| Cream (body text on dark) | `#F7F5EF` | Body text on dark backgrounds |

Only introduce a new color if the website's palette doesn't cover the need (like dark slide backgrounds). Keep new colors in the same family (muted greens/creams), not arbitrary additions. This includes status/severity colors (critical, done, pending, etc.), don't reach for red or amber, signal urgency through bold weight and wording instead.

## 2. Fonts
**Website (web fonts, safe because the browser loads them):**
- Serif / headings: `Source Serif 4`
- Sans / body: `Inter`
- Mono / labels, tags, code: `IBM Plex Mono`

**Documents (Word, PowerPoint, PDF) — use safe Office-installed fonts instead:**
- Serif / headings: `Cambria`
- Sans / body: `Calibri`

Reason: Source Serif 4 / Inter / IBM Plex Mono aren't guaranteed to be installed on whoever opens the document (e.g. a client's laptop), so PowerPoint/Word would silently substitute a random font and possibly break layout. Cambria and Calibri ship with every Office install and render identically everywhere. Never use the web fonts in a .docx/.pptx/.pdf deliverable.

## 3. Voice
See `WRITING_GUIDE.md` for full writing rules. Key ones that also apply to decks/documents, not just notes articles:
- **Never use em dashes or double-hyphen (`--`) as a substitute for them, in any document, deck, or chat response.** Use periods, commas, colons, or parentheses instead.
- Plain, direct phrasing over native-flavored idiom (see WRITING_GUIDE #2)
- Bold key phrases/sentences for skimmability, not entire paragraphs
- Never overstate a role, title, or relationship that hasn't been confirmed (e.g. don't write "leads X" when it's still a proposal, don't assume a claimed title/collaboration is more definite than it actually is)

## 3.5 Canonical Contact Block
Use this exact block wherever a document needs identity or contact info: cover pages, footers, closing signatures, email signatures. Update this section first if any of it changes, don't let individual documents drift from what's live on the site.
- **Name:** Widi Ginanjar
- **Tagline:** SEO & Growth Marketing Consultant
- **Website:** widiginanjar.com
- **Email:** rajnanig22@gmail.com
- **LinkedIn:** linkedin.com/in/widiginanjar
- **Location:** Bali, Indonesia

Place name + tagline + website + email together on a document's cover (so it's visible immediately), and repeat name + tagline + website in the closing signature. Don't invent alternate taglines or link to superseded profiles (e.g. old Notion portfolio links) once the live site supersedes them.

## 4. Deck/Document Design Guardrails (avoid the "AI deck" look)
These aren't stylistic nice-to-haves, they're the specific tells that make a deck or document read as generated rather than designed. Check every deliverable against this list before sending, but judgment beats mechanical compliance, if a rule below doesn't fit the specific piece, override it deliberately rather than following it blindly.

**Backgrounds**
- Full-bleed saturated dark background (like Forest) is reserved for title and closing slides only, maximum. Never use it on a content-heavy slide (findings, roadmap, comparisons), that's the single biggest "AI deck" tell.
- Content slides default to light (`Background` + `Paper` cards). Dark should feel like the exception, not the base.
- Never default to cream/beige (`F5F5DC`, `FAF0E6`, etc.) when no background is specified, use `Background` (`#FAFAF7`) or `Paper` (`#FFFFFF`).

**Structure**
- Never put an accent line or underline directly beneath a title. Never add a decorative color bar or accent stripe (header bar, vertical sidebar, edge stripe on a card). If a card needs separation, use a subtle shadow or tint, not an edge stripe.
- Don't repeat the identical layout on every slide (same grid of cards, same icon-in-circle pattern every time). Vary between cards, two-column, stat callouts, and timeline/process layouts across a deck.
- One dominant color per slide (60-70% weight), 1-2 supporting tones, one accent, never all colors given equal weight.

**Text**
- Left-align body text and lists. Center only titles.
- Bold titles need real size contrast against body (titles 26-36pt+, body 10-12pt), don't let them sit close in size.
- Every card needs breathing room between its label/title and its body text, don't let fixed box heights create a visible gap where text ends early. Size text boxes to content, not to a round number.

**Icons and shapes**
- Don't put every single item in a generic icon-in-circle. Vary between numbers, letters, or no icon at all across a deck.
- Rounded corners + drop shadow on every single box reads as templated. Mix in sharp corners or borderless cards for variety.
- Skip connector arrows between items when the sequence is already clear from numbering or labels, arrows between every step is a generative-flow-diagram tell.

**Symmetry**
- Rule-of-3 columns for everything is a recognizable pattern. Let content dictate the split, sometimes 2 items or an asymmetric 1-big-plus-3-small layout reads more intentional.
- Perfectly uniform spacing everywhere can look suspicious. Real design has small deliberate variation for hierarchy, not machine-perfect regularity.

**Content**
- No generic claims ("innovative solution," "boost efficiency") without a number or specific example backing it up. Specific data is both more convincing and harder to mistake for a template.
- No placeholder-looking content: suspiciously round numbers (100%, 10x), generic example names, anything that reads like a filled-in template field.
- No generic openers ("Di era digital yang serba cepat ini...") or stacked formal transitions ("selain itu", "lebih lanjut", "dengan demikian") back to back.
- Don't bold random words for "emphasis" without a clear reason that specific word carries the point.

**Before sending**
- Would this slide still make sense stripped of icons and colors, just the words? If the words are generic, the design is doing work the content should be doing.
- Zoom out and squint: does one slide look identical in shape to the slide before it? If yes, change the layout.
- 3-second test: if someone can tell it's AI-made in the first 3 seconds, it's usually because it's too uniform and symmetric, not because it's messy. Good human design has small intentional imperfection.

## 5. McKinsey-Style Conventions (structure, keep the brand palette)
Adopt the discipline of consulting-style decks and documents where it earns its place, but every color reference below maps to §1, never introduce new colors for this. These are habits of mind, not a checklist to tick off on every single deliverable, a short internal update doesn't need a storyline and an exhibit number.

- **Action titles.** The slide or section title states the takeaway, not the topic, when the content supports it. Not "Rencana" but "Perbaikan dasar bisa dikerjakan tim internal dalam 2 minggu tanpa biaya tambahan." Read all the titles in sequence, they should form one argument (the storyline).
- **MECE breakdowns.** Any framework, pillar list, or category split should be mutually exclusive and collectively exhaustive, no overlap, nothing missing.
- **Minimal color, one accent for the insight.** `Ink`/`Ink soft` as the neutral base across charts and tables, `Accent` used only to highlight the single most important bar, number, or row, not spread evenly for decoration.
- **Functional charts and tables, not decorative ones.** Horizontal bar, waterfall, 2x2 matrix, process flow, status table, chosen because the shape fits the data, not to look more "designed."
- **"So what" callout.** Dense sections benefit from one short line stating the insight directly ("Domain Rating 0,1 means zero authority, starting from zero"), use it where it adds clarity, not as a mandatory box on every section.
- **Source line + exhibit number.** Useful on longer, more formal data-heavy documents. Skip it on shorter or more casual pieces where it would feel like empty formality.
- **Strict grid alignment.** Every element aligns to the same margins and grid across all slides/pages, don't let alignment drift. This is separate from and compatible with the layout variation in §4, vary the layout type, not the grid discipline.

## 6. Word Document Toolkit: Proposals & Quotations
This is a toolkit, not a fixed skeleton. It's built from what worked in the Cothink proposal/quotation, but the actual best version of any given document depends on the client, the scope, and what needs emphasis, so treat every section below as available, not mandatory. Merge two sections when they're thin enough to share space, drop a section that doesn't apply, reorder if the story reads better differently, add something not listed here if the situation calls for it. Palette from §1, fonts from §2 (Cambria headings / Calibri body), guardrails from §4, McKinsey conventions from §5 apply wherever they fit.

**Header block**
Small caps eyebrow (`PREPARED FOR [CLIENT NAME]`), document title, a one-line subtitle naming the actual deliverable (not a generic label), prepared-by line from the canonical contact block (§3.5), and a validity/currency line if the quote has a shelf life.

**Executive summary + plain-terms callout**
One paragraph on the situation and the cost structure, in prose. Follow with a short `Accent soft` tinted callout that states the "so what" in plain language. Worth including on almost anything with a price attached, since it's the paragraph a busy client actually reads.

**Current state**
A two-column table (Area | Status) works well when there's a clear before-state to diagnose. Skip it if there's no real "current state" to describe, e.g. a brand-new engagement with nothing to audit yet. Status should read as a full sentence, specific rather than a red/amber label.

**Objectives & success criteria**
Bullets stated as outcomes, not tasks, closing with a concrete "Success looks like:" line. Useful whenever the client needs to know how they'll judge whether it worked, not needed for very short, transactional documents.

**Approach (pillars)**
Name a framework only if there's a real MECE structure to name, don't force a "Four Pillars" label onto something that's really just three sequential steps. State explicitly if the order is dependency-driven.

**Phase / pricing table**
The core of a quotation. Columns adapt to what's actually being split out, Pillar / Research & Recs / Applied By / Fee worked for Cothink because work was split between Widi and their team, a different engagement might just need Deliverable / Fee. Always end with a bold, right-aligned total row. Any caveat that changes scope or timing gets its own explicit `Note:` line rather than buried in a bullet.

**Timeline**
A When / What Happens table earns its place when there are real dependencies or waiting periods worth flagging (e.g. waiting on client's hosting access). For a fast, self-contained engagement, a single sentence on turnaround may say more than a table.

**Optional/recurring work**
Same table logic as the main phase table, framed as a package with a quarterly or monthly fee. Only needed if there's a genuine ongoing component being proposed.

**Terms & assumptions**
Bullets stating concrete conditions (payment split and timing, what has to be true for the estimate to hold), not boilerplate legal language. Nearly always worth including, cheap to add and prevents disputes later.

**Closing**
Canonical contact block (§3.5), no extra sign-off flourish needed.

**Table styling, when tables are used:**
Header row `Accent soft` background with bold `Ink` text. Alternate `Paper`/`Background` row shading on long tables, all `Paper` is fine on short ones. `Rule`-colored thin borders, never heavy black grid lines. Right-align purely numeric columns.

## 7. Where this has been applied so far
- Website (widiginanjar.com): source of truth for the light-mode palette, web fonts, and canonical contact info
- CV / cover letters (docx): Cambria + Calibri, ink/accent colors only, no dark sections
- Cothink proposal deck (pptx): full palette including dark-mode extension, Cambria + Calibri
- Cothink proposal & quotation (docx): Cambria + Calibri, ink/accent/accent-soft only, canonical contact block on cover and closing, source of the §6 toolkit
- TEB pitch deck (pptx): full palette including dark-mode extension, Cambria + Calibri, no em dashes anywhere in copy
- SAH audit/strategy deck (pptx): full palette, dark background limited to title slide only after content slides read as too "AI-generated" in dark green, Cambria + Calibri
