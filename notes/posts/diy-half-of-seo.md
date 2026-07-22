---
title: "You Can DIY Half of This. Here's the Half You Can't."
description: "AI can spot a missing meta description in seconds. It can't tell you which broken thing is actually urgent versus which one just looks urgent."
tag: "practice notes"
date: 2026-07-22
slug: "diy-half-of-seo"
sources:
  - title: "Protecting Staging Environments: the Ultimate Guide"
    url: "https://www.conductor.com/academy/protect-staging-environment/"
    publisher: "Conductor"
---

Most SEO fixes are a Google search away now, or these days, a few prompts to ChatGPT away. Paste in your homepage's HTML and ask what's wrong, and you'll get a decent list back:

* Remove a leftover `noindex` tag from when the site was still in development
* Write an actual meta description instead of leaving it blank
* Add alt text to images so they're readable, not just visible
* Fix a title tag that still says "Home" or the name of whatever platform built the site
* Point a canonical tag at the right page instead of a duplicate
* Add a missing sitemap.xml or fix a robots.txt blocking the wrong folder

Most of it is documented and simple enough to copy. AI tools can spot these problems in seconds too now. **If that's all this was, I wouldn't charge for it. I don't.**

What a checklist, or an AI reading your HTML, cannot do is tell you **which problem is actually urgent and which one only looks urgent.**

<figure>
  <svg viewBox="0 0 680 260" xmlns="http://www.w3.org/2000/svg">
    <text x="0" y="20" font-family="IBM Plex Mono, monospace" font-size="11" fill="#5C615A">what gets caught, and by what</text>
    <rect x="0" y="35" width="325" height="210" rx="10" fill="#F1EFE8" stroke="#B4B2A9" stroke-width="1"/>
    <text x="20" y="62" font-family="Georgia, serif" font-size="14" font-weight="600" fill="#2C2C2A">A checklist, or an AI prompt</text>
    <text x="20" y="90" font-family="Inter, sans-serif" font-size="12" fill="#5F5E5A">Missing meta description</text>
    <text x="20" y="112" font-family="Inter, sans-serif" font-size="12" fill="#5F5E5A">Leftover noindex tag</text>
    <text x="20" y="134" font-family="Inter, sans-serif" font-size="12" fill="#5F5E5A">Broken canonical tag</text>
    <text x="20" y="156" font-family="Inter, sans-serif" font-size="12" fill="#5F5E5A">Missing alt text</text>
    <text x="20" y="178" font-family="Inter, sans-serif" font-size="12" fill="#5F5E5A">Keyword list, ranked by volume</text>
    <text x="20" y="210" font-family="IBM Plex Mono, monospace" font-size="10.5" fill="#5C615A">Fast, cheap, and genuinely useful,</text>
    <text x="20" y="226" font-family="IBM Plex Mono, monospace" font-size="10.5" fill="#5C615A">as far as it goes</text>
    <rect x="355" y="35" width="325" height="210" rx="10" fill="#E7F0EB" stroke="#5DCAA5" stroke-width="1"/>
    <text x="375" y="62" font-family="Georgia, serif" font-size="14" font-weight="600" fill="#04342C">Judgment</text>
    <text x="375" y="90" font-family="Inter, sans-serif" font-size="12" fill="#085041">Which fix is actually urgent</text>
    <text x="375" y="112" font-family="Inter, sans-serif" font-size="12" fill="#085041">A staging link that's really a security gap</text>
    <text x="375" y="134" font-family="Inter, sans-serif" font-size="12" fill="#085041">Zero traffic is a symptom worth chasing</text>
    <text x="375" y="156" font-family="Inter, sans-serif" font-size="12" fill="#085041">Which keyword actually fits the business</text>
    <text x="375" y="178" font-family="Inter, sans-serif" font-size="12" fill="#085041">Whether a fix actually worked</text>
    <text x="375" y="210" font-family="IBM Plex Mono, monospace" font-size="10.5" fill="#085041">Slower, and the part someone</text>
    <text x="375" y="226" font-family="IBM Plex Mono, monospace" font-size="10.5" fill="#085041">has to actually be paid to notice</text>
  </svg>
  <figcaption>Same site, same list of fixes. Only one column tells you what actually matters.</figcaption>
</figure>

A recent audit I ran turned up a "leftover staging link" that an internal team had already flagged and planned to fix with a simple find-and-replace. It wasn't a broken image link. **It was an exposed staging folder with a server error log sitting in public view. A security problem, disguised as an SEO problem.**

That's not a rare mistake. [Staging environments left on a public subdomain risk getting crawled and indexed the same way a live site does](https://www.conductor.com/academy/protect-staging-environment/), which means the "hidden" test folder nobody bothers to lock is often just one Google search away from anyone who knows where to look. The line between a small SEO issue and an exposed internal system is thinner than a checklist shows, or thinner than an AI tool can tell you, since it only matches patterns and doesn't really understand what it's looking at.

This is why [a small canonical tag mistake can quietly cost an organisation real search visibility](/notes/grantmakers-check-your-website-first.html), while looking like nothing on paper. Small technical detail, easy to miss, big consequence.

## There's a layer underneath that one, too

A checklist can only exist once someone already knows what to check for. Before any of the bullet points above get written down, someone has to notice that a site pulling zero traffic despite a decent backlink profile is a symptom worth chasing, not just a slow month. **That's diagnosis, not remediation, and it never shows up on the list itself.** By the time something is on the checklist, the hard part is already done. It's the same with [checking what a crawler actually sees on your own site](/notes/my-own-title-tag-said-notion.html): you only think to check once you stop trusting what looks fine in a browser.

The same split shows up somewhere less dramatic: keyword research. A tool, or a prompt, can hand you a list of search terms ranked by volume in a few seconds. What it won't tell you is which of those terms actually fits where the business is trying to go, whether to chase the broad high-volume search or the narrower one nobody else has claimed yet, whether it's worth writing for an international audience or staying local. **A better prompt doesn't fix this, because it was never really a factual question. It's a business decision, not a technical one.**

That's the difference between reading a list of fixes and knowing which one changes the story. That judgment, plus the discipline to actually verify a fix worked instead of assuming it did, is what I get paid for.

**The checklist is free. Knowing which line on it matters isn't.**

<hr class="rule">

<div class="cta-box">
  <p><strong>Curious what's actually urgent on your own site, versus what just looks urgent?</strong> I offer a free 30-minute look.</p>
  <p class="cta-detail">You'll walk away with one concrete finding, whether or not we end up working together. <a href="mailto:rajnanig22@gmail.com" onclick="gtag('event','contact_click',{'method':'email','location':'notes_cta'});">Get in touch</a> or <a href="/book.html" onclick="gtag('event','contact_click',{'method':'booking','location':'notes_cta'});">book a call</a>.</p>
</div>
