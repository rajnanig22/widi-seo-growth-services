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
seo_title: "Optional title for Google results, with the words people search for"
republished: true   # optional, for essays first published elsewhere: shows "Pertama terbit <date>"
title_en: "Optional English translation of the title (llms.txt and search data only)"
description_en: "Optional English summary, shown on the English homepage card and in llms.txt"
---

Photos: upload them to writing/img/ and use ![alt text](/writing/img/photo.jpg)
with the caption as *italic text* on the very next line.

Then normal markdown body below the second `---`.

Run: python3 scripts/build_writing.py
(Also runs automatically via GitHub Actions on every push that touches
writing/posts/*.md, see .github/workflows/build-writing.yml)

This script never touches /notes/ or llms.txt. It also refreshes the
"Tulisan terbaru" block on the homepage (index.html), between the
WRITING:START and WRITING:END markers, with the 3 newest essays.
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
  .back-link { font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); text-decoration: none; display: block; width: fit-content; margin-bottom: 32px; }
  .back-link:hover { color: var(--accent); text-decoration: none; }
  .eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em; text-transform: lowercase; color: var(--accent); background: var(--accent-soft); display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 14px; }  .navwrap { max-width: 1520px; margin: 0 auto; padding: 0 clamp(20px, 5vw, 80px); }
  nav.top { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; border-bottom: 1px solid var(--rule); flex-wrap: wrap; }
  .nav-home { font-family: var(--mono); font-size: 13px; color: var(--ink); letter-spacing: 0.02em; text-decoration: none; }
  .nav-links { display: flex; gap: 28px; flex-wrap: wrap; }
  .nav-links a { font-size: 15px; font-weight: 600; color: var(--ink); border-bottom: 2px solid transparent; padding-bottom: 3px; text-decoration: none; }
  .nav-links a:hover, .nav-home:hover { color: var(--accent); text-decoration: none; }
  .nav-links a:hover { border-bottom-color: var(--accent); }
  .site-foot { background: #16302A; color: rgba(255,255,255,0.75); }
  .site-foot-in { max-width: 1520px; margin: 0 auto; padding: 28px clamp(20px, 5vw, 80px) 32px; display: flex; justify-content: space-between; align-items: center; gap: 12px 32px; flex-wrap: wrap; font-size: 13.5px; }
  .site-foot-in p { margin: 0; color: rgba(255,255,255,0.75); font-size: 13.5px; }
  .site-foot .links { display: flex; gap: 22px; }
  .site-foot .links a { display: inline-flex; align-items: center; justify-content: center; min-width: 32px; min-height: 32px; color: #CFE5DA; }
  .site-foot .links a:hover { color: #FFFFFF; text-decoration: none; }
  @media (max-width: 760px) { .nav-home { display: none; } nav.top { justify-content: flex-end; } }
  @media (max-width: 420px) { .nav-links { gap: 14px; } .nav-links a { font-size: 13px; } }
  /* shared nav: name on the left on every screen, lighter links */
  .nav-home { font-family: var(--serif) !important; font-weight: 700; font-size: 17px !important; letter-spacing: -0.01em !important; color: var(--ink); display: inline !important; text-decoration: none; }
  nav.top .nav-links { gap: 24px; }
  nav.top .nav-links a { font-size: 14.5px; font-weight: 500; }
  @media (max-width: 820px) { nav.top { justify-content: space-between !important; flex-wrap: nowrap !important; } }
  @media (max-width: 420px) { .nav-home { font-size: 15px !important; } nav.top .nav-links { gap: 12px !important; } nav.top .nav-links a { font-size: 13px !important; } }
"""

NAV = """<div class="navwrap">
  <nav class="top" aria-label="Main">
    <a class="nav-home" href="/">Widi Ginanjar</a>
    <div class="nav-links">
      <a href="/writing/">Essays</a>
      <a href="/about.html">About</a>
      <a href="/services/">SEO Consulting</a>
    </div>
  </nav>
</div>
"""

FOOTER = """<div class="site-foot">
  <div class="site-foot-in">
    <p>&copy; 2026 Widi Ginanjar</p>
    <div class="links">
      <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{'method':'email','location':'site_footer'});" aria-label="Email" title="Email"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="m22 6-10 7L2 6"/></svg></a>
        <a href="https://linkedin.com/in/widiginanjar" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn"><svg width="20" height="20" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a>
        <a href="https://www.instagram.com/wdwynson/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" title="Instagram"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.6" fill="currentColor"/></svg></a>
    </div>
  </div>
