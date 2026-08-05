---
title: "The Small Grey Text Under a Google Result That Most People Skip"
description: "A page ranking #1 was still getting a below-average click rate. The reason was sitting in plain sight, in small grey text most people scroll straight past."
tag: "practice notes"
date: 2026-08-05
slug: "google-missing-word-serp-snippet"
sources:
  - title: "Google Search / Missing Words"
    url: "https://google.fandom.com/wiki/Google_Search/Missing_Words"
    publisher: "Google Wiki (Fandom)"
---

I was checking rankings for a client's cafe last week when I noticed something under one of their listings, right below the snippet, in small grey text:

<figure>
<svg viewBox="0 0 640 170" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="640" height="170" rx="10" fill="#FFFFFF" stroke="#E1DED4"/>
  <text x="24" y="40" font-family="Georgia, serif" font-size="17" fill="#2F6F5E">A Cafe in Denpasar | Menu, Hours &amp; Location</text>
  <text x="24" y="62" font-family="ui-monospace, monospace" font-size="11.5" fill="#565B54">www.example-cafe.com</text>
  <text x="24" y="90" font-family="Georgia, serif" font-size="13.5" fill="#1C1F1B">Cozy neighbourhood cafe serving coffee, brunch, and pastries.</text>
  <text x="24" y="110" font-family="Georgia, serif" font-size="13.5" fill="#1C1F1B">Open daily from 8am. Dine-in and takeaway available.</text>
  <text x="24" y="138" font-family="ui-monospace, monospace" font-size="12.5" fill="#9A958A">Missing: city</text>
  <text x="112" y="138" font-family="ui-monospace, monospace" font-size="12.5" fill="#9A958A"> | </text>
  <text x="122" y="138" font-family="ui-monospace, monospace" font-size="12.5" fill="#2F6F5E" text-decoration="underline">Show results with: city</text>
</svg>
<figcaption>What most people scroll past without reading.</figcaption>
</figure>

The page was already ranking #1 for the search "[cafe name] denpasar city." First position. But that little note was sitting there anyway, and **the click-through rate on that query was 6.7 percent, well below every other query the site ranked for.**

Turns out this is [a documented Google Search feature](https://google.fandom.com/wiki/Google_Search/Missing_Words) that tells you, directly, in plain language, that the word "city" doesn't appear anywhere in the content it crawled for that page. Not the title, not the description, not the body copy. Google still matched the page to the search because the rest of it was relevant enough, but it's flagging the gap to the person searching too, which is probably why fewer of them bothered clicking through.

I don't see this mentioned much. Most SEO advice is about title tags, meta descriptions, keyword density, the usual list. This is different: **it's Google showing its work, on the actual results page, for free**, and most people scroll right past it because the text is small and grey and easy to mistake for a footnote.

## Why it happens

Usually it's a mismatch between how a business writes about itself and how people actually search for it. A cafe might write "Denpasar" everywhere in its copy but never "Denpasar City," even though that's the exact phrase someone typed. Same city, different phrasing, and Google notices the difference even if a human reader wouldn't. It's the same underlying pattern I keep finding in [larger technical audits](/notes/instagram-scores-100-cafe-scores-9.html): a small, invisible mismatch between the words a business uses and the words a searcher types.

## What to do about it

Pull up your own listings in an incognito window and actually read the grey text under them, not just the blue link and the description. **If you see a "Missing: [word]" note, that's a free instruction from Google:** add that exact word somewhere natural on the page, an address line, a sentence in the description, wherever it fits without sounding forced. It's a small fix, but it's one of the few times Google tells you precisely what's missing instead of making you guess.

Worth checking next time you're auditing anything, not just for new pages, for pages that are already ranking well but underperforming on clicks. **Position #1 doesn't mean the work is done if the click-through rate says otherwise.**

<hr class="rule">

<div class="cta-box">
  <p><strong>If you're not sure whether your own top-ranking pages are quietly leaking clicks like this,</strong> I offer a free 30-minute look at your site.</p>
  <p class="cta-detail">You'll walk away with one concrete finding either way, whether or not we end up working together. <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{'method':'email','location':'notes_cta'});">Get in touch</a> or <a href="/book.html" onclick="gtag('event','contact_click',{'method':'booking','location':'notes_cta'});">book a call</a>, or see the <a href="/services/hospitality.html">full Hospitality service page</a> for more anonymised examples.</p>
</div>
