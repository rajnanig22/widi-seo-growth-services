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
import math
import datetime
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
  "author": {{
    "@type": "Person",
    "name": "Widi Ginanjar",
    "url": "https://widiginanjar.com",
    "sameAs": ["https://linkedin.com/in/widiginanjar"],
    "jobTitle": "SEO & Growth Consultant"
  }},
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
    --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace;
    --serif: Georgia, 'Times New Roman', serif;
    --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
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
  .wrap {{ max-width: 760px; margin: 0 auto; padding: 56px 32px 80px; }}
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
  .author-box {{
    margin-top: 48px; padding: 22px 24px; background: var(--paper);
    border: 1px solid var(--rule); border-radius: 10px;
    display: flex; gap: 16px; align-items: flex-start;
  }}
  .author-box .avatar {{
    width: 40px; height: 40px; border-radius: 50%; background: var(--accent-soft);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--serif); font-weight: 600; font-size: 16px; color: var(--accent);
    flex-shrink: 0;
  }}
  .author-box .author-label {{
    font-family: var(--mono); font-size: 10.5px; text-transform: lowercase;
    color: var(--ink-soft); letter-spacing: 0.04em; margin: 0 0 4px;
  }}
  .author-box p {{ font-size: 13.5px; color: var(--ink-soft); margin: 0 0 12px; }}
  .author-box strong {{ color: var(--ink); }}
  .author-box .author-link {{
    display: inline-block;
    font-family: var(--mono);
    font-size: 12.5px;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 5px 12px;
    border-radius: 6px;
    text-decoration: none;
  }}
  .author-box .author-link:hover {{ text-decoration: none; opacity: 0.85; }}

  @media (max-width: 640px) {{
    .wrap {{ padding: 40px 20px 60px; }}
    h1 {{ font-size: clamp(22px, 7vw, 30px); line-height: 1.25; }}
    .meta {{ font-size: 12px; margin-bottom: 28px; }}
    article p {{ font-size: 15px; margin: 0 0 18px; }}
    article h2 {{ font-size: 19px; margin: 32px 0 12px; }}
    article ul, article ol {{ font-size: 15px; }}
    blockquote {{ font-size: 14px; margin: 22px 0; }}
    .cta-box p {{ font-size: 14px; }}
    .cta-box .cta-detail {{ font-size: 12.5px; }}
    figcaption {{ font-size: 10px; }}
  }}
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

  <div class="author-box">
    <div class="avatar">WG</div>
    <div>
      <p class="author-label">written by</p>
      <p><strong>Widi Ginanjar</strong> is an SEO, growth marketing, and content strategist based in Bali, Indonesia. He currently helps SaaS companies earn organic visibility through SEO and outreach, audits websites for freelance clients across hospitality, B2B, and NGO sectors, and researches how local supply chains create sustainable value on the ground. He previously spent nearly four years in community development and sustainability work with Delterra/McKinsey.org.</p>
      <a class="author-link" href="https://linkedin.com/in/widiginanjar" target="_blank" rel="noopener noreferrer" onclick="gtag('event','contact_click',{{'method':'linkedin','location':'notes_author_box'}});">LinkedIn &rarr;</a>
    </div>
  </div>

{sources_block}
</div>

<script>
  (function() {{
    var tracked = {{}};
    var thresholds = [25, 50, 75, 100];
    function checkScroll() {{
      var scrollTop = window.scrollY || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight <= 0) return;
      var pct = Math.round((scrollTop / docHeight) * 100);
      thresholds.forEach(function(t) {{
        if (pct >= t && !tracked[t]) {{
          tracked[t] = true;
          gtag('event', 'scroll_depth', {{ 'percent': t, 'page_path': window.location.pathname }});
        }}
      }});
    }}
    var ticking = false;
    window.addEventListener('scroll', function() {{
      if (!ticking) {{
        requestAnimationFrame(function() {{ checkScroll(); ticking = false; }});
        ticking = true;
      }}
    }}, {{ passive: true }});
  }})();
