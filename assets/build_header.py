#!/usr/bin/env python3
"""Render a Daksh-style terminal banner as an SVG: ASCII art (from image.txt)
on the left, info card on the right."""

from html import escape

# ---------------------------------------------------------------- ASCII art
# Literal ASCII logo taken verbatim from image.txt.
with open("image.txt") as f:
    lines = [ln.rstrip("\n") for ln in f.read().splitlines()]
lines = [ln for ln in lines if ln.strip()]      # drop blank lines
COLS = max(len(ln) for ln in lines)

# ---------------------------------------------------------------- info card
RED = "#ff6b6b"       # header labels (Daksh uses a red/pink)
KEY = "#f7768e"       # key labels
VAL = "#c0caf5"       # values
DIM = "#565f89"       # divider / dim
ART = "#e2e6f3"       # ascii art colour (bright bat)
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

# ---------------------------------------------------------------- animation
# Timeline (seconds): boot bar -> logo reveal -> card types in -> cursor blink.
BOOT_END   = 1.55      # boot group fades out here
LOGO_T     = 1.85      # first logo line reveals
LOGO_STAG  = 0.045     # per-line stagger
CARD_STAG  = 0.05
REV_DUR    = 0.30      # fade-in duration per line


def fade_in(begin):
    return (f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin:.2f}s" dur="{REV_DUR}s" fill="freeze"/>')


def t(x, y, s, fill, weight="normal", delay=None, anchor=None, grid=True):
    attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'fill="{fill}"',
             f'font-weight="{weight}"']
    if grid:  # pin to the monospace grid so layout is font-independent
        attrs += [f'textLength="{max(len(s),1)*CH_W:.1f}"',
                  'lengthAdjust="spacingAndGlyphs"']
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    inner = ""
    if delay is not None:
        attrs.append('opacity="0"')
        inner = fade_in(delay)
    return (f'<text {" ".join(attrs)} xml:space="preserve">'
            f'{escape(s)}{inner}</text>')


parts = []
# background window
parts.append(f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="12" fill="#0d0f17"/>')
parts.append(f'<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="11" fill="none" stroke="#1f2335" stroke-width="1.5"/>')
# traffic lights
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{22 + i*20}" cy="18" r="6" fill="{c}"/>')

# ---- boot loader (centered), fades away after BOOT_END ------------------
cxm, mid = WIDTH / 2, HEIGHT * 0.44
barw = 260
barx = cxm - barw / 2
boot = []
boot.append(t(cxm, mid - 18, "booting  ashutosh.profile", VAL, "bold",
              anchor="middle", grid=False))
boot.append(f'<rect x="{barx:.1f}" y="{mid:.1f}" width="{barw}" height="13" rx="4" fill="none" stroke="{DIM}"/>')
boot.append(f'<rect x="{barx:.1f}" y="{mid:.1f}" width="0" height="13" rx="4" fill="{GREEN}">'
            f'<animate attributeName="width" from="0" to="{barw}" begin="0.25s" dur="{BOOT_END-0.35:.2f}s" fill="freeze"/></rect>')
boot.append(t(cxm, mid + 33, "loading modules . . .", DIM, anchor="middle", grid=False))
parts.append(f'<g>{"".join(boot)}'
             f'<animate attributeName="opacity" from="1" to="0" begin="{BOOT_END:.2f}s" dur="0.35s" fill="freeze"/></g>')

# ---- ascii logo: reveal line by line -----------------------------------
y = TOP + 26
for i, ln in enumerate(lines):
    parts.append(t(ART_X, y, ln, ART, delay=LOGO_T + i * LOGO_STAG))
    y += CH_H
logo_end = LOGO_T + len(lines) * LOGO_STAG

# ---- info card: types in row by row ------------------------------------
y = TOP + 26
rule = "─" * 34
row = 0
CARD_T = logo_end - 0.25          # start slightly before the logo finishes
def cd():                          # delay for the current card row
    return CARD_T + row * CARD_STAG
for item in card:
    kind = item[0]
    if kind == "hdr":
        d = cd()
        parts.append(f'<rect x="{CARD_X-6:.1f}" y="{y-12:.1f}" width="{len(item[1])*CH_W+12:.1f}" height="18" rx="3" fill="{RED}" opacity="0">{fade_in(d)}</rect>')
        parts.append(t(CARD_X, y, item[1], "#0d0f17", "bold", delay=d))
        y += CH_H; row += 1
    elif kind == "rule":
        parts.append(t(CARD_X, y, rule, DIM, delay=cd()))
        y += CH_H; row += 1
    elif kind == "gap":
        y += CH_H * 0.6
    elif kind == "kv":
        _, k, v = item
        d = cd()
        parts.append(t(CARD_X, y, (k + ":").ljust(10), KEY, "bold", delay=d))
        parts.append(t(CARD_X + 10 * CH_W, y, v, VAL, delay=d))
        y += CH_H; row += 1

# ---- prompt line + blinking cursor -------------------------------------
PROMPT_T = max(logo_end, CARD_T + row * CARD_STAG) + 0.15
py = HEIGHT - PAD
parts.append(t(PAD, py, "ashutosh@dev ~>", KEY, "bold", delay=PROMPT_T))
parts.append(t(PAD + 16 * CH_W, py, "# thanks for stopping by :)", GREEN, delay=PROMPT_T))
cur_x = PAD + (16 + 27) * CH_W
parts.append(f'<rect x="{cur_x:.1f}" y="{py-11:.1f}" width="{CH_W*0.85:.1f}" height="13" fill="{GREEN}" opacity="0">'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.5;1" '
             f'dur="1s" begin="{PROMPT_T+0.25:.2f}s" repeatCount="indefinite"/></rect>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="'JetBrains Mono','Fira Code',Consolas,monospace" font-size="12.5px">
{chr(10).join(parts)}
</svg>'''

with open("assets/header.svg", "w") as f:
    f.write(svg)
print(f"wrote assets/header.svg  ({WIDTH}x{HEIGHT})  ascii {COLS}x{len(lines)}")
