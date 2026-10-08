# Build gate comparison sheets: census ref card vs frames-r1792 character shots
# R1793 formal gate recheck (after Qwen-Image-2.1 full re-roll)
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", "..", "..", ".."))
FRAMES = os.path.join(BASE, "frames-r1792")
CARDS = os.path.join(ROOT, "storylines", "cards")

GROUPS = [
    ("lamp",  "MC-20260926-CENSUS-v19", ["shot02", "shot03", "shot04", "shot12"]),
    ("tower", "MC-20260926-CENSUS-v18", ["shot06", "shot07"]),
    ("cat",   "MC-20260926-CENSUS-v20", ["shot09", "shot10", "shot11"]),
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

def fit(img, target_w):
    r = target_w / img.width
    return img.resize((target_w, int(img.height * r)))

for name, card, shots in GROUPS:
    card_path = os.path.join(CARDS, card, card + ".png")
    ci = Image.open(card_path).convert("RGB")
    ci = fit(ci, 620)
    ci = labeled(ci, "REF " + card)
    ch = ci.height

    cols = 2
    rows = (len(shots) + cols - 1) // cols
    fw = 620
    fx = Image.open(os.path.join(FRAMES, shots[0] + ".png"))
    fh = int(fw * fx.height / fx.width)

    grid_w = cols * (fw + 12) + 12
    grid = Image.new("RGB", (grid_w, rows * (fh + 52) + 12), (24, 24, 24))
    for i, s in enumerate(shots):
        im = Image.open(os.path.join(FRAMES, s + ".png")).convert("RGB")
        im = fit(im, fw)
        im = labeled(im, s)
        x = 12 + (i % cols) * (fw + 12)
        y = 12 + (i // cols) * (fh + 52)
        grid.paste(im, (x, y))

    total_h = max(ch, grid.height) + 24
    total_w = ci.width + grid.width + 36
    sheet = Image.new("RGB", (total_w, total_h), (24, 24, 24))
    sheet.paste(ci, (12, 12))
    sheet.paste(grid, (ci.width + 24, 12))
    out = os.path.join(BASE, "gate-r1792-%s.png" % name)
    sheet.save(out, optimize=True)
    print("OK %s %dx%d -> %s" % (name, sheet.width, sheet.height, out))
