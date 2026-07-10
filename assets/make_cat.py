#!/usr/bin/env python3
"""Draw a clean 'cool cat with sunglasses' (white cat on black) so the ASCII
conversion is crisp and dense like Daksh's, instead of fighting a photo."""

from PIL import Image, ImageDraw

S = 640
im = Image.new("L", (S, S), 0)          # black background
d = ImageDraw.Draw(im)
W = 255                                  # white fur

cx = S // 2

# ---- ears (triangles) --------------------------------------------------
d.polygon([(150, 250), (175, 70), (300, 210)], fill=W)   # left ear
d.polygon([(S-150, 250), (S-175, 70), (S-300, 210)], fill=W)  # right ear
# inner ear shading (subtle)
d.polygon([(190, 215), (200, 130), (270, 205)], fill=170)
d.polygon([(S-190, 215), (S-200, 130), (S-270, 205)], fill=170)

# ---- head + cheeks -----------------------------------------------------
d.ellipse([cx-215, 175, cx+215, 470], fill=W)            # face
# ---- chest / body ------------------------------------------------------
d.ellipse([cx-200, 430, cx+200, 720], fill=225)

# ---- sunglasses (black lenses + bridge + arms) -------------------------
ly = 320
d.ellipse([cx-190, ly-70, cx-30, ly+70], fill=0)         # left lens
d.ellipse([cx+30, ly-70, cx+190, ly+70], fill=0)         # right lens
d.rectangle([cx-40, ly-28, cx+40, ly+8], fill=0)         # bridge
d.line([(cx-190, ly-40), (cx-235, ly-60)], fill=0, width=14)  # left arm
d.line([(cx+190, ly-40), (cx+235, ly-60)], fill=0, width=14)  # right arm

# ---- nose + muzzle -----------------------------------------------------
d.polygon([(cx-16, ly+120), (cx+16, ly+120), (cx, ly+142)], fill=120)  # nose
d.line([(cx, ly+142), (cx, ly+165)], fill=120, width=4)               # philtrum
# whisker dots
for dx in (-70, -95, -120):
    d.ellipse([cx+dx-3, ly+150, cx+dx+3, ly+156], fill=120)
    d.ellipse([cx-dx-3, ly+150, cx-dx+3, ly+156], fill=120)

# ---- raised paw (right side, like the meme) ----------------------------
d.ellipse([S-200, ly-30, S-70, ly+150], fill=235)

im.save("assets/_cat.png")
print("wrote assets/_cat.png")
