#!/usr/bin/env python3
"""
Build script for the Writing section (separate from build_notes.py).

Converts markdown files in writing/posts/*.md into static HTML pages under
writing/*.html, and regenerates writing/index.html listing all essays.

Write each essay as plain markdown with YAML frontmatter:

---
title: "My Essay Title"
description: "One-line description, under ~160 chars."
tag: esai pribadi
date: 2019-07-28
slug: my-essay-title
note: "Optional small footer line, for example where it was first published."
subtitle: "Optional line shown under the title."
image: img/cover.jpg   # optional, 1200x630, used for link previews
---

Photos: upload them to writing/img/ and use ![alt text](/writing/img/photo.jpg)
with the caption as *italic text* on the very next line.

Then normal markdown body below the second `---`.

Run: python3 scripts/build_writing.py
(Also runs automatically via GitHub Actions on every push that touches
writing/posts/*.md, see .github/workflows/build-writing.yml)

This script never touches /notes/ or llms.txt.
"""

import os
import re
import glob
import json
import html
import math
import datetime

import yaml
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "writing", "posts")
OUTPUT_DIR = os.path.join(ROOT, "writing")
SITE_URL = "https://widiginanjar.com"
GA_ID = "G-XMWESDJT49"

# Indonesian month names, so the script does not depend on the server locale.
MONTHS_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]

# Shared <head> start (analytics, fonts). Placeholders use %%NAME%% tokens
# so the CSS braces do not need escaping.
HEAD_COMMON = """<!DOCTYPE html>
<html lang="id">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%%GA_ID%%"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '%%GA_ID%%');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#2F6F5E">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>&#127793;</text></svg>">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600;700&display=swap" rel="stylesheet"></noscript>
"""

CSS_COMMON = """  :root {
    --bg: #FAFAF7; --paper: #FFFFFF; --ink: #1C1F1B; --ink-soft: #565B54;
    --accent: #2F6F5E; --accent-soft: #E7F0EB; --rule: #E1DED4;
    --mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    --serif: 'IBM Plex Serif', Georgia, 'Times New Roman', serif;
    --sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
  * { box-sizing: border-box; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  a:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }
  .back-link { font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); text-decoration: none; display: inline-block; margin-bottom: 32px; }
  .back-link:hover { color: var(--accent); text-decoration: none; }
  .eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em; text-transform: lowercase; color: var(--accent); background: var(--accent-soft); display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 14px; }
"""

ARTICLE_TEMPLATE = HEAD_COMMON + """
<title>%%TITLE%% | Widi Ginanjar</title>
<meta name="description" content="%%DESCRIPTION%%">
<link rel="canonical" href="%%CANONICAL%%">

<meta property="og:type" content="article">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESCRIPTION%%">
<meta property="og:url" content="%%CANONICAL%%">
<meta property="og:image" content="%%OG_IMAGE%%">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="Widi Ginanjar">
<meta name="twitter:card" content="summary_large_image">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "image": "%%OG_IMAGE%%",
  "headline": %%TITLE_JSON%%,
  "inLanguage": "id",
  "author": { "@type": "Person", "name": "Widi Ginanjar", "url": "https://widiginanjar.com" },
  "mainEntityOfPage": "%%CANONICAL%%",
  "datePublished": "%%DATE%%",
  "description": %%DESCRIPTION_JSON%%
}
</script>

<style>
""" + CSS_COMMON + """  body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--sans); line-height: 1.7; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 680px; margin: 0 auto; padding: 56px 20px 64px; }
  h1 { font-family: var(--serif); font-weight: 600; font-size: clamp(24px, 6vw, 32px); line-height: 1.25; letter-spacing: -0.01em; margin: 0 0 10px; }
  .meta { font-size: 13px; color: var(--ink-soft); margin: 0 0 32px; }
  article p { font-size: 16.5px; margin: 0 0 1.1em; overflow-wrap: anywhere; }
  article h2 { font-family: var(--serif); font-size: 21px; line-height: 1.3; margin: 1.6em 0 0.6em; }
  article blockquote { margin: 0 0 1.1em; padding-left: 16px; border-left: 2px solid var(--accent); color: var(--ink-soft); }
  article blockquote p { margin: 0 0 0.7em; font-size: inherit; color: inherit; }
    article blockquote p { margin: 0 0 0.7em; font-size: inherit; color: inherit; }
  article strong { color: var(--ink); }
  article a { color: var(--ink); text-decoration: none; background: linear-gradient(transparent 58%, #CFE5DA 58%); padding: 0 1px; transition: background 0.15s ease; }
  article a:hover { background: #CFE5DA; text-decoration: none; }
  .subtitle { font-family: var(--serif); font-size: 17px; color: var(--ink-soft); margin: 0 0 10px; }
  .subtitle { font-family: var(--serif); font-size: 17px; color: var(--ink-soft); margin: 0 0 10px; }
  article img { display: block; width: 100%; height: auto; border-radius: 8px; margin: 1.6em 0 8px; }
  article p:has(> img) { margin-bottom: 1.6em; }
  article p:has(> img) em { display: block; font-size: 13px; line-height: 1.5; color: var(--ink-soft); text-align: center; }
  .note { margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--rule); font-size: 13px; color: var(--ink-soft); }
  @media (min-width: 720px) { .wrap { padding: 56px 32px 80px; } }
  @media (max-width: 640px) { article p { font-size: 16px; } }
</style>
</head>
<body>

<div class="wrap">
  <a class="back-link" href="/writing/">&larr; Writing</a>
  <span class="eyebrow">%%TAG%%</span>
  <h1>%%TITLE%%</h1>
%%SUBTITLE_BLOCK%%  <p class="meta">Widi Ginanjar &middot; %%DATE_DISPLAY%% &middot; %%READ_TIME%%</p>

  <article>
%%CONTENT%%
  </article>
%%NOTE_BLOCK%%
</div>

</body>
</html>
"""

