"""Small RSS 2.0 writer shared by build_writing.py and build_notes.py.

Each item carries the summary (description) and the full article
(content:encoded), so feed readers can show the whole post.
"""

import datetime
import email.utils
import re
from xml.sax.saxutils import escape

SITE_URL = "https://widiginanjar.com"
AUTHOR = "Widi Ginanjar"


def rfc822(date_value):
    """'2026-10-31' or a date object -> 'Sat, 31 Oct 2026 08:00:00 +0800'."""
    text = str(date_value)[:10]
    d = datetime.datetime.strptime(text, "%Y-%m-%d")
    d = d.replace(hour=8, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
    return email.utils.format_datetime(d)


def absolute_urls(html_text):
    """Feed readers need full URLs for links and images."""
    return re.sub(r'(href|src)="/(?!/)', rf'\1="{SITE_URL}/', html_text)


def cdata(text):
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def write_feed(path, *, title, link, feed_url, description, language, items, limit=20):
    """items: dicts with title, link, description, date, content_html."""
    items = items[:limit]
    last = rfc822(items[0]["date"]) if items else email.utils.format_datetime(
        datetime.datetime.now(datetime.timezone.utc))
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/">',
        "<channel>",
        f"  <title>{escape(title)}</title>",
        f"  <link>{escape(link)}</link>",
        f'  <atom:link href="{escape(feed_url)}" rel="self" type="application/rss+xml"/>',
        f"  <description>{escape(description)}</description>",
        f"  <language>{language}</language>",
        f"  <lastBuildDate>{last}</lastBuildDate>",
    ]
    for it in items:
        parts += [
            "  <item>",
            f"    <title>{escape(it['title'])}</title>",
            f"    <link>{escape(it['link'])}</link>",
            f'    <guid isPermaLink="true">{escape(it["link"])}</guid>',
            f"    <pubDate>{rfc822(it['date'])}</pubDate>",
            f"    <dc:creator>{AUTHOR}</dc:creator>",
            f"    <description>{escape(it['description'])}</description>",
            f"    <content:encoded>{cdata(absolute_urls(it['content_html']))}</content:encoded>",
            "  </item>",
        ]
    parts += ["</channel>", "</rss>", ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
