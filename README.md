# CI WINNING LTD — Official Website

Professional website for **CI WINNING LTD** — educational support services helping
students win places at universities in the **United Kingdom**, **Canada**, the
**Netherlands** and beyond, with offices/presence in the **UK** and
**Port Harcourt, Nigeria**.

**Live site:** https://rudra496.github.io/ciwinningltd/

> ℹ️ Contact channels (phone, WhatsApp, email) are being set up and will be added
> to the site the moment they are live. The Port Harcourt office address is on the
> [Contact page](https://rudra496.github.io/ciwinningltd/contact.html).

## Pages
| File | Purpose |
|------|---------|
| `index.html` | Home — hero, stats, why-us, 9 services, destinations, 7-step journey, testimonials, FAQ |
| `about.html` | Story, mission/vision/values, why-choose-us, offices |
| `services.html` | All 9 services in detail (anchor-linked sections) |
| `destinations.html` | UK (flagship), Canada, Netherlands + other destinations on request |
| `contact.html` | Offices, contact-channel status, map of the Port Harcourt office |

## Tech
- Pure **HTML5 + CSS3 + vanilla JavaScript** — no frameworks, no build step, no backend
- Custom SVG logo/favicon, generated social-share image (og-image.png)
- Photos: [Unsplash License](https://unsplash.com/license) — free for commercial use
- Fonts: Sora + Inter via Google Fonts (system fallbacks included)
- SEO: per-page meta/OG tags, JSON-LD organization schema, `sitemap.xml`, `robots.txt`
- Accessibility: skip links, ARIA labels, keyboard-friendly menus, `prefers-reduced-motion` support

## Structure
```
ciwinningltd/
├── index.html · about.html · services.html · destinations.html · contact.html
├── css/style.css        ← design system (colors/fonts as CSS variables)
├── js/main.js           ← nav, scroll reveals, counters, slider, FAQ accordion
├── assets/              ← logo, favicons, og-image
├── images/              ← site photography
└── tools/               ← static audit + brand-asset generator scripts
```

## Run locally
Open `index.html` in a browser, or:
```
python -m http.server 8080
```

## Deployment
Hosted free on **GitHub Pages** (repo root, `main` branch). To move to a custom
domain later: add the domain in repo Settings → Pages, update the `canonical` /
Open Graph / `sitemap.xml` / `robots.txt` URLs from
`https://rudra496.github.io/ciwinningltd/` to the new domain, and add a CNAME file.

## Updating content
All text lives directly in the five HTML files. Brand colors/fonts are CSS
variables at the top of `css/style.css`. When the new contact channels are ready,
they go into: the topbar, contact page cards, footer contact column, and the
floating WhatsApp button slot in each HTML file.

---
© CI WINNING LTD. All rights reserved.