INDEX_TEMPLATE = HEAD_COMMON + """
<title>Writing | Widi Ginanjar</title>
<meta name="description" content="Esai pribadi dan catatan lapangan dari Widi Ginanjar, dalam Bahasa Indonesia.">
<link rel="canonical" href="%%SITE_URL%%/writing/">

<meta property="og:type" content="website">
<meta property="og:title" content="Writing | Widi Ginanjar">
<meta property="og:description" content="Esai pribadi dan catatan lapangan, dalam Bahasa Indonesia.">
<meta property="og:url" content="%%SITE_URL%%/writing/">
<meta property="og:image" content="%%SITE_URL%%/og-image.png">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="Widi Ginanjar">
<meta name="twitter:card" content="summary_large_image">

<style>
""" + CSS_COMMON + """  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.6; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 760px; margin: 0 auto; padding: 56px 32px 80px; }
  h1 { font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 5vw, 36px); line-height: 1.2; letter-spacing: -0.01em; margin: 0 0 12px; }
  .subhead { font-size: 15px; color: var(--ink-soft); margin: 0 0 36px; max-width: 52ch; }
  .article-list { display: flex; flex-direction: column; gap: 14px; margin-bottom: 36px; }
  .article-card {
    background: var(--paper); border: 1px solid var(--rule); border-radius: 10px;
    padding: 20px 22px; display: block; color: inherit; text-decoration: none;
    transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  }
  .article-card:hover { border-color: var(--accent); transform: translateY(-1px); box-shadow: 0 4px 14px rgba(47, 111, 94, 0.08); text-decoration: none; }
  .article-card-top { display: flex; align-items: center; justify-content: space-between; }
  .article-card .tag { font-family: var(--mono); font-size: 10.5px; color: var(--accent); text-transform: lowercase; letter-spacing: 0.02em; }
  .article-card .go-arrow { font-family: var(--mono); font-size: 15px; color: var(--ink-soft); transition: color 0.15s ease, transform 0.15s ease; }
  .article-card:hover .go-arrow { color: var(--accent); transform: translateX(2px); }
  .article-card h2 { font-family: var(--serif); font-size: 18px; font-weight: 600; margin: 8px 0 6px; color: var(--ink); }
  .article-card p { font-size: 13.5px; color: var(--ink-soft); margin: 0; }
  .article-card .card-meta { font-family: var(--mono); font-size: 11px; color: var(--ink-soft); margin-top: 10px; opacity: 0.8; }
  @media (prefers-reduced-motion: reduce) { .article-card { transition: none !important; } .article-card:hover { transform: none; } }

  @media (max-width: 640px) {
    .wrap { padding: 40px 20px 60px; }
    h1 { font-size: clamp(24px, 7vw, 30px); }
    .subhead { font-size: 13px; margin-bottom: 28px; }
    .article-card { padding: 16px 18px; }
    .article-card h2 { font-size: 16px; }
    .article-card p { font-size: 12.5px; }
    .article-card .card-meta { font-size: 10px; }
  }
</style>
</head>
<body>

<div class="wrap">
  <a class="back-link" href="/">&larr; widiginanjar.com</a>
  <span class="eyebrow">writing</span>
  <h1>Writing</h1>
  <p class="subhead">Esai pribadi dan catatan lapangan tentang manusia dan komunitas, dalam Bahasa Indonesia. Ancora imparo.</p>

  <div class="article-list">
%%CARDS%%
  </div>
</div>

</body>
</html>
"""

