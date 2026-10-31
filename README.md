# widiginanjar.com

Personal website of Widi Ginanjar: research, sustainability, essays, and SEO consulting.

The site has two parts:

- **Writing** (`/writing/`): field notes and personal essays in Bahasa Indonesia.
- **Services** (`/services/`): SEO consulting for NGOs, hospitality brands, B2B firms, and AI startups, plus technical notes in `/notes/`.

It is a static site served by GitHub Pages on a custom domain (see `CNAME`). There is no CMS and no framework.

## How publishing works

Essays and notes are written in Markdown with a small YAML header. On every push, GitHub Actions runs a Python build script that turns them into HTML pages.

```
writing/posts/*.md  ->  scripts/build_writing.py  ->  writing/*.html
                                                  ->  writing/index.html
                                                  ->  index.html (newest 3 essays)
notes/posts/*.md    ->  scripts/build_notes.py    ->  notes/*.html
```

### Adding an essay

1. Put cover and inline photos in `writing/img/`.
2. Create `writing/posts/<slug>.md`:

   ```yaml
   ---
   title: "Essay title"
   subtitle: "Optional line under the title"
   description: "One line, under about 160 characters"
   tag: catatan lapangan
   date: 2026-10-30
   slug: essay-slug
   image: img/cover.jpg        # optional, 1200x630, used for cards and link previews
   ---
   ```

3. Inline photos: `![alt text](/writing/img/photo.jpg)` with the caption in *italics* on the next line.
4. Commit. The workflow rebuilds the pages and the homepage cards.

## Structure

| Path | What it is |
|---|---|
| `index.html` | Homepage: name, two sections (Writing and Services), newest essays |
| `services/` | Services overview and one page per client type |
| `writing/` | Essays (generated), sources in `writing/posts/`, images in `writing/img/` |
| `notes/` | SEO and growth notes (generated), sources in `notes/posts/` |
| `scripts/` | Build scripts |
| `.github/workflows/` | Build automation |
| `BRAND_GUIDE.md` | Colors, fonts, voice, and positioning rules |
| `writing_guide.md` | Writing rules for the SEO notes |
| `CLAUDE.md` | Instructions for Claude Code |

## Roadmap

About 100 hours of planned work, tracked in GitHub Issues:

| Feature | Issue | Estimate |
|---|---|---|
| Tags and search for essays and notes | #3 | 12 h |
| RSS feeds for Writing and Notes | #4 | 4 h |
| Bilingual metadata for Indonesian essays | #5 | 8 h |
| Search Console and GA4 dashboard | #6 | 20 h |
| Build checks and maintenance | #7 | 16 h |
| Rewrite the About page | #9 | 8 h |
| Image pipeline for photos and covers | #10 | 16 h |
| Related essays and archive by year | #11 | 8 h |
| Refresh service pages | #12 | 8 h |

## Working with Claude Code

This project is built with Claude Code as a coding assistant. `CLAUDE.md` describes the build system, conventions, and rules it follows. Changes go through branches and pull requests, and are reviewed before merging.

## Ownership

All content and code: Widi Ginanjar. All rights reserved.
