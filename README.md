# widiginanjar.com

Personal website of Widi Ginanjar: research, sustainability, and digital marketing.

The site has two parts:

- **Writing** (`/writing/`): field notes and personal essays in Bahasa Indonesia.
- **Services** (`/services/`): SEO and digital marketing for NGOs, hospitality brands, B2B firms, and AI startups, plus technical notes in `/notes/`.

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

## Ownership

All content and code: Widi Ginanjar. All rights reserved.
