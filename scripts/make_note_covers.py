#!/usr/bin/env python3
"""
Makes a 1200x630 cover for every SEO note that does not have one yet.

Covers are typographic (no stock photos): the note's category, its title in
IBM Plex Serif, and the site name, on a colour that depends on the category.
They are used as card images on /notes/ and as link previews (og:image).

Output: notes/img/<slug>.jpg. Existing covers are left alone, so a cover can be
replaced by hand. Delete a cover to have it regenerated.

Needs Playwright for Python:
    pip install playwright pyyaml && python3 -m playwright install chromium
Run:
    python3 scripts/make_note_covers.py

Fonts load from Google Fonts. To render offline, set PLEX_FONT_DIR to a folder
with the @fontsource woff2 files (ibm-plex-serif-latin-600-normal.woff2 and
ibm-plex-mono-latin-500-normal.woff2).
"""

import os
import re
import glob
import html
import base64

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "notes", "posts")
IMG_DIR = os.path.join(ROOT, "notes", "img")

# Category -> (label, background, text colour, small text colour)
STYLES = {
    "practice notes": ("practice notes", "#2F6F5E", "#FFFFFF", "#CFE5DA"),
    "mission-driven": ("mission-driven & ngo", "#E7F0EB", "#1C1F1B", "#2F6F5E"),
    "ngo": ("mission-driven & ngo", "#E7F0EB", "#1C1F1B", "#2F6F5E"),
    "ai search": ("ai & search", "#1C1F1B", "#FAFAF7", "#9CC7B5"),
    "ai & tech": ("ai & search", "#1C1F1B", "#FAFAF7", "#9CC7B5"),
}
DEFAULT_STYLE = ("seo notes", "#FAFAF7", "#1C1F1B", "#2F6F5E")


def font_faces():
    font_dir = os.environ.get("PLEX_FONT_DIR")
    if not font_dir:
        return ('<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500'
                '&family=IBM+Plex+Serif:wght@600&display=block" rel="stylesheet">')
    def data_url(name):
        with open(os.path.join(font_dir, name), "rb") as f:
            return "data:font/woff2;base64," + base64.b64encode(f.read()).decode()
    serif = data_url("ibm-plex-serif-latin-600-normal.woff2")
    mono = data_url("ibm-plex-mono-latin-500-normal.woff2")
    return ("<style>"
            f"@font-face{{font-family:'IBM Plex Serif';font-weight:600;src:url('{serif}')}}"
            f"@font-face{{font-family:'IBM Plex Mono';font-weight:500;src:url('{mono}')}}"
            "</style>")


def cover_html(title, tag):
    label, bg, ink, soft = STYLES.get(str(tag).lower(), DEFAULT_STYLE)
    size = 64 if len(title) <= 60 else 54 if len(title) <= 85 else 46
    return f"""<!doctype html><html><head><meta charset="utf-8">{font_faces()}
<style>
  html,body{{margin:0}}
  .c{{width:1200px;height:630px;box-sizing:border-box;padding:72px 80px;background:{bg};color:{ink};
      display:flex;flex-direction:column;justify-content:space-between}}
  .top,.bottom{{font-family:'IBM Plex Mono',monospace;font-weight:500;font-size:24px;letter-spacing:.04em;color:{soft}}}
  h1{{font-family:'IBM Plex Serif',Georgia,serif;font-weight:600;font-size:{size}px;line-height:1.15;
      letter-spacing:-.01em;margin:0;max-width:980px}}
</style></head><body><div class="c">
  <div class="top">seo notes &middot; {html.escape(label)}</div>
  <h1>{html.escape(title)}</h1>
  <div class="bottom">widiginanjar.com</div>
</div></body></html>"""


def load_notes():
    notes = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
        if not m:
            continue
        front = yaml.safe_load(m.group(1)) or {}
        front["slug"] = front.get("slug") or os.path.splitext(os.path.basename(path))[0]
        notes.append(front)
    return notes


def main():
    from playwright.sync_api import sync_playwright

    os.makedirs(IMG_DIR, exist_ok=True)
    todo = [n for n in load_notes() if not os.path.exists(os.path.join(IMG_DIR, n["slug"] + ".jpg"))]
    if not todo:
        print("All notes already have covers")
        return
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        for n in todo:
            page.set_content(cover_html(str(n.get("title", "")), n.get("tag", "")), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            out = os.path.join(IMG_DIR, n["slug"] + ".jpg")
            page.screenshot(path=out, type="jpeg", quality=82)
            print(f"Made {out}")
        browser.close()


if __name__ == "__main__":
    main()
