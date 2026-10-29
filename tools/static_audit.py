"""Static integrity audit for CI WINNING LTD site — parses real artifacts (L-118)."""
import re, os, sys
from html.parser import HTMLParser

ROOT = r"E:\zcode-data\ciwinning-website"
PAGES = ["index.html", "about.html", "services.html", "destinations.html", "contact.html"]
fails, warns = [], []

class AttrParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.srcs, self.ids = [], [], set()
        self.aria_current = []
        self.tag_stack = []
        self.div_open = self.div_close = 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "href" in d: self.hrefs.append((tag, d["href"]))
        if "src" in d: self.srcs.append((tag, d["src"]))
        if "id" in d: self.ids.add(d["id"])
        if "aria-current" in d: self.aria_current.append(d["aria-current"])
        if tag == "div": self.div_open += 1
    def handle_endtag(self, tag):
        if tag == "div": self.div_close += 1

page_data = {}
for page in PAGES:
    path = os.path.join(ROOT, page)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    p = AttrParser(); p.feed(html)
    page_data[page] = p

    # tag balance
    for t in ["div", "section", "header", "footer", "main", "form", "a", "ul", "li", "details", "summary", "svg", "nav", "span"]:
        o = len(re.findall(rf"<{t}[\s>]", html))
        c = len(re.findall(rf"</{t}>", html))
        # svg/self-closing not expected for these container tags
        if o != c:
            fails.append(f"{page}: <{t}> open={o} close={c} MISMATCH")

# ---- 1. internal page + anchor links ----
id_index = {pg: page_data[pg].ids for pg in PAGES}
for pg in PAGES:
    for tag, href in page_data[pg].hrefs:
        if href.startswith(("http://", "https://", "mailto:", "tel:")) or href == "#":
            continue
        if href.startswith("#"):
            target = href[1:]
            if target and target not in id_index[pg]:
                fails.append(f"{pg}: broken same-page anchor #{target}")
            continue
        # e.g. services.html#course-guidance or css/style.css
        file_part, _, anchor = href.partition("#")
        fp = os.path.join(ROOT, file_part)
        if not os.path.exists(fp):
            fails.append(f"{pg}: broken link -> {href}")
        elif anchor and file_part.endswith(".html"):
            if anchor not in id_index.get(file_part, set()):
                fails.append(f"{pg}: broken cross-page anchor {href}")

# ---- 2. asset refs (src) ----
for pg in PAGES:
    for tag, src in page_data[pg].srcs:
        if src.startswith("http"): continue
        fp = os.path.join(ROOT, src)
        if not os.path.exists(fp):
            fails.append(f"{pg}: missing asset -> {src}")

# ---- 3. image files in CSS ----
with open(os.path.join(ROOT, "css", "style.css"), encoding="utf-8") as f:
    css = f.read()
for m in re.findall(r"url\('([^']+)'\)", css):
    fp = os.path.join(ROOT, "css", m)
    if not os.path.exists(fp):
        fails.append(f"style.css: missing asset -> {m}")

# ---- 4. background-image refs in HTML ----
for pg in PAGES:
    html = open(os.path.join(ROOT, pg), encoding="utf-8").read()
    for m in re.findall(r"background-image:url\('([^']+)'\)", html):
        if not os.path.exists(os.path.join(ROOT, m)):
            fails.append(f"{pg}: missing bg image -> {m}")

# ---- 5. SVG icon path consistency (phone + whatsapp) ----
canon_phone = "M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"
phone_variants, wa_variants = set(), set()
phone_count = wa_count = 0
for pg in PAGES:
    html = open(os.path.join(ROOT, pg), encoding="utf-8").read()
    ds = re.findall(r'<path d="([^"]+)"', html)
    for d in ds:
        if d.startswith("M22 16.92"):
            phone_variants.add(d); phone_count += 1
        if d.startswith("M17.472"):
            wa_variants.add(d); wa_count += 1
# 0 uses = contact info removed (2026-10-18 order); 1 use = re-added consistently
if len(phone_variants) > 1:
    fails.append(f"phone icon path has {len(phone_variants)} distinct variants ({phone_count} uses)")
elif len(phone_variants) == 1 and canon_phone not in phone_variants:
    fails.append(f"phone icon path deviates from canonical (count={phone_count}): {list(phone_variants)[0][:120]}...")
if len(wa_variants) > 1:
    fails.append(f"whatsapp icon path has {len(wa_variants)} distinct variants ({wa_count} uses)")

# ---- 6. aria-current exactly one per page ----
for pg in PAGES:
    n = len(page_data[pg].aria_current)
    if n != 1:
        warns.append(f"{pg}: aria-current count = {n} (expected 1)")

# ---- 7. required content spot-checks (parsed from artifact) ----
must_have = {
    "index.html": ["CI WINNING", "Eligibility", "Personal Statement", "Pre-departure",
                   "Orientation", "Elioparanwo", "+44 7397 267592",
                   "wa.me/447397267592", "ciwinningltd@gmail.com"],
    "contact.html": ["Elioparanwo", "Contact Us Directly", "visit",
                     "+44 7397 267592", "wa.me/447397267592", "ciwinningltd@gmail.com"],
    "services.html": ["course-guidance", "eligibility-assessment", "application-support",
                      "document-preparation", "sop-guidance", "application-followup",
                      "offer-guidance", "pre-departure", "orientation"],
}
for pg, needles in must_have.items():
    html = open(os.path.join(ROOT, pg), encoding="utf-8").read()
    for n in needles:
        if "|" in n:
            if not any(x in html for x in n.split("|")):
                fails.append(f"{pg}: missing any of {n}")
        elif n not in html:
            fails.append(f"{pg}: missing required content -> {n}")

# ---- 8. banned strings: fake claims + unpublished contact info (his order, 2026-10-18) ----
banned = ["since 2015", "since 2010", "10,000+ students", "500+ students", "years of experience",
          "98% success", "visa guaranteed", "100% visa",
          "+44 7823", "+234 703", "794298", "486 5270", "9:00",
          "info@ciwinningltd.com",
          "our offices", "two countries, one team", "port harcourt office",
          "offices in the uk", "nigeria offices", "visit our office", "two offices",
          "offices — uk"]
for pg in PAGES:
    html = open(os.path.join(ROOT, pg), encoding="utf-8").read().lower()
    for b in banned:
        if b in html:
            fails.append(f"{pg}: contains banned claim -> {b}")

print("=" * 60)
if fails:
    print(f"FAIL ({len(fails)}):")
    for f_ in fails: print("  ✗", f_)
else:
    print("ALL STATIC CHECKS PASS ✓")
if warns:
    print(f"WARN ({len(warns)}):")
    for w in warns: print("  ⚠", w)
sys.exit(1 if fails else 0)