CARD_TEMPLATE = """    <a class="article-card" href="/writing/%%SLUG%%.html">
      <div class="article-card-top">
        <span class="tag">%%TAG%%</span>
        <span class="go-arrow">&rarr;</span>
      </div>
      <h2>%%TITLE%%</h2>
      <p>%%DESCRIPTION%%</p>
      <p class="card-meta">%%DATE_DISPLAY%% &middot; %%READ_TIME%%</p>
    </a>"""


def fill(template, values):
    """Replace %%KEY%% tokens with values (plain string replace, no escaping needed)."""
    for key, value in values.items():
        template = template.replace("%%" + key + "%%", value)
    return template


def load_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
        if not match:
            print(f"WARNING: {path} has no valid frontmatter, skipping")
            continue
        front = yaml.safe_load(match.group(1)) or {}
        front["body_md"] = match.group(2)
        front["slug"] = front.get("slug") or os.path.splitext(os.path.basename(path))[0]
        posts.append(front)
    posts.sort(key=lambda p: str(p.get("date", "")), reverse=True)
    return posts


def format_date(date_value):
    """'2019-07-28' -> '28 Juli 2019'. Falls back to the raw string if unparseable."""
    text = str(date_value)
    try:
        d = datetime.datetime.strptime(text[:10], "%Y-%m-%d")
        return f"{d.day} {MONTHS_ID[d.month - 1]} {d.year}"
    except ValueError:
        return text


def reading_time(text):
    """About 200 words per minute, minimum 1 minute."""
    words = re.findall(r"\w+", text)
    return f"{max(1, math.ceil(len(words) / 200))} menit baca"


def build_article(post):
    title_raw = str(post.get("title", "Tanpa judul"))
    description_raw = str(post.get("description", ""))
    slug = post["slug"]
    canonical = f"{SITE_URL}/writing/{slug}.html"
    date = str(post.get("date", ""))[:10]

    body_html = markdown.markdown(post["body_md"], extensions=["extra", "sane_lists"])
    # Indent the generated body so the page source stays readable.
    body_html = "\n".join("    " + line if line else line for line in body_html.splitlines())

    note = post.get("note")
    note_block = f'\n  <p class="note">{html.escape(str(note), quote=True)}</p>' if note else ""

    subtitle = post.get("subtitle")
    subtitle_block = f'  <p class="subtitle">{html.escape(str(subtitle), quote=True)}</p>\n' if subtitle else ""

    image = str(post.get("image") or "").strip()
    if image.startswith("http"):
        og_image = image
    elif image.startswith("/"):
        og_image = SITE_URL + image
    elif image:
        og_image = f"{SITE_URL}/writing/{image}"
    else:
        og_image = f"{SITE_URL}/og-image.png"

    post["_date_display"] = format_date(date)
    post["_read_time"] = reading_time(post["body_md"])

    page = fill(ARTICLE_TEMPLATE, {
        "GA_ID": GA_ID,
        "SITE_URL": SITE_URL,
        "TITLE": html.escape(title_raw, quote=True),
        "TITLE_JSON": json.dumps(title_raw, ensure_ascii=False),
        "DESCRIPTION": html.escape(description_raw, quote=True),
        "DESCRIPTION_JSON": json.dumps(description_raw, ensure_ascii=False),
        "CANONICAL": canonical,
        "DATE": date,
        "DATE_DISPLAY": post["_date_display"],
        "READ_TIME": post["_read_time"],
        "TAG": html.escape(str(post.get("tag", "tulisan"))),
        "CONTENT": body_html,
        "NOTE_BLOCK": note_block,
        "SUBTITLE_BLOCK": subtitle_block,
        "OG_IMAGE": og_image,
    })
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Built {out_path}")


def build_index(posts):
    cards = "\n\n".join(
        fill(CARD_TEMPLATE, {
            "SLUG": p["slug"],
            "TAG": html.escape(str(p.get("tag", "tulisan"))),
            "TITLE": html.escape(str(p.get("title", "")), quote=True),
            "DESCRIPTION": html.escape(str(p.get("description", "")), quote=True),
            "DATE_DISPLAY": p["_date_display"],
            "READ_TIME": p["_read_time"],
        })
        for p in posts
    )
    page = fill(INDEX_TEMPLATE, {"GA_ID": GA_ID, "SITE_URL": SITE_URL, "CARDS": cards})
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Built {out_path}")


def main():
    posts = load_posts()
    if not posts:
        print("No posts found in writing/posts/, nothing to build.")
        return
    for post in posts:
        build_article(post)
    build_index(posts)


if __name__ == "__main__":
    main()
