"""Generate CI WINNING LTD brand PNGs: og-image (1200x630), apple-touch-icon (180), favicon-32."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = r"E:\zcode-data\ciwinning-website"
NAVY = (7, 22, 52)
NAVY2 = (14, 42, 92)
GOLD = (240, 165, 0)
GOLD_L = (255, 201, 74)
WHITE = (255, 255, 255)

def font(name, size):
    try:
        return ImageFont.truetype(rf"C:\Windows\Fonts\{name}", size)
    except OSError:
        return ImageFont.load_default()

# ---------- OG image 1200x630 ----------
src = Image.open(fr"{BASE}\images\graduation-toss.jpg").convert("RGB")
# cover-crop to 1200x630
tw, th = 1200, 630
ratio = max(tw / src.width, th / src.height)
src = src.resize((int(src.width * ratio) + 1, int(src.height * ratio) + 1))
x = (src.width - tw) // 2
y = (src.height - th) // 2
img = src.crop((x, y, x + tw, y + th))

overlay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
# left-heavy navy gradient via horizontal bands
for i in range(tw):
    a = int(235 * (1 - i / tw) ** 1.35)
    od.line([(i, 0), (i, th)], fill=NAVY + (min(a, 235),))
# slight bottom shade for legibility
od.rectangle([0, th - 140, tw, th], fill=NAVY + (110,))
img = Image.alpha_composite(img.convert("RGBA"), overlay)
d = ImageDraw.Draw(img)

# gold accent bar
d.rounded_rectangle([72, 208, 72 + 110, 218], 5, fill=GOLD)

f_kick = font("seguisb.ttf", 26)
f_title = font("seguisb.ttf", 84)
f_sub = font("segoeui.ttf", 33)
f_small = font("segoeui.ttf", 26)

d.text((74, 156), "UK  ·  NIGERIA  —  EDUCATIONAL SUPPORT SERVICES", font=f_kick, fill=GOLD_L)
d.text((70, 240), "CI WINNING LTD", font=f_title, fill=WHITE)
d.text((74, 352), "Winning Futures Through Global Education", font=f_sub, fill=(214, 226, 244))
d.text((74, 470), "University & Course Guidance   ·   Applications   ·   SOP Support", font=f_small, fill=(190, 205, 230))
d.text((74, 510), "Pre-Departure & Orientation   ·   UK  |  Canada  |  Netherlands", font=f_small, fill=(190, 205, 230))

img.convert("RGB").save(fr"{BASE}\assets\og-image.png", "PNG", optimize=True)
print("og-image.png", img.size)

# ---------- Icon: draw shield+cap at 512 then resize ----------
S = 512
ic = Image.new("RGBA", (S, S), (0, 0, 0, 0))
p = ImageDraw.Draw(ic)

# shield path (polygon approx)
shield = [(256, 24), (468, 92), (468, 250)]
# right side curve to bottom point
curve_r = [(468 - i * 0, 250 + i) for i in range(0, 1)]
pts = []
# build shield outline parametrically
import math
top_l = (44, 92)
top_r = (468, 92)
pts.append((256, 24))
pts += [(44 + (256 - 44) * t, 92 - 68 * (1 - t)) for t in [i / 40 for i in range(41)]]  # already from apex? simpler below
pts = [(256, 24)]
# left edge down
pts.append(top_l)
# left curve to bottom tip
for t in [i / 60 for i in range(61)]:
    # quadratic bezier from top_l to bottom tip (256,488) with ctrl (44, 420)
    x0, y0 = top_l
    cx, cy = 44, 430
    x1, y1 = 256, 488
    bx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1
    by = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1
    pts.append((bx, by))
# right curve back up
for t in [i / 60 for i in range(60, -1, -1)]:
    x0, y0 = top_r
    cx, cy = 468, 430
    x1, y1 = 256, 488
    bx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1
    by = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1
    pts.append((bx, by))
pts.append(top_r)

p.polygon(pts, fill=NAVY2 + (255,))
# gold border
p.line(pts + [pts[0]], fill=GOLD + (255,), width=16, joint="curve")

# cap board (diamond)
cap = [(256, 150), (430, 222), (256, 294), (82, 222)]
p.polygon(cap, fill=WHITE + (255,))
# cap base
p.pieslice([150, 240, 362, 420], 0, 180, fill=WHITE + (230,))
p.rectangle([150, 240, 362, 330], fill=WHITE + (230,))
# tassel
p.line([(430, 222), (430, 320)], fill=GOLD + (255,), width=18)
p.ellipse([408, 318, 452, 362], fill=GOLD + (255,))

for size, name in [(180, "apple-touch-icon.png"), (32, "favicon-32.png"), (192, "icon-192.png")]:
    ic.resize((size, size), Image.LANCZOS).save(fr"{BASE}\assets\{name}", "PNG", optimize=True)
    print(name, size)
print("DONE")
