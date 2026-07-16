#!/usr/bin/env python3
"""
Build script: converts markdown files in notes/posts/*.md into fully
static, styled HTML pages under notes/*.html, and regenerates
notes/index.html listing all posts.

Write your posts as plain markdown with YAML frontmatter, like:

---
title: My Post Title
description: One-line SEO description, under ~160 chars.
tag: ai search
date: 2026-07-16
slug: my-post-title
sources:
  - title: "Some Source"
    url: "https://example.com/source"
    publisher: "Example Publisher"
---

Then normal markdown body below the second `---`.

Run: python3 scripts/build_notes.py
(This also runs automatically via GitHub Actions on every push that
touches notes/posts/*.md -- see .github/workflows/build-notes.yml)
"""

import os
import re
import glob
import json
import html
import yaml
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "notes", "posts")
OUTPUT_DIR = os.path.join(ROOT, "notes")
SITE_URL = "https://widiginanjar.com"
GA_ID = "G-XMWESDJT49"

ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_id}');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#2F6F5E">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>&#127793;</text></svg>">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&family=Source+Serif+4:wght@600;700&display=swap" rel="stylesheet">

<title>{title} | Widi Ginanjar</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Widi Ginanjar">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {title_json},
  "author": {{ "@type": "Person", "name": "Widi Ginanjar" }},
  "publisher": {{ "@type": "Person", "name": "Widi Ginanjar" }},
  "mainEntityOfPage": "{canonical}",
  "datePublished": "{date}",
  "description": {description_json}
}}
</script>

<style>
  :root {{
    --bg: #FAFAF7;
    --paper: #FFFFFF;
    --ink: #1C1F1B;
    --ink-soft: #565B54;
    --accent: #2F6F5E;
    --accent-soft: #E7F0EB;
    --rule: #E1DED4;
    --mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: var(--sans);
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }}
  a {{ color: var(--accent); }}
  a:hover {{ text-decoration: underline; }}
  .wrap {{ max-width: 680px; margin: 0 auto; padding: 56px 24px 80px; }}
  .back-link {{
    font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft);
    text-decoration: none; display: inline-block; margin-bottom: 32px;
  }}
  .back-link:hover {{ color: var(--accent); }}
  .eyebrow {{
    font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em;
    text-transform: lowercase; color: var(--accent); background: var(--accent-soft);
    display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 20px;
  }}
  h1 {{
    font-family: var(--serif); font-weight: 600; font-size: clamp(26px, 5vw, 36px);
    line-height: 1.22; letter-spacing: -0.01em; margin: 0 0 16px;
  }}
  .meta {{ font-size: 13px; color: var(--ink-soft); margin-bottom: 36px; }}
  article p {{ font-size: 16.5px; margin: 0 0 20px; }}
  article h2 {{ font-family: var(--serif); font-size: 22px; font-weight: 600; margin: 40px 0 14px; }}
  article strong {{ color: var(--ink); }}
  article ul, article ol {{ font-size: 16.5px; padding-left: 22px; margin: 0 0 20px; }}
  article li {{ margin-bottom: 8px; }}
  figure {{ margin: 32px 0; padding: 20px; background: var(--paper); border: 1px solid var(--rule); border-radius: 10px; }}
  figure svg, figure img {{ display: block; width: 100%; height: auto; }}
  figcaption {{ font-family: var(--mono); font-size: 11px; color: var(--ink-soft); text-align: center; margin-top: 10px; }}
  blockquote {{
    margin: 28px 0; padding-left: 18px; border-left: 2px solid var(--accent);
    font-size: 16px; color: var(--ink-soft); font-style: italic;
  }}
  blockquote p {{ margin: 0; font-size: inherit; color: inherit; font-style: inherit; }}
  .rule {{ border: none; border-top: 1px solid var(--rule); margin: 40px 0; }}
  .cta-box {{ background: var(--accent-soft); border-radius: 10px; padding: 24px 22px; margin-top: 8px; }}
  .cta-box p {{ margin: 0; font-size: 15px; }}
  .cta-box .cta-detail {{ color: var(--ink-soft); font-size: 13.5px; margin-top: 8px; }}
  .sources {{ margin-top: 48px; padding-top: 20px; border-top: 1px solid var(--rule); }}
  .sources h2 {{ font-size: 14px; margin: 0 0 12px; }}
  .sources ol {{ font-size: 13px; color: var(--ink-soft); padding-left: 20px; margin: 0; }}
  .sources li {{ margin-bottom: 6px; }}
</style>
</head>
<body>

<div class="wrap">

  <a class="back-link" href="/notes/">&larr; notes</a>

  <span class="eyebrow">notes / {tag}</span>

  <h1>{title}</h1>
  <p class="meta">Widi Ginanjar &middot; SEO &amp; Growth &middot; {date_display}</p>

  <article>
{content}
  </article>

{sources_block}
</div>

</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga_id}');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#2F6F5E">
<meta name="robots" content="index, follow">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>&#127793;</text></svg>">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&family=Source+Serif+4:wght@600;700&display=swap" rel="stylesheet">

<title>Notes | Widi Ginanjar</title>
<meta name="description" content="Short notes on SEO, technical audits, and what real audits actually find, from Widi Ginanjar.">
<link rel="canonical" href="{site_url}/notes/">

