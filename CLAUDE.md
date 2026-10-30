# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

The source for **widiginanjar.com**: a static personal site served by GitHub Pages (custom domain in `CNAME`). No framework, no CMS, no JavaScript build step. Plain HTML and CSS, plus Python scripts that turn Markdown into pages.

- `/` homepage: name, two doors (Writing and Services), newest essays filled in automatically
- `/writing/` field notes and essays, **in Bahasa Indonesia**
- `/services/` SEO and digital marketing services, **in English**
- `/notes/` SEO and growth notes, in English

## How the build works

| Source | Script | Output |
|---|---|---|
| `writing/posts/*.md` | `scripts/build_writing.py` | `writing/*.html`, `writing/index.html`, the cards between the `WRITING:START` and `WRITING:END` markers in `index.html` |
| `notes/posts/*.md` | `scripts/build_notes.py` | `notes/*.html`, `notes/index.html` |
| all of the above + static pages | `scripts/build_site_index.py` | `sitemap.xml`, `llms.txt` |
| `notes/posts/*.md` without a cover | `scripts/make_note_covers.py` (fallback, run by hand, needs Playwright) | `notes/img/<slug>.jpg`, 1200x630 typographic cover |

GitHub Actions (`.github/workflows/build-writing.yml`, `build-notes.yml`) run these on push to `main` and commit the generated files.

Run locally:

```bash
pip install markdown pyyaml
python3 scripts/build_writing.py
python3 scripts/build_notes.py
python3 scripts/build_site_index.py
```

## Rules

- **Never edit generated files by hand**: `writing/*.html`, `notes/*.html`, the block between the `WRITING` markers in `index.html`, `sitemap.xml`, `llms.txt`. Change the Markdown source or the script instead, or the next build overwrites the edit.
- **Never use em dashes or double hyphens** in visible text, copy, or commit messages. Use periods, commas, colons, or parentheses.
- **Never overstate roles or claims.** Describe what Widi does, not titles. Every sentence on the site must be true today. See `BRAND_GUIDE.md` section 0.
- **Language:** site frame, services, and notes in English. Essays in Bahasa Indonesia; keep their titles in Indonesian everywhere.
- **Brand:** colors, fonts (IBM Plex Serif, Sans, Mono), and design guardrails are in `BRAND_GUIDE.md`. Follow its "avoid the AI look" rules: no icon-in-circle, no drop shadow on every card, no decorative accent bars.
- **Mobile first:** check every layout change at 360px and 390px wide with no horizontal scroll.
- **Note covers:** free Unsplash photos, 1200x630, in `notes/img/<slug>.jpg`, each listed in `notes/img/CREDITS.md`. No clear faces or brand logos.
- **Images:** essay photos go in `writing/img/`, 4:5 crop around 900px wide, under about 300 KB. Covers for cards and link previews are 1200x630.
- **SEO notes** follow `writing_guide.md`, including its six official tags.
- **Privacy:** don't name people from fieldwork without their consent. Never commit client data or credentials. API keys go in repository secrets.

## Frontmatter

Essay (`writing/posts/<slug>.md`):

```yaml
---
title: "..."
subtitle: "..."        # optional
description: "..."     # one line, under about 160 characters
tag: catatan lapangan
date: 2026-10-30
slug: ...
image: img/cover.jpg   # optional
note: "..."            # optional footer line
---
```

Inline photo: `![alt text](/writing/img/photo.jpg)` with the caption in *italics* on the next line.

Note (`notes/posts/<slug>.md`): `title`, `description`, `tag` (one of the six in `writing_guide.md`), `date`, `slug`, optional `sources` list.

## Workflow

- Work on a branch and open a pull request. Widi reviews and merges; merging to `main` publishes the site.
- Write clear commit messages that say what changed and why.
- Planned work lives in GitHub Issues and in the README roadmap.
