#!/usr/bin/env python3
"""
Regenerates sitemap.xml and llms.txt at the repo root from every page on the site.

- Static pages are listed below (STATIC_PAGES, SERVICE_PAGES).
- Essays come from writing/posts/*.md, notes from notes/posts/*.md (YAML frontmatter:
  title, description, slug, date).

Runs automatically after build_writing.py and build_notes.py in GitHub Actions,
so a new essay or note always shows up in both files without manual edits.

Run: python3 scripts/build_site_index.py
"""

import os
import re
import glob
import datetime

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://widiginanjar.com"

# (path, priority, changefreq)
STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/services/", "0.9", "monthly"),
    ("/writing/", "0.9", "weekly"),
    ("/notes/", "0.8", "weekly"),
    ("/about.html", "0.8", "monthly"),
    ("/scope-of-work.html", "0.7", "monthly"),
    ("/book.html", "0.6", "yearly"),
]

# (path, llms.txt title, llms.txt description)
SERVICE_PAGES = [
    ("/services/ngo.html", "SEO for NGOs & Mission-Driven Teams",
     "Technical SEO for NGOs, nonprofits, and social enterprises."),
    ("/services/b2b.html", "B2B SEO Strategy for Professional Services",
     "SEO and backlink strategy for consulting, research, and B2B firms."),
    ("/services/hospitality.html", "Restaurant SEO for Hospitality & F&B Brands",
     "Local SEO and Google Business Profile optimisation for restaurants, bars, and hospitality groups."),
    ("/services/ai-search-era.html", "AI Search Optimization & Citability",
     "Helping organisations get found and accurately cited by ChatGPT, Perplexity, and Google AI summaries."),
]

LLMS_HEADER = """# Widi Ginanjar

> Works in research, project management, and sustainability, mostly with community programs in Indonesia. Also does SEO consulting for NGOs, B2B firms, hospitality brands, and organisations navigating AI search, and writes field notes and essays in Bahasa Indonesia. Background in community-based development (Delterra, YCAB, BIDUK) and in SEO and growth marketing (BetterPic, Runflow).
"""


def load_posts(folder):
    posts = []
    for path in glob.glob(os.path.join(ROOT, folder, "posts", "*.md")):
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
        if not match:
            continue
        front = yaml.safe_load(match.group(1)) or {}
        front["slug"] = front.get("slug") or os.path.splitext(os.path.basename(path))[0]
        front["date"] = str(front.get("date", ""))[:10]
        posts.append(front)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def valid_date(text):
    try:
        datetime.datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def url_block(loc, priority, changefreq, lastmod=""):
    lines = ["  <url>", f"    <loc>{loc}</loc>"]
    if lastmod and valid_date(lastmod):
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines += [f"    <changefreq>{changefreq}</changefreq>", f"    <priority>{priority}</priority>", "  </url>"]
    return "\n".join(lines)


def build_sitemap(essays, notes):
    blocks = [url_block(SITE_URL + path, pr, cf) for path, pr, cf in STATIC_PAGES]
    blocks += [url_block(SITE_URL + path, "0.8", "monthly") for path, _, _ in SERVICE_PAGES
               if os.path.exists(os.path.join(ROOT, path.lstrip("/")))]
    blocks += [url_block(f"{SITE_URL}/writing/{p['slug']}.html", "0.7", "yearly", p["date"]) for p in essays]
    blocks += [url_block(f"{SITE_URL}/notes/{p['slug']}.html", "0.7", "yearly", p["date"]) for p in notes]
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(blocks) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Wrote sitemap.xml ({len(blocks)} URLs)")


def line(title, url, desc):
    title = str(title).strip()
    desc = str(desc).strip()
    return f"- [{title}]({url}): {desc}" if desc else f"- [{title}]({url})"


def essay_title(p):
    """Indonesian title, with the English translation in brackets when there is one."""
    title = str(p.get("title", "")).strip()
    return f"{title} (English: {str(p['title_en']).strip()})" if p.get("title_en") else title


def essay_desc(p):
    """English summary first (llms.txt is read in English), then the Indonesian original."""
    id_desc = str(p.get("description", "")).strip()
    en_desc = str(p.get("description_en") or "").strip()
    return f"{en_desc} Indonesian: {id_desc}" if en_desc else id_desc


def build_llms(essays, notes):
    parts = [LLMS_HEADER]

    parts.append("## Essays (field notes and essays, in Bahasa Indonesia)\n")
    parts.append(line("Essays index", f"{SITE_URL}/writing/", "All essays and field notes."))
    parts += [line(essay_title(p), f"{SITE_URL}/writing/{p['slug']}.html", essay_desc(p)) for p in essays]

    parts.append("\n## Services\n")
    parts.append(line("Services overview", f"{SITE_URL}/services/", "SEO consulting: services, scope of work, and booking."))
    parts += [line(t, SITE_URL + path, d) for path, t, d in SERVICE_PAGES
              if os.path.exists(os.path.join(ROOT, path.lstrip("/")))]
    parts.append(line("Full Scope of Work", f"{SITE_URL}/scope-of-work.html", "Complete, itemised breakdown of every service offered."))
    parts.append(line("About", f"{SITE_URL}/about.html", "Background, approach, and career history."))

    parts.append("\n## Notes (technical write-ups and case studies)\n")
    parts.append(line("Notes index", f"{SITE_URL}/notes/", "Full archive of write-ups on SEO, growth, and AI search."))
    parts += [line(p.get("title", ""), f"{SITE_URL}/notes/{p['slug']}.html", p.get("description", "")) for p in notes]

    parts.append("\n## Optional\n")
    parts.append(line("Book a free 30-minute look", f"{SITE_URL}/book.html", "Scheduling page for a free site review."))

    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")
    print(f"Wrote llms.txt ({len(essays)} essays, {len(notes)} notes)")


def main():
    essays = load_posts("writing")
    notes = load_posts("notes")
    build_sitemap(essays, notes)
    build_llms(essays, notes)


if __name__ == "__main__":
    main()
