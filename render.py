"""Render the front-page image for news-image-20261121 with PIL.
Deterministic: same bytes every run. Output: entry.png, 1024x1024, <1 MiB."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30
INK = (17, 17, 17)
NAVY = (20, 38, 63)
RED = (185, 28, 28)
GOLD = (243, 201, 105)
GREEN = (22, 101, 52)
TEAL = (14, 116, 144)
AMBER = (146, 64, 14)
LIGHT_GREEN = (238, 244, 234)
GREY = (85, 85, 85)
RULE = (204, 204, 204)

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_BLACK = lambda s: font("NotoSerif-Black.ttf", s)
SERIF_BOLD = lambda s: font("NotoSerif-Bold.ttf", s)
SANS_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def text_w(t, f):
    return d.textlength(t, font=f)

def wrap(t, f, max_w):
    words, lines, cur = t.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(lines, f, x, y, fill=INK, leading=None):
    lh = leading or int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

def centered(t, f, cx, y, fill):
    d.text((cx - text_w(t, f) / 2, y), t, font=f, fill=fill)
    return y + int(f.size * 1.2)

def tag(text, x, y, bg):
    f = SANS_BOLD(15)
    tw = text_w(text, f)
    d.rectangle([x, y, x + tw + 20, y + 26], fill=bg)
    d.text((x + 10, y + 4), text, font=f, fill="white")
    return tw + 20

y = 26
# ---- Masthead ----
d.rectangle([MARGIN, y, W - MARGIN, y + 118], fill=NAVY)
centered("THE WORLD IN ONE IMAGE", SANS_BOLD(15), W // 2, y + 10, GOLD)
centered("THE WORLD", SERIF_BLACK(58), W // 2, y + 30, "white")
centered("SATURDAY  \u00b7  21 NOVEMBER 2026", SANS_BOLD(20), W // 2, y + 88, "white")
y += 118
d.rectangle([MARGIN, y, W - MARGIN, y + 5], fill=RED)
y += 5 + 14

# ---- Lead story ----
tag("WAR IN UKRAINE", MARGIN, y, RED)
y += 26 + 8
lead_head = "Russia fires 400+ drones and 110 missiles at Ukraine; two land in Poland"
y = draw_lines(wrap(lead_head, SERIF_BLACK(40), W - 2 * MARGIN), SERIF_BLACK(40), MARGIN, y, leading=48)
y += 6
lead_sum = ("Overnight strikes kill at least eight in Kyiv and hit bridges and railways. "
            "Warsaw says the missiles that came down on its soil were a deliberate provocation.")
y = draw_lines(wrap(lead_sum, SANS(20), W - 2 * MARGIN), SANS(20), MARGIN, y, leading=27)
y += 10
chips = ["400+ drones", "110 missiles", "8 killed in Kyiv", "2 missiles in Poland"]
cx = MARGIN
cf = SANS_BOLD(17)
for i, c in enumerate(chips):
    tw = text_w(c, cf)
    col = RED if i < 2 else INK
    d.rectangle([cx, y, cx + tw + 20, y + 30], outline=col, width=2)
    d.text((cx + 10, y + 5), c, font=cf, fill=col)
    cx += tw + 20 + 10
y += 30 + 12
d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
y += 14

# ---- Grid 2x2 ----
stories = [
    ("MARKETS", NAVY, "AI sell-off drags S&P 500 into correction",
     "Stocks fall 3.7% on Friday; the Nasdaq drops 5.3%. Nvidia tumbles 14% and Anthropic slides 9% a day after its market debut."),
    ("JUSTICE", RED, "World court: Myanmar committed genocide",
     "In a first, the ICJ holds a state responsible for genocide against the Rohingya. Myanmar calls the ruling \u201cunfair\u201d."),
    ("CLIMATE", TEAL, "COP31 talks run past deadline in Antalya",
     "Nearly 200 nations fail to agree on fossil fuels as the UN climate summit goes into overtime."),
    ("MIDDLE EAST", AMBER, "Houthi attack hits Riyadh\u2019s financial district",
     "Missiles and drones strike the capital\u2019s tallest tower; no one is hurt. Saudi civil defence issues eight emergency alerts."),
]
col_w = (W - 2 * MARGIN - 26) // 2
grid_top = y
row_h = 0
for row in range(2):
    row_y = grid_top + row * 198
    for col in range(2):
        tag_t, bg, head, summ = stories[row * 2 + col]
        x = MARGIN + col * (col_w + 26)
        tag(tag_t, x, row_y, bg)
        hy = row_y + 34
        hy = draw_lines(wrap(head, SERIF_BOLD(25), col_w), SERIF_BOLD(25), x, hy, leading=30)
        hy = draw_lines(wrap(summ, SANS(17), col_w), SANS(17), x, hy + 4, leading=22)
        row_h = max(row_h, hy - row_y)
    d.line([MARGIN, grid_top + row * 198 + 186, W - MARGIN, grid_top + row * 198 + 186], fill=RULE, width=1)
y = grid_top + 2 * 198 + 2

# ---- Health band ----
d.rectangle([MARGIN, y, W - MARGIN, y + 104], fill=LIGHT_GREEN)
d.rectangle([MARGIN, y, MARGIN + 6, y + 104], fill=GREEN)
tag("HEALTH", MARGIN + 18, y + 12, GREEN)
hx = MARGIN + 18 + text_w("HEALTH", SANS_BOLD(15)) + 20 + 12
hy = draw_lines(wrap("Cancer pill trial: tumours undetectable in 1 in 12 patients",
                      SERIF_BOLD(24), W - MARGIN - hx), SERIF_BOLD(24), hx, y + 10, leading=29)
d.text((MARGIN + 18, y + 66),
       "Daraxonrasib shows major progress against pancreatic cancer in trial results reported today.",
       font=SANS(17), fill=INK)
y += 104 + 14

# ---- Ticker ----
d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
y += 8
tick = ("ALSO TODAY  \u00b7  Peru: magnitude 6.7 earthquake  \u00b7  Tbilisi: gas blast kills six  "
        "\u00b7  Seoul: court overturns ex-PM\u2019s sentence")
for ln in wrap(tick, SANS_BOLD(17), W - 2 * MARGIN):
    centered(ln, SANS_BOLD(17), W // 2, y, INK)
    y += 22
y += 4
d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
y += 10
centered("THE WORLD \u2014 SATURDAY 21 NOVEMBER 2026 \u2014 WORLD NEWS IN ONE IMAGE",
         SANS(14), W // 2, y, GREY)
y += 20
assert y <= H, f"layout overflow: y={y}"
print("layout bottom y =", y)

img.save("entry.png", optimize=True)
import os
print("bytes:", os.path.getsize("entry.png"))
