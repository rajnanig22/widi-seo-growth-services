---
title: "Google Knows My Website. It Doesn't Know Me."
description: "Two searches, minutes apart. One found my site accurately. The other pulled from LinkedIn and mixed me up with someone else entirely."
tag: "ai search"
date: 2026-08-07
slug: "ai-overview-domain-vs-name"
---

I ran two Google searches back to back last night. Same person, same intent, one word different.

First search: my domain, widiginanjar.com. The AI Overview got it right, in detail. It described the site as my professional portfolio, correctly listed the four things I actually specialise in (NGO, B2B, hospitality, AI search), and cited the site itself as the source.

Second search: my name, Widi Ginanjar. No domain, just the name. The AI Overview came back completely different. It only pulled from LinkedIn, described me as someone working in "digital operations and community management," and never mentioned the SEO work at all. It even added a line saying if I meant a different Widi Ginanjar, to share more details, because there's a Wikipedia page for someone with a similar name and Google wasn't sure which one I meant.

**Same person. Two searches, minutes apart. Completely different answers.**

<figure>
<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="300" height="220" rx="10" fill="#FFFFFF" stroke="#E1DED4"/>
  <text x="150" y="34" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" fill="#2F6F5E">search: widiginanjar.com</text>
  <text x="150" y="70" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#1C1F1B">Correctly describes</text>
  <text x="150" y="92" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#1C1F1B">the SEO consultancy</text>
  <text x="150" y="130" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#565B54">source: widiginanjar.com</text>

  <rect x="340" y="0" width="300" height="220" rx="10" fill="#FFFFFF" stroke="#E1DED4"/>
  <text x="490" y="34" text-anchor="middle" font-family="ui-monospace, monospace" font-size="12" fill="#2F6F5E">search: widi ginanjar</text>
  <text x="490" y="70" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#1C1F1B">Only describes the</text>
  <text x="490" y="92" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#1C1F1B">LinkedIn job history</text>
  <text x="490" y="130" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="#565B54">source: linkedin.com</text>
  <text x="490" y="160" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" fill="#9A958A">+ a disclaimer about</text>
  <text x="490" y="176" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" fill="#9A958A">a different person</text>
</svg>
<figcaption>Same person, two queries, two very different answers.</figcaption>
</figure>

I've written about this gap before, [ranking well on Google versus being understood by AI](/notes/ranking-vs-ai-citation.html), but this is a cleaner version of the same problem, because nothing else changed except which word I typed.

## Why a domain search and a name search aren't the same question

A domain is unambiguous. There's one widiginanjar.com, so Google has one clear thing to describe, and it can pull straight from the site itself.

A name is a different kind of query entirely. Plenty of people share a name, so Google has to guess which one you mean, and it leans on whatever source looks most established. In my case, that's a LinkedIn profile with years of history and 800-plus followers, against a three-week-old website with almost no other sites linking to it yet. LinkedIn wins that comparison easily, not because the information there is more accurate about what I actually do now, but because it's the source Google trusts more right now.

**The AI Overview isn't wrong so much as it's outdated by default.** It's summarising the version of me that has the most established signal, not the most current one.

## Why this actually matters, not just as a curiosity

If someone hears my name from a referral and looks me up instead of clicking a link, this is what they'd get: a description of a past job, not the consultancy I actually run now. That's a real gap between what I do and what shows up when someone searches for me directly, and it's a gap I wouldn't have known was this specific without actually testing it.

## What I'm trying, without knowing yet if it'll work

I added an `llms.txt` file to the site this week, a short, plain-language summary written specifically for AI systems to read, listing what the site actually covers. It's a new, informal convention, not something Google or OpenAI has officially confirmed they use. I don't know yet if it changes anything. But it's cheap to try, and given that half of what I write about here is telling other people to make their sites legible to AI, it felt strange not to test it on my own first.

<hr class="rule">

<div class="cta-box">
  <p><strong>If you're not sure what AI tools currently say about your organisation when someone searches your name,</strong> I offer a free 30-minute look at your site.</p>
  <p class="cta-detail">You'll walk away with one concrete finding either way, whether or not we end up working together. <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{'method':'email','location':'notes_cta'});">Get in touch</a> or <a href="/book.html" onclick="gtag('event','contact_click',{'method':'booking','location':'notes_cta'});">book a call</a>, or see the <a href="/services/ai-search-era.html">full AI Search Era service page</a> for more anonymised examples.</p>
</div>
