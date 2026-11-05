#!/usr/bin/env python3
"""Checks the built site before a pull request is merged.

Run it after the three build scripts. It looks for problems that are easy to
miss by eye:

Errors (the check fails):
  - broken internal links and missing images
  - essays or notes with missing or invalid frontmatter
  - a note tag that is not one of the six in writing_guide.md
  - em dashes or double hyphens in visible text

Warnings (the check passes, but they show up on the pull request):
  - essay photos over about 300 KB
  - Google titles or descriptions long enough to be cut off

On GitHub Actions the problems appear as annotations on the pull request.
Locally they are printed as a list.

Usage: python3 scripts/check_site.py
"""

import datetime
import glob
import os
import re
import sys
from html.parser import HTMLParser

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ON_CI = os.environ.get("GITHUB_ACTIONS") == "true"

NOTE_TAGS = {"ngo", "mission-driven", "hospitality", "b2b", "ai & tech", "ai search", "practice notes"}
ESSAY_FIELDS = ["title", "description", "tag", "date", "slug"]
NOTE_FIELDS = ["title", "description", "tag", "date", "slug"]
IMAGE_LIMIT = 310 * 1024          # "about 300 KB"
TITLE_LIMIT = 65                  # full <title>, including " | Widi Ginanjar"
DESCRIPTION_LIMIT = 160

# Pages that exist only to verify a site or redirect old links.
SKIP_PAGES = {"googlea6e8cda8a891e125.html"}

errors = []
warnings = []


def rel(path):
    return os.path.relpath(path, ROOT)


def report(kind, path, message, line=None):
    (errors if kind == "error" else warnings).append((path, line, message))


# ---------- HTML pages ----------

class PageParser(HTMLParser):
    """Collects links, image sources, the title, the description and visible text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.title = ""
        self.description = None
        self.text = []
        self.redirect = False
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "code", "pre"):
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "a" and a.get("href"):
            self.links.append((a["href"], self.getpos()[0]))
        if tag in ("img", "source") and a.get("src"):
            self.links.append((a["src"], self.getpos()[0]))
        if tag == "link" and a.get("rel") in ("stylesheet", "icon") and a.get("href"):
            self.links.append((a["href"], self.getpos()[0]))
        if tag == "meta":
            if a.get("name") == "description":
                self.description = a.get("content", "")
            if (a.get("http-equiv") or "").lower() == "refresh":
                self.redirect = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "code", "pre") and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip:
            self.text.append((data, self.getpos()[0]))


def target_exists(url):
    path = url.split("#")[0].split("?")[0]
    if not path or path == "/":
        return True
    local = os.path.join(ROOT, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.isfile(os.path.join(local, "index.html"))
    return os.path.isfile(local) or os.path.isfile(os.path.join(local, "index.html"))


def check_pages():
    pages = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if "/node_modules/" not in p and os.path.basename(p) not in SKIP_PAGES]
    for page in sorted(pages):
        parser = PageParser()
        with open(page, encoding="utf-8") as f:
            parser.feed(f.read())
        name = rel(page)

        for url, line in parser.links:
            if url.startswith("/") and not url.startswith("//") and not target_exists(url):
                report("error", name, f"Broken internal link or missing file: {url}", line)

        if parser.redirect:
            continue

        for data, line in parser.text:
            if "—" in data or "–" in data or re.search(r"\s--\s", data):
                snippet = data.strip()[:60]
                report("error", name, f"Em dash or double hyphen in visible text: \"{snippet}\"", line)

        title = " ".join(parser.title.split())
        if len(title) > TITLE_LIMIT:
            report("warning", name, f"Google title is {len(title)} characters and may be cut off (aim for {TITLE_LIMIT} or less). For a note or essay, add a shorter seo_title.")
        if parser.description and len(parser.description) > DESCRIPTION_LIMIT:
            report("warning", name, f"Description is {len(parser.description)} characters and may be cut off (aim for {DESCRIPTION_LIMIT} or less).")


# ---------- Markdown sources ----------

FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def check_posts(folder, fields, kind):
    for path in sorted(glob.glob(os.path.join(ROOT, folder, "*.md"))):
        name = rel(path)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        match = FRONT.match(raw)
        if not match:
            report("error", name, "No frontmatter block (--- at the top and bottom).", 1)
            continue
        try:
            front = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as e:
            report("error", name, f"Frontmatter is not valid YAML: {e}", 1)
            continue

        for field in fields:
            if not str(front.get(field) or "").strip():
                report("error", name, f"Missing frontmatter field: {field}", 1)

        slug = str(front.get("slug") or "")
        if slug and slug != os.path.splitext(os.path.basename(path))[0]:
            report("error", name, f"slug \"{slug}\" does not match the file name.", 1)

        date = front.get("date")
        if date and not isinstance(date, datetime.date):
            try:
                datetime.date.fromisoformat(str(date))
            except ValueError:
                report("error", name, f"date \"{date}\" is not in YYYY-MM-DD format.", 1)

        if kind == "note" and front.get("tag") and str(front["tag"]) not in NOTE_TAGS:
            report("error", name, f"tag \"{front['tag']}\" is not one of the six official tags in writing_guide.md.", 1)

        for i, line in enumerate(raw.splitlines(), 1):
            if "—" in line or "–" in line or re.search(r"\s--\s", line):
                report("error", name, "Em dash or double hyphen. Use a period, comma, colon, or parentheses.", i)


# ---------- Images ----------

def check_images():
    for path in sorted(glob.glob(os.path.join(ROOT, "writing", "img", "*"))):
        if not os.path.isfile(path) or path.endswith(".md"):
            continue
        size = os.path.getsize(path)
        if size > IMAGE_LIMIT:
            report("warning", rel(path), f"Photo is {size // 1024} KB. Essay photos should be about 300 KB or less.")


# ---------- Output ----------

def main():
    check_posts("writing/posts", ESSAY_FIELDS, "essay")
    check_posts("notes/posts", NOTE_FIELDS, "note")
    check_pages()
    check_images()

    for kind, items in (("error", errors), ("warning", warnings)):
        for path, line, message in items:
            if ON_CI:
                loc = f"file={path}" + (f",line={line}" if line else "")
                print(f"::{kind} {loc}::{message}")
            else:
                print(f"{kind.upper():8} {path}{':' + str(line) if line else ''}  {message}")

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
