#!/usr/bin/env python3
"""Comic strip composer: overlay caption bands + AIGC notice on an art strip.

PoC tool for the city-storylines comic line (O-20260925-0850, charter S5).
Deterministic, local-only. Chinese texts live in a JSON data file (encoding
rule); this script stays ASCII. Fonts follow visual-spec S1 (msyh family).

Usage:
    python src/render/comic_compose.py --strip <art.png> --texts <texts.json> --out <out.png>
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"


def load_texts(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    n = len(data["panels"])
    if n < 1:
        raise SystemExit("texts.json needs at least one panel")
    return data


def draw_band(draw, y0, y1, w, alpha=170):
    draw.rectangle([0, y0, w, y1], fill=(0, 0, 0, alpha))


def draw_center(draw, text, font, cx, cy, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text,
              font=font, fill=fill)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strip", required=True)
    ap.add_argument("--texts", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    texts = load_texts(args.texts)
    art = Image.open(args.strip).convert("RGBA")
    w, h = art.size
    s = w / 1080.0
    f_title = ImageFont.truetype(FONT_BOLD, int(56 * s))
    f_ep = ImageFont.truetype(FONT_REG, int(30 * s))
    f_cap = ImageFont.truetype(FONT_BOLD, int(42 * s))
    f_sub = ImageFont.truetype(FONT_REG, int(26 * s))
    f_foot = ImageFont.truetype(FONT_REG, int(24 * s))
    f_aigc = ImageFont.truetype(FONT_BOLD, int(26 * s))

    head_h = int(150 * s)
    foot_h = int(100 * s)
    canvas = Image.new("RGBA", (w, h + head_h + foot_h), (0, 0, 0, 255))
    canvas.paste(art, (0, head_h))
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = w // 2

    # header band: series title + episode id
    draw_band(d, 0, head_h, w, 255)
    d.text((int(40 * s), int(34 * s)), texts["title"], font=f_title,
           fill=(255, 255, 255, 255))
    d.text((w - int(40 * s), int(56 * s)), texts["episode"], font=f_ep,
           fill=(200, 200, 200, 255), anchor="ra")

    # AIGC notice chip (top-left of art area, D-BS-03 machine format,
    # brightened per v14 contrast lesson)
    chip_y = head_h + int(20 * s)
    chip_text = texts["aigc"]
    chip_w = d.textbbox((0, 0), chip_text, font=f_aigc)[2] + int(36 * s)
    chip_h = int(52 * s)
    d.rectangle([int(20 * s), chip_y, int(20 * s) + chip_w,
                 chip_y + chip_h], fill=(0, 0, 0, 200))
    d.text((int(38 * s), chip_y + chip_h // 2), chip_text, font=f_aigc,
           fill=(245, 245, 245, 255), anchor="lm")

    # caption bands: one per panel, bottom of its panel
    panel_h = h // len(texts["panels"])
    for i, p in enumerate(texts["panels"]):
        band_h = int(150 * s)
        y0 = head_h + (i + 1) * panel_h - band_h
        if i == len(texts["panels"]) - 1:
            y0 = min(y0, head_h + h - band_h)
        draw_band(d, y0, y0 + band_h, w)
        cap_cy = y0 + int(58 * s)
        sub_cy = y0 + int(112 * s)
        draw_center(d, p["cap"], f_cap, cx, cap_cy, (255, 255, 255, 240))
        draw_center(d, p["sub"], f_sub, cx, sub_cy, (190, 190, 190, 230))

    # footer band
    draw_band(d, canvas.size[1] - foot_h, canvas.size[1], w, 255)
    draw_center(d, texts["footer"], f_foot, cx,
                canvas.size[1] - foot_h // 2, (185, 185, 185, 255))

    out = Image.alpha_composite(canvas, layer).convert("RGB")
    out.save(args.out)
    print("composed:", args.out, out.size)


if __name__ == "__main__":
    main()
