# Build re-gate sheets for R1793 reroll candidates: census REF + 3 candidates per shot
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "reroll-r1793")
ROOT = os.path.normpath(os.path.join(BASE, "..", "..", "..", ".."))
CARDS = os.path.join(ROOT, "storylines", "cards")

JOBS = [
    ("cat09",  "MC-20260926-CENSUS-v20", ["shot09_s19019", "shot09_s19120", "shot09_s19221"]),
    ("lamp12", "MC-20260926-CENSUS-v19", ["shot12_s13013", "shot12_s13114", "shot12_s13215"]),
]

def load_font(size):
    for p in ("C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def labeled(img, text):
    d = ImageDraw.Draw(img)
    f = load_font(28)
    tw = d.textlength(text, font=f)
    d.rectangle([0, 0, tw + 16, 40], fill=(0, 0, 0))
    d.text((8, 6), text, fill=(255, 255, 80), font=f)
    return img

def fit(img, w):
    return img.resize((w, int(img.height * w / img.width)))

for name, card, cands in JOBS:
    ci = Image.open(os.path.join(CARDS, card, card + ".png")).convert("RGB")
    ci = labeled(fit(ci, 620), "REF " + card)
    ch = ci.height
    fw = 620
    fx = Image.open(os.path.join(OUT, cands[0] + ".png"))
    fh = int(fw * fx.height / fx.width)
    grid = Image.new("RGB", (2 * (fw + 12) + 12, 2 * (fh + 52) + 12), (24, 24, 24))
    for i, c in enumerate(cands):
        im = Image.open(os.path.join(OUT, c + ".png")).convert("RGB")
        im = labeled(fit(im, fw), c)
        grid.paste(im, (12 + (i % 2) * (fw + 12), 12 + (i // 2) * (fh + 52)))
    total_h = max(ch, grid.height) + 24
    sheet = Image.new("RGB", (ci.width + grid.width + 36, total_h), (24, 24, 24))
    sheet.paste(ci, (12, 12))
    sheet.paste(grid, (ci.width + 24, 12))
    out = os.path.join(BASE, "gate-r1792-reroll-%s.png" % name)
    sheet.save(out, optimize=True)
    print("OK %s %dx%d" % (name, sheet.width, sheet.height))
