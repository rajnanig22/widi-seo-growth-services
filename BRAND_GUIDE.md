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

**Dark-mode extension** (used for deck title/closing slides, not on the website itself, since the site has no dark sections):
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

## 4. Where this has been applied so far
- Website (widiginanjar.com): source of truth for the light-mode palette, web fonts, and canonical contact info
- CV / cover letters (docx): Cambria + Calibri, ink/accent colors only, no dark sections
- Cothink proposal deck (pptx): full palette including dark-mode extension, Cambria + Calibri
- Cothink proposal & quotation (docx): Cambria + Calibri, ink/accent/accent-soft only, canonical contact block on cover and closing
- TEB pitch deck (pptx): full palette including dark-mode extension, Cambria + Calibri, no em dashes anywhere in copy