</div>
"""

ARTICLE_TEMPLATE = HEAD_COMMON + """
<title>%%SEO_TITLE%% | Widi Ginanjar</title>
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
  "headline": %%TITLE_JSON%%,%%ALT_HEADLINE%%
  "inLanguage": "id",
  "author": { "@type": "Person", "name": "Widi Ginanjar", "url": "https://widiginanjar.com" },
  "mainEntityOfPage": "%%CANONICAL%%",
  "datePublished": "%%DATE%%",
  "dateModified": "%%DATE%%",
  "publisher": { "@type": "Person", "name": "Widi Ginanjar", "url": "https://widiginanjar.com" },
  "description": %%DESCRIPTION_JSON%%
}
</script>

<style>
""" + CSS_COMMON + """  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.7; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1520px; margin: 0 auto; padding: 0 clamp(20px, 5vw, 80px); }
  .back-link { margin: 32px 0 24px; }
  .art-hero { display: grid; grid-template-columns: 1fr minmax(0, 0.8fr); gap: 56px; align-items: center; padding-bottom: 48px; border-bottom: 1px solid var(--rule); }
  .art-hero.no-cover { grid-template-columns: 1fr; }
  .art-hero .cover { display: block; width: 100%; height: auto; aspect-ratio: 1200 / 630; object-fit: cover; border-radius: 12px; margin: 0; }
  .art-body { max-width: 42em; padding: 48px 0 72px; }
  h1 { font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 3.6vw, 42px); line-height: 1.15; letter-spacing: -0.01em; margin: 0 0 12px; }
  .meta { font-size: 13px; color: var(--ink-soft); margin: 0; }
  @media (max-width: 760px) { .art-hero { grid-template-columns: 1fr; gap: 24px; padding-bottom: 32px; } .art-hero .cover { order: -1; } .art-body { padding: 32px 0 48px; } }
  article p { font-size: 16.5px; margin: 0 0 1.1em; overflow-wrap: anywhere; }
  article h2 { font-family: var(--serif); font-size: 21px; line-height: 1.3; margin: 1.6em 0 0.6em; }
  article blockquote { margin: 0 0 1.1em; padding-left: 16px; border-left: 2px solid var(--accent); color: var(--ink-soft); }
  article blockquote p { margin: 0 0 0.7em; font-size: inherit; color: inherit; }
    article blockquote p { margin: 0 0 0.7em; font-size: inherit; color: inherit; }
  article strong { color: var(--ink); }
    article a { color: var(--ink); text-decoration: underline; text-decoration-color: var(--accent); text-decoration-thickness: 1.5px; text-underline-offset: 3px; background: linear-gradient(transparent 58%, #CFE5DA 58%); padding: 0 1px; transition: background 0.15s ease; }
  article a:hover { background: #CFE5DA; text-decoration-thickness: 2px; }
  .subtitle { font-family: var(--serif); font-size: 17px; color: var(--ink-soft); margin: 0 0 10px; }
  .subtitle { font-family: var(--serif); font-size: 17px; color: var(--ink-soft); margin: 0 0 10px; }
  article img { display: block; width: 100%; height: auto; border-radius: 8px; margin: 1.6em 0 8px; }
  article p:has(> img) { margin-bottom: 1.6em; }
  article p:has(> img) em { display: block; font-size: 13px; line-height: 1.5; color: var(--ink-soft); text-align: center; }
  .note { margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--rule); font-size: 13px; color: var(--ink-soft); }
  @media (max-width: 640px) { article p { font-size: 16px; } }
</style>
</head>
<body>

%%NAV%%
<div class="wrap">
  <a class="back-link" href="/writing/">&larr; Essays</a>
  <header class="art-hero%%HERO_CLASS%%">
    <div>
      <span class="eyebrow">%%TAG%%</span>
      <h1>%%TITLE%%</h1>
%%SUBTITLE_BLOCK%%      <p class="meta">Widi Ginanjar &middot; %%DATE_DISPLAY%% &middot; %%READ_TIME%%</p>
    </div>
%%COVER_BLOCK%%  </header>

  <div class="art-body">
  <article>
%%CONTENT%%
  </article>
%%NOTE_BLOCK%%
  </div>
</div>

%%FOOTER%%
</body>
</html>
"""

INDEX_TEMPLATE = HEAD_COMMON + """
<title>Essays | Widi Ginanjar</title>
<meta name="description" content="Esai pribadi dan catatan lapangan dari Widi Ginanjar, dalam Bahasa Indonesia.">
<link rel="canonical" href="%%SITE_URL%%/writing/">

<meta property="og:type" content="website">
<meta property="og:title" content="Essays | Widi Ginanjar">
<meta property="og:description" content="Esai pribadi dan catatan lapangan, dalam Bahasa Indonesia.">
<meta property="og:url" content="%%SITE_URL%%/writing/">
<meta property="og:image" content="%%SITE_URL%%/og-home.jpg">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="Widi Ginanjar">
<meta name="twitter:card" content="summary_large_image">

<style>
""" + CSS_COMMON + """  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.6; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1520px; margin: 0 auto; padding: 48px clamp(20px, 5vw, 80px) 72px; }
  h1 { font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 5vw, 36px); line-height: 1.2; letter-spacing: -0.01em; margin: 0 0 12px; }
  .subhead { font-size: 15px; color: var(--ink-soft); margin: 0 0 36px; max-width: 52ch; }
  .article-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin-bottom: 36px; }
  @media (max-width: 1000px) { .article-list { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 640px) { .article-list { grid-template-columns: 1fr; } }
  .article-card {
    background: var(--paper); border: 1px solid var(--rule); border-radius: 10px;
    display: flex; flex-direction: column; overflow: hidden; color: inherit; text-decoration: none;
    transition: border-color 0.15s ease;
  }
  .article-card:hover { border-color: var(--accent); text-decoration: none; }
  .article-card .thumb { display: block; background-size: cover; background-position: center; aspect-ratio: 1200 / 630; background-color: var(--accent-soft); }
  .article-card .thumb.empty { display: flex; align-items: center; justify-content: center; color: var(--accent); font-size: 22px; }
  .article-card .card-body { display: flex; flex-direction: column; flex: 1; padding: 18px 20px 20px; min-width: 0; }
  .article-card .card-meta { margin-top: auto !important; padding-top: 14px; }
  .article-card-top { display: flex; align-items: center; justify-content: space-between; }
  .article-card .tag { font-family: var(--mono); font-size: 10.5px; color: var(--accent); text-transform: lowercase; letter-spacing: 0.02em; }
  .article-card .go-arrow { font-family: var(--mono); font-size: 15px; color: var(--ink-soft); transition: color 0.15s ease, transform 0.15s ease; }
  .article-card:hover .go-arrow { color: var(--accent); transform: translateX(2px); }
  .article-card h2 { font-family: var(--serif); font-size: 18px; font-weight: 600; margin: 8px 0 6px; color: var(--ink); }
  .article-card p { font-size: 13.5px; color: var(--ink-soft); margin: 0; }
  .article-card .card-meta { font-family: var(--mono); font-size: 11px; color: var(--ink-soft); margin-top: 10px; opacity: 0.8; }
  @media (prefers-reduced-motion: reduce) { .article-card { transition: none !important; } }

  @media (max-width: 640px) {
    .wrap { padding: 40px 20px 60px; }
    h1 { font-size: clamp(24px, 7vw, 30px); }
    .subhead { font-size: 13px; margin-bottom: 28px; }
    .article-card .card-body { padding: 16px 18px; }
    .article-card h2 { font-size: 16px; }
    .article-card p { font-size: 12.5px; }
    .article-card .card-meta { font-size: 10px; }
  }
</style>
</head>
<body>

%%NAV%%
<div class="wrap">
  <span class="eyebrow">essays</span>
  <h1>Essays</h1>
  <p class="subhead">Esai pribadi dan catatan lapangan tentang manusia dan komunitas, dalam Bahasa Indonesia.</p>

  <div class="article-list">
%%CARDS%%
  </div>
</div>

%%FOOTER%%
</body>
</html>
"""

CARD_TEMPLATE = """    <a class="article-card" href="/writing/%%SLUG%%.html">
      %%THUMB%%
      <div class="card-body">
        <div class="article-card-top">
          <span class="tag">%%TAG%%</span>
          <span class="go-arrow">&rarr;</span>
        </div>
        <h2>%%TITLE%%</h2>
        <p>%%DESCRIPTION%%</p>
        <p class="card-meta">%%DATE_DISPLAY%% &middot; %%READ_TIME%%</p>
      </div>
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
    subtitle_block = f'      <p class="subtitle">{html.escape(str(subtitle), quote=True)}</p>\n' if subtitle else ""

    image = str(post.get("image") or "").strip()
    if image.startswith("http"):
        og_image = image
    elif image.startswith("/"):
        og_image = SITE_URL + image
    elif image:
        og_image = f"{SITE_URL}/writing/{image}"
    else:
        og_image = f"{SITE_URL}/og-home.jpg"
    cover_src = og_image[len(SITE_URL):] if image else ""
    cover_block = f'    <img class="cover" src="{cover_src}" alt="" width="1200" height="630">\n' if cover_src else ""

    post["_date_display"] = format_date(date)
    if post.get("republished"):
        # Older essays moved here from another blog keep their real date, labelled.
        post["_date_display"] = "Pertama terbit " + post["_date_display"]
    post["_read_time"] = reading_time(post["body_md"])

    page = fill(ARTICLE_TEMPLATE, {
        "GA_ID": GA_ID,
        "SITE_URL": SITE_URL,
        "TITLE": html.escape(title_raw, quote=True),
        "TITLE_JSON": json.dumps(title_raw, ensure_ascii=False),
        # Search results can use a plainer title than the essay's own title.
        "ALT_HEADLINE": (f'\n  "alternativeHeadline": {json.dumps(str(post["title_en"]), ensure_ascii=False)},' if post.get("title_en") else ""),
        "SEO_TITLE": html.escape(str(post.get("seo_title") or title_raw), quote=True),
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
        "NAV": NAV,
        "FOOTER": FOOTER,
        "COVER_BLOCK": cover_block,
        "HERO_CLASS": "" if cover_block else " no-cover",
    })
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Built {out_path}")


HOME_CARD_TEMPLATE = """        <a class="w-card" href="/writing/%%SLUG%%.html" onclick="gtag('event','writing_click',{'location':'homepage_card'});">
          %%THUMB%%
          <span class="w-body">
            <span class="tag">%%TAG%%</span>
            <h3 lang="id">%%TITLE%%</h3>
            <p lang="%%DESC_LANG%%">%%DESCRIPTION%%</p>
            <span class="w-meta">%%DATE_DISPLAY%% &middot; %%READ_TIME%% &middot; in Bahasa Indonesia</span>
          </span>
        </a>"""


def thumb_html(post):
    """Cover photo for a homepage card, or a quiet placeholder when the essay has none."""
    image = str(post.get("image") or "").strip()
    if not image:
        return '<span class="thumb empty" aria-hidden="true">&#10086;</span>'
    if not (image.startswith("/") or image.startswith("http")):
        image = "/writing/" + image
    safe = html.escape(image, quote=True)
    return f'<span class="thumb" style="background-image:url({safe})" aria-hidden="true"></span>'


def date_en(date_value):
    """'2026-10-30' -> '30 Oct 2026' for the English homepage."""
    text = str(date_value)
    try:
        return datetime.datetime.strptime(text[:10], "%Y-%m-%d").strftime("%-d %b %Y")
    except ValueError:
        return text


def update_homepage(posts, limit=3):
    """Fill the block between the WRITING markers in /index.html with the newest essays."""
    path = os.path.join(ROOT, "index.html")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        page = f.read()
    pattern = re.compile(r"(<!-- WRITING:START[^>]*-->\n).*?(<!-- WRITING:END -->)", re.DOTALL)
    if not pattern.search(page):
        print("Homepage has no WRITING markers, skipping homepage update")
        return
    cards = "\n".join(
        fill(HOME_CARD_TEMPLATE, {
            "SLUG": p["slug"],
            "THUMB": thumb_html(p),
            "TAG": html.escape(str(p.get("tag", "tulisan"))),
            "TITLE": html.escape(str(p.get("title", "")), quote=True),
            "DESCRIPTION": html.escape(str(p.get("description_en") or p.get("description", "")), quote=True),
            "DESC_LANG": "en" if p.get("description_en") else "id",
            "DATE_DISPLAY": ("First published " if p.get("republished") else "") + date_en(p.get("date", "")),
            "READ_TIME": p["_read_time"].replace("menit baca", "min read"),
        })
        for p in posts[:limit]
    )
    page = pattern.sub(lambda m: m.group(1) + cards + "\n" + m.group(2), page)
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Updated {path}")


def build_index(posts):
    cards = "\n\n".join(
        fill(CARD_TEMPLATE, {
            "SLUG": p["slug"],
            "THUMB": thumb_html(p),
            "TAG": html.escape(str(p.get("tag", "tulisan"))),
            "TITLE": html.escape(str(p.get("title", "")), quote=True),
            "DESCRIPTION": html.escape(str(p.get("description", "")), quote=True),
            "DATE_DISPLAY": p["_date_display"],
            "READ_TIME": p["_read_time"],
        })
        for p in posts
    )
    page = fill(INDEX_TEMPLATE, {"GA_ID": GA_ID, "SITE_URL": SITE_URL, "CARDS": cards, "NAV": NAV, "FOOTER": FOOTER})
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
    update_homepage(posts)


if __name__ == "__main__":
    main()
