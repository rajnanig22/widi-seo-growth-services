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
import urllib.parse
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
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600;700&display=swap" rel="stylesheet"></noscript>

<title>{title} | Widi Ginanjar</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Widi Ginanjar">
<meta property="og:locale" content="en_US">
{og_image}
<meta name="twitter:card" content="{twitter_card}">
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
    --mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    --serif: 'IBM Plex Serif', Georgia, 'Times New Roman', serif;
    --sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
  .wrap {{ max-width: 1520px; margin: 0 auto; padding: 0 clamp(20px, 5vw, 80px); }}
  .art-hero {{ display: grid; grid-template-columns: 1fr minmax(0, 0.8fr); gap: 56px; align-items: center; padding-bottom: 48px; border-bottom: 1px solid var(--rule); }}
  .art-hero.no-cover {{ grid-template-columns: 1fr; }}
  .art-hero .cover {{ display: block; width: 100%; height: auto; aspect-ratio: 1200 / 630; object-fit: cover; border-radius: 12px; margin: 0; }}
  .art-body {{ max-width: 46em; padding: 48px 0 72px; }}
  .back-link {{
    font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft);
    text-decoration: none; display: block; width: fit-content; margin: 32px 0 24px;
  }}
  .back-link:hover {{ color: var(--accent); }}
  .eyebrow {{
    font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em;
    text-transform: lowercase; color: var(--accent); background: var(--accent-soft);
    display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 20px;
  }}
  h1 {{
    font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 3.6vw, 42px);
    line-height: 1.22; letter-spacing: -0.01em; margin: 0 0 16px;
  }}
  .meta {{ font-size: 13px; color: var(--ink-soft); margin: 0; }}
  article p {{ font-size: 16.5px; margin: 0 0 20px; }}
  article h2 {{ font-family: var(--serif); font-size: 22px; font-weight: 600; margin: 40px 0 14px; }}
  article h3 {{ font-family: var(--serif); font-size: 19px; font-weight: 600; line-height: 1.3; margin: 32px 0 12px; }}
  article strong {{ color: var(--ink); }}
  article ul, article ol {{ font-size: 16.5px; padding-left: 22px; margin: 0 0 20px; }}
  article li {{ margin-bottom: 8px; }}
  article table {{
    width: 100%; border-collapse: collapse; margin: 28px 0; font-size: 12.5px;
  }}
  article th {{
    text-align: left; font-family: var(--mono); font-size: 11px; text-transform: lowercase;
    letter-spacing: 0.02em; color: var(--ink-soft); background: var(--accent-soft);
    padding: 10px 14px; border-bottom: 1px solid var(--rule);
  }}
  article td {{
    padding: 9px 14px; border-bottom: 1px solid var(--rule); color: var(--ink);
  }}
  article tr:last-child td {{ border-bottom: none; }}
  article td:not(:first-child), article th:not(:first-child) {{ font-family: var(--mono); font-size: 13px; }}
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
  .author-box .avatar {{ width: 56px; height: 56px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }}
  .author-box .author-link + .author-link {{ margin-left: 6px; }}
  .cover {{ display: block; width: 100%; height: auto; aspect-ratio: 1200 / 630; object-fit: cover; border-radius: 10px; margin: 0 0 36px; }}
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

  @media (max-width: 760px) {{
    .art-hero {{ grid-template-columns: 1fr; gap: 24px; padding-bottom: 32px; }}
    .art-hero .cover {{ order: -1; }}
    .art-body {{ padding: 32px 0 48px; }}
  }}
  @media (max-width: 640px) {{
    h1 {{ font-size: clamp(22px, 7vw, 30px); line-height: 1.25; }}
    .meta {{ font-size: 12px; margin-bottom: 28px; }}
    article p {{ font-size: 15px; margin: 0 0 18px; }}
    article h2 {{ font-size: 19px; margin: 32px 0 12px; }}
    article h3 {{ font-size: 17px; margin: 28px 0 10px; }}
    article ul, article ol {{ font-size: 15px; }}
    blockquote {{ font-size: 14px; margin: 22px 0; }}
    .cta-box p {{ font-size: 14px; }}
    .cta-box .cta-detail {{ font-size: 12.5px; }}
    figcaption {{ font-size: 10px; }}
    article table {{ font-size: 11px; }}
    article th, article td {{ padding: 7px 8px; }}
    article td:not(:first-child), article th:not(:first-child) {{ font-size: 10px; }}
  }}
  .navwrap {{ max-width: 1520px; margin: 0 auto; padding: 0 clamp(20px, 5vw, 80px); }}
  nav.top {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; border-bottom: 1px solid var(--rule); flex-wrap: wrap; }}
  .nav-home {{ font-family: var(--mono); font-size: 13px; color: var(--ink); letter-spacing: 0.02em; text-decoration: none; }}
  .nav-links {{ display: flex; gap: 28px; flex-wrap: wrap; }}
  .nav-links a {{ font-size: 15px; font-weight: 600; color: var(--ink); border-bottom: 2px solid transparent; padding-bottom: 3px; text-decoration: none; }}
  .nav-links a:hover, .nav-home:hover {{ color: var(--accent); text-decoration: none; }}
  .nav-links a:hover {{ border-bottom-color: var(--accent); }}
  .site-foot {{ background: #16302A; color: rgba(255,255,255,0.75); }}
  .site-foot-in {{ max-width: 1520px; margin: 0 auto; padding: 28px clamp(20px, 5vw, 80px) 32px; display: flex; justify-content: space-between; align-items: center; gap: 12px 32px; flex-wrap: wrap; font-size: 13.5px; }}
  .site-foot-in p {{ margin: 0; color: rgba(255,255,255,0.75); font-size: 13.5px; }}
  .site-foot .links {{ display: flex; gap: 22px; }}
  .site-foot .links a {{ display: inline-flex; align-items: center; justify-content: center; min-width: 32px; min-height: 32px; color: #CFE5DA; }}
  .site-foot .links a:hover {{ color: #FFFFFF; text-decoration: none; }}
  @media (max-width: 760px) {{ .nav-home {{ display: none; }} nav.top {{ justify-content: flex-end; }} }}
  @media (max-width: 420px) {{ .nav-links {{ gap: 14px; }} .nav-links a {{ font-size: 13px; }} }}
  /* shared nav: name on the left on every screen, lighter links */
  .nav-home {{ font-family: var(--serif) !important; font-weight: 700; font-size: 19px !important; letter-spacing: -0.01em !important; color: var(--ink); display: inline !important; text-decoration: none; }}
  nav.top .nav-links {{ gap: 24px; }}
  nav.top .nav-links a {{ font-size: 16px; font-weight: 600; color: var(--ink); }}
  nav.top .nav-links a[aria-current] {{ color: var(--accent); border-bottom-color: var(--accent); }}
  @media (max-width: 820px) {{ nav.top {{ justify-content: space-between !important; flex-wrap: nowrap !important; }} }}
  @media (max-width: 420px) {{ .nav-home {{ font-size: 15px !important; }} nav.top .nav-links {{ gap: 12px !important; }} nav.top .nav-links a {{ font-size: 13.5px !important; }} }}
  .subnav {{ display: flex; flex-wrap: wrap; gap: 6px 24px; padding: 12px 0; border-bottom: 1px solid var(--rule); font-size: 14.5px; }}
  .subnav a {{ color: var(--ink-soft); font-weight: 500; text-decoration: none; }}
  .subnav a:hover, .subnav a[aria-current] {{ color: var(--accent); text-decoration: none; }}
  .subnav a[aria-current] {{ font-weight: 600; }}
  @media (max-width: 420px) {{ .subnav {{ gap: 6px 16px; font-size: 13.5px; }} .subnav .long {{ display: none; }} }}
  .end-actions {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 40px; padding-top: 28px; border-top: 1px solid var(--rule); }}
  .btn {{ display: inline-flex; align-items: center; gap: 8px; padding: 12px 18px; border-radius: 10px; border: 1px solid var(--rule); background: var(--paper); color: var(--ink); font-size: 15px; font-weight: 600; text-decoration: none; }}
  .btn:hover {{ border-color: var(--accent); color: var(--accent); text-decoration: none; }}
  .btn-primary {{ background: var(--accent); border-color: var(--accent); color: #FFFFFF; }}
  .btn-primary:hover {{ background: #255A4C; color: #FFFFFF; }}
  @media (max-width: 420px) {{ .end-actions .btn {{ flex: 1 1 100%; justify-content: center; }} }}
  .to-top {{ position: fixed; right: 16px; bottom: 16px; padding: 9px 14px; border-radius: 999px; background: var(--accent); color: #FFFFFF; font-size: 13.5px; font-weight: 600; text-decoration: none; opacity: 0; pointer-events: none; transition: opacity 0.2s ease; z-index: 10; }}
  .to-top.show {{ opacity: 0.92; pointer-events: auto; }}
  .to-top:hover {{ opacity: 1; text-decoration: none; color: #FFFFFF; }}
</style>
</head>
<body>

<div class="navwrap">
  <nav class="top" aria-label="Main">
    <a class="nav-home" href="/">Widi Ginanjar</a>
    <div class="nav-links">
      <a href="/writing/">Essays</a>
      <a href="/about.html">About</a>
      <a aria-current="page" href="/services/">SEO Consulting</a>
    </div>
  </nav>
  <nav class="subnav" aria-label="SEO Consulting">
    <a href="/services/">Services</a>
    <a href="/notes/" aria-current="page">SEO Notes</a>
    <a href="/scope-of-work.html">Scope<span class="long"> of work</span></a>
    <a href="/book.html">Book a call</a>
  </nav>
</div>

<div class="wrap">

  <a class="back-link" href="/notes/">&larr; SEO Notes</a>

  <header class="art-hero{hero_class}">
    <div>
      <span class="eyebrow">notes / {tag}</span>
      <h1>{title}</h1>
      <p class="meta">Widi Ginanjar &middot; {date_display}</p>
    </div>
{cover_block}  </header>

  <div class="art-body">
  <article>
{content}
  </article>

  <div class="author-box">
    <img class="avatar" src="/img/widi-ginanjar-round.jpg" alt="" width="56" height="56" loading="lazy">
    <div>
      <p class="author-label">written by</p>
      <p><strong>Widi Ginanjar</strong> works on research, project management, and sustainability with community programs, and helps a few organisations with SEO. These notes come from that SEO work.</p>
      <a class="author-link" href="/about.html">About &rarr;</a>
      <a class="author-link" href="https://linkedin.com/in/widiginanjar" target="_blank" rel="noopener noreferrer" onclick="gtag('event','contact_click',{{'method':'linkedin','location':'notes_author_box'}});">LinkedIn &rarr;</a>
    </div>
  </div>

{sources_block}
  <div class="end-actions">
    <a class="btn btn-primary" href="/notes/" onclick="gtag('event','note_end_click',{{'action':'more_notes'}});">More SEO notes <span aria-hidden="true">&rarr;</span></a>
    <a class="btn" href="{linkedin_share}" target="_blank" rel="noopener noreferrer" onclick="gtag('event','note_end_click',{{'action':'share_linkedin'}});">Share on LinkedIn</a>
  </div>
  </div>
</div>

<a class="to-top" href="#" aria-label="Back to top">&uarr; Top</a>
<script>
  (function () {{
    var b = document.querySelector('.to-top');
    function check() {{
      var nearEnd = window.innerHeight + window.scrollY > document.documentElement.scrollHeight - 220;
      b.classList.toggle('show', window.scrollY > 900 && !nearEnd);
    }}
    window.addEventListener('scroll', check, {{ passive: true }});
    b.addEventListener('click', function (e) {{ e.preventDefault(); window.scrollTo({{ top: 0, behavior: 'smooth' }}); }});
  }})();
</script>

<div class="site-foot">
  <div class="site-foot-in">
    <p>&copy; 2026 Widi Ginanjar</p>
    <div class="links">
      <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{{'method':'email','location':'site_footer'}});" aria-label="Email" title="Email"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="m22 6-10 7L2 6"/></svg></a>
        <a href="https://linkedin.com/in/widiginanjar" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn"><svg width="20" height="20" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a>
        <a href="https://www.instagram.com/wdwynson/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" title="Instagram"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.6" fill="currentColor"/></svg></a>
    </div>
  </div>
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

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@600;700&display=swap" rel="stylesheet"></noscript>

<title>SEO Notes | Widi Ginanjar</title>
<meta name="description" content="Short notes on SEO, technical audits, and what real audits actually find, from Widi Ginanjar.">
<link rel="canonical" href="{site_url}/notes/">

<meta property="og:type" content="website">
<meta property="og:title" content="SEO Notes | Widi Ginanjar">
<meta property="og:description" content="Short notes on SEO, technical audits, and what real audits actually find.">
<meta property="og:url" content="{site_url}/notes/">
<meta property="og:site_name" content="Widi Ginanjar">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{site_url}/og-home.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<style>
  :root {{
    --bg: #FAFAF7; --paper: #FFFFFF; --ink: #1C1F1B; --ink-soft: #565B54;
    --accent: #2F6F5E; --accent-soft: #E7F0EB; --rule: #E1DED4;
    --mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    --serif: 'IBM Plex Serif', Georgia, 'Times New Roman', serif;
    --sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); line-height: 1.6; -webkit-font-smoothing: antialiased; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .wrap {{ max-width: 1520px; margin: 0 auto; padding: 40px clamp(20px, 5vw, 80px) 72px; }}
  .back-link {{ font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); text-decoration: none; display: block; width: fit-content; margin-bottom: 32px; }}
  .back-link:hover {{ color: var(--accent); }}
  .eyebrow {{ font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em; text-transform: lowercase; color: var(--accent); background: var(--accent-soft); display: inline-block; padding: 4px 10px; border-radius: 4px; margin-bottom: 20px; }}
  h1 {{ font-family: var(--serif); font-weight: 600; font-size: clamp(28px, 5vw, 36px); line-height: 1.2; letter-spacing: -0.01em; margin: 0 0 12px; }}
  .subhead {{ font-size: 15px; color: var(--ink-soft); margin: 0 0 36px; max-width: 52ch; }}
  .article-list {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin-bottom: 44px; }}
  @media (max-width: 1000px) {{ .article-list {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  @media (max-width: 640px) {{ .article-list {{ grid-template-columns: 1fr; }} }}
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
    display: flex; flex-direction: column; overflow: hidden; color: inherit; text-decoration: none;
    transition: border-color 0.15s ease;
  }}
  .article-card:hover {{ border-color: var(--accent); text-decoration: none; }}
  .article-card .thumb {{ display: block; aspect-ratio: 1200 / 630; background-size: cover; background-position: center; border-bottom: 1px solid var(--rule); }}
  .article-card .card-body {{ display: flex; flex-direction: column; flex: 1; padding: 18px 20px 20px; min-width: 0; }}
  .article-card-top {{ display: flex; align-items: center; justify-content: space-between; }}
  .article-card .tag {{ font-family: var(--mono); font-size: 10.5px; color: var(--accent); text-transform: lowercase; letter-spacing: 0.02em; }}
  .article-card .go-arrow {{
    font-family: var(--mono); font-size: 15px; color: var(--ink-soft);
    transition: color 0.15s ease, transform 0.15s ease;
  }}
  .article-card:hover .go-arrow {{ color: var(--accent); transform: translateX(2px); }}
  .article-card h2 {{ font-family: var(--serif); font-size: 18px; font-weight: 600; margin: 8px 0 6px; color: var(--ink); }}
  .article-card p {{ font-size: 13.5px; color: var(--ink-soft); margin: 0; }}
  .article-card .card-meta {{
    font-family: var(--mono); font-size: 11px; color: var(--ink-soft);
    margin-top: auto; padding-top: 14px; opacity: 0.8;
  }}
  @media (prefers-reduced-motion: reduce) {{ .article-card {{ transition: none !important; }} }}

  @media (max-width: 640px) {{
    .wrap {{ padding: 40px 20px 60px; }}
    h1 {{ font-size: clamp(24px, 7vw, 30px); }}
    .subhead {{ font-size: 13px; margin-bottom: 28px; }}
    .article-card .card-body {{ padding: 16px 18px; }}
    .article-card h2 {{ font-size: 16px; }}
    .article-card p {{ font-size: 12.5px; }}
    .article-card .card-meta {{ font-size: 10px; }}
  }}
  .navwrap {{ max-width: 1520px; margin: 0 auto; padding: 0 clamp(20px, 5vw, 80px); }}
  nav.top {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 0; border-bottom: 1px solid var(--rule); flex-wrap: wrap; }}
  .nav-home {{ font-family: var(--mono); font-size: 13px; color: var(--ink); letter-spacing: 0.02em; text-decoration: none; }}
  .nav-links {{ display: flex; gap: 28px; flex-wrap: wrap; }}
  .nav-links a {{ font-size: 15px; font-weight: 600; color: var(--ink); border-bottom: 2px solid transparent; padding-bottom: 3px; text-decoration: none; }}
  .nav-links a:hover, .nav-home:hover {{ color: var(--accent); text-decoration: none; }}
  .nav-links a:hover {{ border-bottom-color: var(--accent); }}
  .site-foot {{ background: #16302A; color: rgba(255,255,255,0.75); }}
  .site-foot-in {{ max-width: 1520px; margin: 0 auto; padding: 28px clamp(20px, 5vw, 80px) 32px; display: flex; justify-content: space-between; align-items: center; gap: 12px 32px; flex-wrap: wrap; font-size: 13.5px; }}
  .site-foot-in p {{ margin: 0; color: rgba(255,255,255,0.75); font-size: 13.5px; }}
  .site-foot .links {{ display: flex; gap: 22px; }}
  .site-foot .links a {{ display: inline-flex; align-items: center; justify-content: center; min-width: 32px; min-height: 32px; color: #CFE5DA; }}
  .site-foot .links a:hover {{ color: #FFFFFF; text-decoration: none; }}
  @media (max-width: 760px) {{ .nav-home {{ display: none; }} nav.top {{ justify-content: flex-end; }} }}
  @media (max-width: 420px) {{ .nav-links {{ gap: 14px; }} .nav-links a {{ font-size: 13px; }} }}
  /* shared nav: name on the left on every screen, lighter links */
  .nav-home {{ font-family: var(--serif) !important; font-weight: 700; font-size: 19px !important; letter-spacing: -0.01em !important; color: var(--ink); display: inline !important; text-decoration: none; }}
  nav.top .nav-links {{ gap: 24px; }}
  nav.top .nav-links a {{ font-size: 16px; font-weight: 600; color: var(--ink); }}
  nav.top .nav-links a[aria-current] {{ color: var(--accent); border-bottom-color: var(--accent); }}
  @media (max-width: 820px) {{ nav.top {{ justify-content: space-between !important; flex-wrap: nowrap !important; }} }}
  @media (max-width: 420px) {{ .nav-home {{ font-size: 15px !important; }} nav.top .nav-links {{ gap: 12px !important; }} nav.top .nav-links a {{ font-size: 13.5px !important; }} }}
  .subnav {{ display: flex; flex-wrap: wrap; gap: 6px 24px; padding: 12px 0; border-bottom: 1px solid var(--rule); font-size: 14.5px; }}
  .subnav a {{ color: var(--ink-soft); font-weight: 500; text-decoration: none; }}
  .subnav a:hover, .subnav a[aria-current] {{ color: var(--accent); text-decoration: none; }}
  .subnav a[aria-current] {{ font-weight: 600; }}
  @media (max-width: 420px) {{ .subnav {{ gap: 6px 16px; font-size: 13.5px; }} .subnav .long {{ display: none; }} }}
</style>
</head>
<body>

<div class="navwrap">
  <nav class="top" aria-label="Main">
    <a class="nav-home" href="/">Widi Ginanjar</a>
    <div class="nav-links">
      <a href="/writing/">Essays</a>
      <a href="/about.html">About</a>
      <a aria-current="page" href="/services/">SEO Consulting</a>
    </div>
  </nav>
  <nav class="subnav" aria-label="SEO Consulting">
    <a href="/services/">Services</a>
    <a href="/notes/" aria-current="page">SEO Notes</a>
    <a href="/scope-of-work.html">Scope<span class="long"> of work</span></a>
    <a href="/book.html">Book a call</a>
  </nav>
</div>

<div class="wrap">
  <a class="back-link" href="/services/">&larr; SEO Consulting</a>
  <span class="eyebrow">seo notes</span>
  <h1>SEO Notes</h1>
  <p class="subhead">Short, specific write-ups drawn from real audits, not generic listicles.</p>
{nav}
{cards}
</div>

<div class="site-foot">
  <div class="site-foot-in">
    <p>&copy; 2026 Widi Ginanjar</p>
    <div class="links">
      <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{{'method':'email','location':'site_footer'}});" aria-label="Email" title="Email"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><path d="m22 6-10 7L2 6"/></svg></a>
        <a href="https://linkedin.com/in/widiginanjar" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn"><svg width="20" height="20" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a>
        <a href="https://www.instagram.com/wdwynson/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" title="Instagram"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.6" fill="currentColor"/></svg></a>
    </div>
  </div>
</div>

</body>
</html>
"""

CARD_TEMPLATE = """    <a class="article-card" href="/notes/{slug}.html">
      {thumb}
      <div class="card-body">
        <div class="article-card-top">
          <span class="tag">{tag}</span>
          <span class="go-arrow">&rarr;</span>
        </div>
        <h2>{title}</h2>
        <p>{description}</p>
        <p class="card-meta">{date_display}</p>
      </div>
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
        items.append(f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>, {publisher}</li>')
    return (
        '<div class="sources">\n<h2>Sources</h2>\n<ol>\n'
        + "\n".join(items)
        + "\n</ol>\n</div>"
    )


def cover_path(slug):
    """Site path of the note's cover (made by make_note_covers.py), or '' if there is none."""
    if os.path.exists(os.path.join(OUTPUT_DIR, "img", f"{slug}.jpg")):
        return f"/notes/img/{slug}.jpg"
    return ""


def og_image_tags(slug):
    path = cover_path(slug)
    if not path:
        return ""
    url = SITE_URL + path
    return (f'<meta property="og:image" content="{url}">\n'
            '<meta property="og:image:width" content="1200">\n'
            '<meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:image" content="{url}">\n')


def thumb_html(slug):
    path = cover_path(slug)
    if not path:
        return ""
    return f'<span class="thumb" style="background-image:url({path})" aria-hidden="true"></span>'


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
        linkedin_share="https://www.linkedin.com/sharing/share-offsite/?url=" + urllib.parse.quote(
            f"{canonical}?utm_source=linkedin&utm_medium=social&utm_campaign=share_button", safe=""),
        date=date,
        date_display=date_display,
        tag=tag,
        content=body_html,
        sources_block=render_sources(post.get("sources")),
        og_image=og_image_tags(slug),
        cover_block=(f'    <img class="cover" src="{cover_path(slug)}" alt="" width="1200" height="630">\n' if cover_path(slug) else ""),
        hero_class="" if cover_path(slug) else " no-cover",
        twitter_card="summary_large_image" if cover_path(slug) else "summary",
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
                thumb=thumb_html(p["slug"]),
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
    # llms.txt and sitemap.xml are now built by scripts/build_site_index.py


if __name__ == "__main__":
    main()
