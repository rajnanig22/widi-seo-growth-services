---
title: "My SEO Portfolio's Title Tag Said \"Notion\" for Two Weeks"
description: "I built a portfolio to sell SEO audits. Its own title tag was generic platform branding the whole time. Here's what that taught me about checking your own site first."
tag: "meta"
date: 2026-07-16
slug: "my-own-title-tag-said-notion"
sources:
  - title: "Meta Title and Description Tags in SEO: Best Practices"
    url: "https://seranking.com/blog/title-tags-and-meta-descriptions-in-seo/"
    publisher: "SE Ranking"
---

I built my portfolio the fast way: a Notion page, shared publicly, five sub-pages for five audiences. It looked clean. Anonymised case studies, a clear CTA, the whole thing done in an afternoon. I linked it everywhere: LinkedIn, email signature, client pitches.

Two weeks in, I did something I tell clients to do on day one: I checked what the raw page actually looked like to something that isn't a browser. Not "does it look good when I open it." What does a crawler, or an AI system that doesn't run JavaScript, actually see.

The title tag said "Notion." The meta description was Notion's own generic product copy: something about teams and agents working together. Nothing about me, nothing about SEO, nothing about the actual content sitting one click away.

## How this actually happens

Notion's public share links render the real page fine in a browser, because your browser runs the JavaScript that builds it. But the raw HTML shell, the version any tool that doesn't execute JavaScript pulls first, ships with Notion's own default metadata. Mine had been sitting there the entire time I was sending the link to people, confident it represented me.

This isn't a rare mistake. [Analysis of 40,000 sites by SE Ranking](https://seranking.com/blog/title-tags-and-meta-descriptions-in-seo/) found that 71% had an empty or missing meta description, and nearly two-thirds had duplicate title tags. Generic or missing metadata isn't an edge case. It's closer to the default state of the average website, mine included, until someone actually checks.

<figure>
  <svg viewBox="0 0 600 170" xmlns="http://www.w3.org/2000/svg">
    <text x="0" y="20" font-family="IBM Plex Mono, monospace" font-size="11" fill="#5C615A">what a non-rendering crawler actually saw</text>
    <rect x="0" y="35" width="600" height="50" rx="6" fill="#FAEEDA" stroke="#E1DED4" stroke-width="1.5"/>
    <text x="16" y="55" font-family="IBM Plex Mono, monospace" font-size="12" fill="#1C1F1B">&lt;title&gt;</text>
    <text x="80" y="55" font-family="Inter, sans-serif" font-size="12" fill="#1C1F1B">Notion</text>
    <text x="16" y="73" font-family="IBM Plex Mono, monospace" font-size="11" fill="#5C615A">Notion's own generic product description, unrelated to my content</text>
    <rect x="0" y="100" width="600" height="50" rx="6" fill="#E7F0EB" stroke="#E1DED4" stroke-width="1.5"/>
    <text x="16" y="120" font-family="IBM Plex Mono, monospace" font-size="12" fill="#1C1F1B">&lt;title&gt;</text>
    <text x="80" y="120" font-family="Inter, sans-serif" font-size="12" fill="#1C1F1B">Widi Ginanjar | SEO &amp; Growth Services</text>
    <text x="16" y="138" font-family="IBM Plex Mono, monospace" font-size="11" fill="#2F6F5E">specific, accurate, written for this page and no other</text>
  </svg>
  <figcaption>Same content, two very different first impressions to anything that doesn't run JavaScript</figcaption>
</figure>

## The fix, and the more useful lesson

The fix itself was straightforward: move the front door of the portfolio to a plain static HTML page I fully control, with hand-written title tags, meta descriptions, and structured data. That's what this site is now. The detailed case studies still live on Notion, but the page people actually land on first, and the one crawlers see, is one I built by hand.

The more useful lesson is the order I did things in. I'd been telling myself the portfolio was "done" because it looked right in a browser. I hadn't checked what it looked like to anything else. That's an easy mistake to make precisely because it's invisible from the inside: everything about the experience of visiting your own site feels fine, right up until you look at it the way a machine does.

I'd been about to pitch AI-citability audits to clients while my own site's raw metadata said "Notion." If I hadn't caught it, that's not a hypothetical embarrassment, that's the exact failure I'd be auditing someone else for.

<hr class="rule">

<div class="cta-box">
  <p><strong>Curious what your site actually says to something that doesn't render JavaScript?</strong> I offer a free 30-minute look.</p>
  <p class="cta-detail">You'll walk away with one concrete finding either way, whether or not we end up working together. <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{'method':'email','location':'notes_cta'});">Get in touch</a> or <a href="/book.html" onclick="gtag('event','contact_click',{'method':'booking','location':'notes_cta'});">book a call</a>.</p>
</div>