</script>
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
    --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace;
    --serif: Georgia, 'Times New Roman', serif;
    --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.6; -webkit-font-smoothing: antialiased; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .wrap {{ max-width: 760px; margin: 0 auto; padding: 56px 32px 80px; }}
  .back-link {{ font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); text-decoration: none; display: inline-block; margin-bottom: 32px; }}
  .back-link:hover {{ color: var(--accent); }}
  .eyebrow {{ font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em; text-transform: lowercase; color: var(--accent); background: var(--accent-soft); display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 20px; }}
  h1 {{ font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 5vw, 36px); line-height: 1.2; letter-spacing: -0.01em; margin: 0 0 12px; }}
  .subhead {{ font-size: 15px; color: var(--ink-soft); margin: 0 0 36px; max-width: 52ch; }}
  .article-list {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 36px; }}
  .section-heading {{
    font-family: var(--mono); font-size: 12px; letter-spacing: 0.04em;
    text-transform: uppercase; color: var(--ink-soft); font-weight: 600;
    margin: 0 0 14px; padding-top: 4px;
  }}
  .section-nav {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 32px; }}
  .section-nav .nav-pill {{
    font-family: var(--mono); font-size: 11.5px; color: var(--ink-soft);
    background: var(--paper); border: 1px solid var(--rule); border-radius: 20px;
    padding: 6px 14px; text-decoration: none; transition: border-color 0.15s ease, color 0.15s ease;
  }}
  .section-nav .nav-pill:hover {{ border-color: var(--accent); color: var(--accent); text-decoration: none; }}
  .article-card {{
    background: var(--paper); border: 1px solid var(--rule); border-radius: 10px;
    padding: 20px 22px; display: block; color: inherit; text-decoration: none;
    transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  }}
  .article-card:hover {{ border-color: var(--accent); transform: translateY(-1px); box-shadow: 0 4px 14px rgba(47, 111, 94, 0.08); text-decoration: none; }}
  .article-card .tag {{ font-family: var(--mono); font-size: 10.5px; color: var(--accent); text-transform: lowercase; letter-spacing: 0.02em; }}
  .article-card h2 {{ font-family: var(--serif); font-size: 18px; font-weight: 600; margin: 8px 0 6px; color: var(--ink); }}
  .article-card p {{ font-size: 13.5px; color: var(--ink-soft); margin: 0; }}
  .article-card .card-meta {{
    font-family: var(--mono); font-size: 11px; color: var(--ink-soft);
    margin-top: 10px; opacity: 0.8;
  }}
  @media (prefers-reduced-motion: reduce) {{ .article-card {{ transition: none !important; }} .article-card:hover {{ transform: none; }} }}

  @media (max-width: 640px) {{
    .wrap {{ padding: 40px 20px 60px; }}
    h1 {{ font-size: clamp(24px, 7vw, 30px); }}
    .subhead {{ font-size: 13px; margin-bottom: 28px; }}
    .article-card {{ padding: 16px 18px; }}
    .article-card h2 {{ font-size: 16px; }}
    .article-card p {{ font-size: 12.5px; }}
    .article-card .card-meta {{ font-size: 10px; }}
  }}
</style>
</head>
<body>

<div class="wrap">
  <a class="back-link" href="/">&larr; widiginanjar.com</a>
  <span class="eyebrow">notes</span>
  <h1>Notes on SEO &amp; Growth</h1>
  <p class="subhead">Short, specific write-ups drawn from real audits, not generic listicles.</p>
{nav}
{cards}
</div>

</body>
</html>
"""

CARD_TEMPLATE = """    <a class="article-card" href="/notes/{slug}.html">
      <span class="tag">{tag}</span>
      <h2>{title}</h2>
      <p>{description}</p>
      <p class="card-meta">{date_display}</p>
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


def format_date(date_str):
    """'2026-07-16' -> 'July 16, 2026'. Falls back to raw string if unparseable."""
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            d = datetime.datetime.strptime(date_str, fmt)
            return d.strftime("%B %-d, %Y") if os.name != "nt" else d.strftime("%B %d, %Y")
        except ValueError:
            continue
    return date_str


def reading_time(text):
    """Rough estimate: 200 words per minute, minimum 1 minute. Strips HTML tags first."""
    plain = re.sub(r"<[^>]+>", " ", text)
    words = re.findall(r"\w+", plain)
    minutes = max(1, math.ceil(len(words) / 200))
    return f"{minutes} min read"


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
    date_display = format_date(date)
    slug = post["slug"]
    canonical = f"{SITE_URL}/notes/{slug}.html"

    body_html = markdown.markdown(
        post["body_md"], extensions=["extra", "sane_lists"]
    )
    read_time = reading_time(post["body_md"])
    date_display = f"{date_display} &middot; {read_time}"
    post["_date_display"] = date_display

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


SECTION_MAP = {
    "mission-driven": "Mission-Driven & NGO",
    "ngo": "Mission-Driven & NGO",
    "practice notes": "Practice Notes",
    "ai search": "AI & Search",
    "ai & tech": "AI & Search",
    "hospitality": "Hospitality & F&B",
    "b2b": "B2B & Professional Services",
}


def build_index(posts):
    groups = {}
    group_order = []
    for p in posts:
        tag = p.get("tag", "seo")
        section = SECTION_MAP.get(tag, tag.title())
        if section not in groups:
            groups[section] = []
            group_order.append(section)
        groups[section].append(p)

    # Order sections by the most recent post date within each group
    group_order.sort(key=lambda s: str(groups[s][0].get("date", "")), reverse=True)

    def slugify(text):
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

    # Quick-nav pills, only meaningful once there's more than one section
    nav_html = ""
    if len(group_order) > 1:
        pills = "\n".join(
            f'    <a href="#{slugify(section)}" class="nav-pill">{html.escape(section)}</a>'
            for section in group_order
        )
        nav_html = f'  <div class="section-nav">\n{pills}\n  </div>\n'

    sections_html = []
    for section in group_order:
        cards = "\n".join(
            CARD_TEMPLATE.format(
                slug=p["slug"],
                tag=html.escape(p.get("tag", "seo")),
                title=html.escape(p.get("title", ""), quote=True),
                description=html.escape(p.get("description", ""), quote=True),
                date_display=p.get("_date_display", ""),
            )
            for p in groups[section]
        )
        sections_html.append(
            f'  <h2 class="section-heading" id="{slugify(section)}">{html.escape(section)}</h2>\n'
            f'  <div class="article-list">\n{cards}\n  </div>\n'
        )

    html_out = INDEX_TEMPLATE.format(
        ga_id=GA_ID, site_url=SITE_URL, nav=nav_html, cards="\n".join(sections_html)
    )
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
