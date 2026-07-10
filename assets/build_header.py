#!/usr/bin/env python3
"""Convert the GitHub avatar into ASCII art and render a Daksh-style
terminal banner as an SVG (ASCII portrait left, info card right)."""

from PIL import Image, ImageOps, ImageEnhance
from html import escape

# ---------------------------------------------------------------- ASCII art
# Cool-cat (clean vector art): bright fur -> dense glyphs, lenses/bg -> empty.
RAMP = " .:-=+*#%@"
COLS = 54                     # character columns in the portrait
ASPECT = 0.52                 # terminal cell h/w correction

img = Image.open("assets/_cat.png").convert("L")
img = img.crop((60, 40, 580, 600))                      # crop to the cat
w, h = img.size
rows = int(COLS * (h / w) * ASPECT)
img = img.resize((COLS, rows))
px = img.load()

lines = []
for y in range(rows):
    row = []
    for x in range(COLS):
        row.append(RAMP[int(px[x, y] / 256 * len(RAMP))])
    lines.append("".join(row).rstrip())

# ---------------------------------------------------------------- info card
RED = "#ff6b6b"       # header labels (Daksh uses a red/pink)
KEY = "#f7768e"       # key labels
VAL = "#c0caf5"       # values
DIM = "#565f89"       # divider / dim
ART = "#7a8299"       # ascii art colour
GREEN = "#9ece6a"     # prompt comment

card = [
    ("hdr",  "ashutosh@GitHub"),
    ("rule", ""),
    ("kv", "Focus",    "Building things that actually ship"),
    ("kv", "Edu",      "B.E. CSE @ BMSIT&M  ·  CGPA 8.7"),
    ("kv", "Roles",    "Full-Stack Dev  ·  GenAI Builder"),
    ("kv", "CP",       "900+ solved on LeetCode"),
    ("kv", "Lang",     "C++  ·  Python  ·  TypeScript  ·  Swift"),
    ("kv", "Web",      "React  ·  Node  ·  Express  ·  FastAPI"),
    ("kv", "Data",     "PostgreSQL  ·  Mongo  ·  Redis  ·  Prisma"),
    ("kv", "AI/ML",    "Claude  ·  OpenAI  ·  Gemini  ·  LangChain"),
    ("kv", "Ships",    "LGTM  ·  PrepNext  ·  AgriSmart"),
    ("gap", ""),
    ("hdr",  "Contact"),
    ("rule", ""),
    ("kv", "Site",     "ashutoshsharma1309.vercel.app"),
    ("kv", "LinkedIn", "in/ashutoshsharma1309"),
    ("kv", "Email",    "ashutoshsharma1395@gmail.com"),
]

# ---------------------------------------------------------------- layout
CH_W, CH_H = 7.55, 15.5       # monospace cell size (px) @ 12.5px font
PAD = 26
ART_X = PAD
CARD_X = PAD + COLS * CH_W + 40
TOP = PAD + 10

# widest card line (label col = 10 chars + value) drives canvas width
card_chars = max([len(v[1]) for v in card if v[0] == "hdr"]
                 + [10 + len(v[2]) for v in card if v[0] == "kv"])

art_h = TOP + len(lines) * CH_H
card_h = TOP + (len(card) + 3) * CH_H
HEIGHT = int(max(art_h, card_h) + PAD + 30)
WIDTH = int(CARD_X + card_chars * CH_W + PAD + 8)

def t(x, y, s, fill, weight="normal"):
    # pin every run to an exact grid width so layout is font-independent
    tl = max(len(s), 1) * CH_W
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-weight="{weight}" '
            f'textLength="{tl:.1f}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve">{escape(s)}</text>')

parts = []
# background window
parts.append(f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="12" fill="#0d0f17"/>')
parts.append(f'<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="11" fill="none" stroke="#1f2335" stroke-width="1.5"/>')
# traffic lights
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{22 + i*20}" cy="18" r="6" fill="{c}"/>')

# ascii art
y = TOP + 26
for ln in lines:
    parts.append(t(ART_X, y, ln, ART))
    y += CH_H

# info card
y = TOP + 26
rule = "─" * 34
for item in card:
    kind = item[0]
    if kind == "hdr":
        parts.append(f'<rect x="{CARD_X-6:.1f}" y="{y-12:.1f}" width="{len(item[1])*CH_W+12:.1f}" height="18" rx="3" fill="{RED}"/>')
        parts.append(t(CARD_X, y, item[1], "#0d0f17", "bold"))
        y += CH_H
    elif kind == "rule":
        parts.append(t(CARD_X, y, rule, DIM))
        y += CH_H
    elif kind == "gap":
        y += CH_H * 0.6
    elif kind == "kv":
        _, k, v = item
        label = (k + ":").ljust(10)
        parts.append(t(CARD_X, y, label, KEY, "bold"))
        parts.append(t(CARD_X + 10 * CH_W, y, v, VAL))
        y += CH_H

# prompt line
py = HEIGHT - PAD
parts.append(t(PAD, py, "ashutosh@dev ~>", KEY, "bold"))
parts.append(t(PAD + 16 * CH_W, py, "# thanks for stopping by :)_", GREEN))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="'JetBrains Mono','Fira Code',Consolas,monospace" font-size="12.5px">
{chr(10).join(parts)}
</svg>'''

with open("assets/header.svg", "w") as f:
    f.write(svg)
print(f"wrote assets/header.svg  ({WIDTH}x{HEIGHT})  ascii {COLS}x{len(lines)}")