<meta property="og:type" content="website">
<meta property="og:title" content="Notes | Widi Ginanjar">
<meta property="og:description" content="Short notes on SEO, technical audits, and what real audits actually find.">
<meta property="og:url" content="{site_url}/notes/">
<meta property="og:site_name" content="Widi Ginanjar">

<style>
  :root {{
    --bg: #FAFAF7; --paper: #FFFFFF; --ink: #1C1F1B; --ink-soft: #565B54;
    --accent: #2F6F5E; --accent-soft: #E7F0EB; --rule: #E1DED4;
    --mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    --serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.6; -webkit-font-smoothing: antialiased; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .wrap {{ max-width: 680px; margin: 0 auto; padding: 56px 24px 80px; }}
  .back-link {{ font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); text-decoration: none; display: inline-block; margin-bottom: 32px; }}
  .back-link:hover {{ color: var(--accent); }}
  .eyebrow {{ font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em; text-transform: lowercase; color: var(--accent); background: var(--accent-soft); display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 20px; }}
  h1 {{ font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 5vw, 36px); line-height: 1.2; letter-spacing: -0.01em; margin: 0 0 12px; }}
  .subhead {{ font-size: 15px; color: var(--ink-soft); margin: 0 0 36px; max-width: 52ch; }}
  .article-list {{ display: flex; flex-direction: column; gap: 14px; }}
  .article-card {{
    background: var(--paper); border: 1px solid var(--rule); border-radius: 10px;
    padding: 20px 22px; display: block; color: inherit; text-decoration: none;
    transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  }}
  .article-card:hover {{ border-color: var(--accent); transform: translateY(-1px); box-shadow: 0 4px 14px rgba(47, 111, 94, 0.08); text-decoration: none; }}
  .article-card .tag {{ font-family: var(--mono); font-size: 10.5px; color: var(--accent); text-transform: lowercase; letter-spacing: 0.02em; }}
  .article-card h2 {{ font-family: var(--serif); font-size: 18px; font-weight: 600; margin: 8px 0 6px; color: var(--ink); }}
  .article-card p {{ font-size: 13.5px; color: var(--ink-soft); margin: 0; }}
  @media (prefers-reduced-motion: reduce) {{ .article-card {{ transition: none !important; }} .article-card:hover {{ transform: none; }} }}
</style>
</head>
<body>

<div class="wrap">
  <a class="back-link" href="/">&larr; widiginanjar.com</a>
  <span class="eyebrow">notes</span>
  <h1>Notes on SEO &amp; Growth</h1>
  <p class="subhead">Short, specific write-ups drawn from real audits, not generic listicles.</p>
  <div class="article-list">
{cards}
  </div>
</div>

</body>
</html>
"""

CARD_TEMPLATE = """    <a class="article-card" href="/notes/{slug}.html">
      <span class="tag">{tag}</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </a>
"""


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
        body_md = match.group(2)
        slug = front.get("slug") or os.path.splitext(os.path.basename(path))[0]
        front["slug"] = slug
        front["body_md"] = body_md
        posts.append(front)
    posts.sort(key=lambda p: str(p.get("date", "")), reverse=True)
    return posts


def render_sources(sources):
    if not sources:
        return ""
    items = []
    for s in sources:
        title = s.get("title", "")
        url = s.get("url", "")
        publisher = s.get("publisher", "")
        items.append(f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a> &mdash; {publisher}</li>')
    return (
        '<div class="sources">\n<h2>Sources</h2>\n<ol>\n'
        + "\n".join(items)
        + "\n</ol>\n</div>"
    )


def build_article(post):
    title_raw = post.get("title", "Untitled")
    description_raw = post.get("description", "")
    tag_raw = post.get("tag", "seo")
    title = html.escape(title_raw, quote=True)
    description = html.escape(description_raw, quote=True)
    tag = html.escape(tag_raw)
    date = str(post.get("date", ""))
    date_display = date
    slug = post["slug"]
    canonical = f"{SITE_URL}/notes/{slug}.html"

    body_html = markdown.markdown(
        post["body_md"], extensions=["extra", "sane_lists"]
    )

    html_out = ARTICLE_TEMPLATE.format(
        ga_id=GA_ID,
        title=title,
        title_json=json.dumps(title_raw),
        description=description,
        description_json=json.dumps(description_raw),
        canonical=canonical,
        date=date,
        date_display=date_display,
        tag=tag,
        content=body_html,
        sources_block=render_sources(post.get("sources")),
    )

    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Built {out_path}")


def build_index(posts):
    cards = "\n".join(
        CARD_TEMPLATE.format(
            slug=p["slug"],
            tag=html.escape(p.get("tag", "seo")),
            title=html.escape(p.get("title", ""), quote=True),
            description=html.escape(p.get("description", ""), quote=True),
        )
        for p in posts
    )
    html_out = INDEX_TEMPLATE.format(ga_id=GA_ID, site_url=SITE_URL, cards=cards)
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Built {out_path}")


def main():
    posts = load_posts()
    if not posts:
        print("No posts found in notes/posts/*.md")
        return
    for p in posts:
        build_article(p)
    build_index(posts)


if __name__ == "__main__":
    main()
