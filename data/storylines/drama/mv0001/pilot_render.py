# -*- coding: utf-8 -*-
"""MV-0001 试跑渲染器：真音轨+结构对轴+细颗粒视觉（两支试跑：开场段/副歌刻字段）
消费：structure.json（节拍/段落/whisper 行）+ ai-zai-xi-yuan-qian.wav（CEO 曲库真音源）"""
import json, math, pathlib, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).parent
DST = pathlib.Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\sources\mv001")
MV = DST.parent.parent / "storylines" / "drama" / "mv0001"
PILOTS = MV / "pilots"
PILOTS.mkdir(parents=True, exist_ok=True)
WAV = DST / "ai-zai-xi-yuan-qian.wav"
ST = json.loads((DST / "structure.json").read_text(encoding="utf-8"))
W, H, FPS = 1600, 900, 24

def font(size, bold=False):
    for c in (["C:\\Windows\\Fonts\\msyhbd.ttc", "C:\\Windows\\Fonts\\simhei.ttf"] if bold else []) + \
             ["C:\\Windows\\Fonts\\msyh.ttc", "C:\\Windows\\Fonts\\simhei.ttf"]:
        p = pathlib.Path(c)
        if p.exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

F_T = font(96, True); F_S = font(40); F_XS = font(28)

def base(top, bot):
    img = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / H
        img.putpixel((0, y), tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3)))
    img = img.resize((W, H)).convert("RGBA")
    return img, ImageDraw.Draw(img, "RGBA")

def wedges(d, x0, y0, w, rows, size, color, rng, gap=26):
    for r in range(rows):
        y = y0 + r * gap
        if y > y0 + rows * gap:
            break
        n = int(w / (size * 3.2))
        for i in range(n):
            x = x0 + (i + rng.uniform(-0.15, 0.15)) * (w / n)
            a = rng.choice([0, 180]) + rng.uniform(-16, 16)
            rad = math.radians(a)
            d.line([(x, y), (x+math.cos(rad)*size*1.7, y+math.sin(rad)*size*1.7)],
                   fill=color, width=max(2, size//4))
            hx, hy = x+math.cos(rad)*size*1.7, y+math.sin(rad)*size*1.7
            px, py = -math.sin(rad)*size*0.5, math.cos(rad)*size*0.5
            d.polygon([(hx, hy), (hx+px, hy+py),
                       (hx+px*0.2-math.cos(rad)*size*0.45, hy+py*0.2-math.sin(rad)*size*0.45)], fill=color)

def stele(img, cx, top, w_, h_, line=(232, 200, 130)):
    """汉谟拉比法典式圆顶石碑（考证：圆顶+顶部浮雕区）"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    r = w_ / 2
    dd.pieslice([cx-r, top, cx+r, top+2*r], 180, 360, fill=(44, 38, 32, 255))            # 圆顶
    dd.rectangle([cx-r, top+r, cx+r, top+h_], fill=(40, 35, 29, 255))                      # 碑身（侧光体）
    # 左侧受光面（顶光斜打·立体感）
    dd.polygon([(cx-r, top+r), (cx-r*0.72, top+r), (cx-r*0.86, top+h_), (cx-r, top+h_)],
               fill=(58, 50, 40, 255))
    # 顶部浮雕区（沙玛什与汉谟拉比剪影·简化两坐像）
    dd.ellipse([cx-r*0.55, top+r*0.25, cx-r*0.15, top+r*0.75], fill=line+(120,))
    dd.ellipse([cx+r*0.18, top+r*0.30, cx+r*0.52, top+r*0.78], fill=line+(120,))
    # 金边光
    dd.arc([cx-r, top, cx+r, top+2*r], 180, 360, fill=line+(230,), width=4)
    dd.line([(cx-r, top+r), (cx-r, top+h_)], fill=line+(150,), width=3)
    dd.line([(cx+r, top+r), (cx+r, top+h_)], fill=line+(150,), width=3)
    out = Image.alpha_composite(img, ov)
    d = ImageDraw.Draw(out, "RGBA")
    rng = random.Random(7)
    wedges(d, cx-r*0.78, top+r*1.35, r*1.56, 26, 9, line+(150,), rng, gap=int((h_-r*1.6)/26))
    return out

def tablet(img, cx, cy, w_, h_, glow=True):
    """暖泥板（软·私人·材质词②）"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    dd.rounded_rectangle([cx-w_/2, cy-h_/2, cx+w_/2, cy+h_/2], radius=int(w_*0.07),
                         fill=(146, 108, 66, 255), outline=(96, 68, 38, 255), width=3)
    rng = random.Random(11)
    d = ImageDraw.Draw(ov, "RGBA")
    rows = 7
    wedges(d, cx-w_*0.38, cy-h_*0.36, w_*0.76, rows, 8, (70, 46, 24, 235), rng, gap=int(h_*0.72/rows))
    out = Image.alpha_composite(img, ov)
    if glow:
        d2 = ImageDraw.Draw(out, "RGBA")
        d2.rounded_rectangle([cx-w_/2-8, cy-h_/2-8, cx+w_/2+8, cy+h_/2+8],
                             radius=int(w_*0.08), outline=(255, 214, 140, 110), width=3)
    return out

def hands_over_tablet(img, cx, cy, w_, h_):
    """掌心相覆剪影（峰值帧·两剪影交叠于泥板上）"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    s = w_ * 0.30
    for dx, dy, a in [(-s*0.35, -s*0.18, 120), (s*0.35, -s*0.05, 235)]:
        dd.ellipse([cx+dx-s*0.5, cy+dy-s*0.30, cx+dx+s*0.5, cy+dy+s*0.42], fill=(24, 18, 12, 235))
        dd.polygon([(cx+dx-s*0.5, cy+dy+s*0.05), (cx+dx-s*0.1, cy+dy-s*0.55),
                    (cx+dx+s*0.5, cy+dy+s*0.05)], fill=(24, 18, 12, 235))
    return Image.alpha_composite(img, ov)

def sand_strata(img, rng):
    """沙层漫延（B 池·地层）"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    for i in range(5):
        y = 520 + i * 72
        dd.line([(0, y), (W, y)], fill=(210, 176, 120, 70+i*26), width=3)
    for _ in range(160):
        x, y = rng.uniform(0, W), rng.uniform(500, H)
        dd.point((x, y), fill=(226, 198, 148, rng.randint(60, 170)))
    return Image.alpha_composite(img, ov)

def title_card(text, sub):
    img, d = base((12, 12, 15), (5, 5, 7))
    d.text((W//2, H//2 - 40), text, font=F_T, fill=(245, 243, 236, 235), anchor="mm")
    d.text((W//2, H//2 + 66), sub, font=F_S, fill=(225, 218, 200, 185), anchor="mm")
    d.text((W//2, H - 46), "试跑片段 · 程序化占位画面 · 真音轨", font=F_XS, fill=(190, 186, 176, 140), anchor="mm")
    return img.convert("RGB")

def frame_A(shot):
    """开场段·玄武岩黑金单色场"""
    rng = random.Random(100 + shot)
    img, d = base((16, 15, 14), (6, 6, 5))
    if shot == 0:   # 黑场一束顶光→碑巨影
        img = stele(img, W//2, 150, 560, 660)
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(28):  # 顶光尘
            d.point((rng.uniform(W*0.3, W*0.7), rng.uniform(120, 760)), fill=(255, 226, 168, rng.randint(40, 120)))
    elif shot == 1:  # 碑面楔形刻痕下移
        img = stele(img, W//2, -320, 620, 1200)
        d = ImageDraw.Draw(img, "RGBA")
        d.line([(W*0.18, 0), (W*0.18, H)], fill=(0, 0, 0, 0), width=1)
    elif shot == 2:  # 三千七百多年·地层叠化
        for i, a in enumerate([30, 55, 85, 120]):
            d.rectangle([0, H-110-i*0, W, H-110-i*0], fill=(0, 0, 0, 0))
        img2 = sand_strata(img, rng)
        d = ImageDraw.Draw(img2, "RGBA")
        d.text((W//2, 170), "距今已经三千七百多年", font=F_S, fill=(214, 196, 158, 200), anchor="mm")
        img = img2
    else:          # 碑底阴影里的小泥板（材质对照）
        img = stele(img, W//2, 90, 470, 560)
        img = tablet(img, W//2, 730, 190, 130)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((W//2, 848), "王的石碑 · 恋人的泥板", font=F_XS, fill=(206, 190, 156, 150), anchor="mm")
    return img.convert("RGB")

def frame_C(shot):
    """副歌段·刻字仪式→深埋（A→B 池）"""
    rng = random.Random(200 + shot)
    if shot == 0:   # 起刀（刻字之手·慢放位）
        img, d = base((20, 16, 12), (8, 6, 5))
        img = tablet(img, W//2, 560, 760, 470, glow=False)
        d = ImageDraw.Draw(img, "RGBA")
        d.polygon([(W//2-60, 300), (W//2+40, 420), (W//2-10, 452), (W//2-90, 340)], fill=(232, 200, 130, 220))
        d.line([(W//2-30, 386), (W//2+26, 560)], fill=(196, 158, 96, 200), width=6)
    elif shot == 1:  # 楔形笔画成形特写
        img, d = base((146, 108, 66), (54, 38, 24))
        d2 = ImageDraw.Draw(img, "RGBA")
        wedges(d2, W*0.2, 220, W*0.6, 8, 26, (58, 38, 20, 240), rng, gap=64)
        d.line([(W*0.5, 0), (W*0.5, H)], fill=(0, 0, 0, 0), width=1)
    elif shot == 2:  # 掌心相覆（峰值帧·9/10）
        img, d = base((26, 20, 14), (10, 8, 6))
        img = tablet(img, W//2, 520, 700, 430)
        img = hands_over_tablet(img, W//2, 500, 700, 430)
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(36):
            d.point((rng.uniform(W*0.28, W*0.72), rng.uniform(300, 700)),
                    fill=(255, 216, 150, rng.randint(50, 150)))
        d.text((W//2, 120), "用楔形文字刻下了永远", font=F_T, fill=(245, 238, 222, 235), anchor="mm")
    else:          # 黄沙漫延覆板（B 池过渡·俯拍）
        img, d = base((36, 30, 22), (18, 14, 10))
        img = tablet(img, W//2, 430, 560, 340, glow=False)
        img = sand_strata(img, rng)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((W//2, 810), "深埋在美索不达米亚平原", font=F_S, fill=(224, 208, 176, 195), anchor="mm")
    return img.convert("RGB")

GRADES = {
    "A": "eq=saturation=0.52:contrast=1.12:brightness=-0.02,colorbalance=rs=0.05:bm=0.06:bs=0.05,curves=all='0/0.02 0.5/0.5 1/0.97'",
    "C1": "eq=saturation=0.78:contrast=1.06,colorbalance=rs=0.06:bm=0.04:bs=0.06,curves=all='0/0.03 0.5/0.52 1/0.98'",
    "C2": "eq=saturation=0.62:contrast=1.04,colorbalance=rs=0.10:gs=-0.02:bs=-0.02,curves=all='0/0.04 0.5/0.53 1/0.99'",
}

def build(name, t0, t1, frames_fn, grade, shots_n, title, sub):
    seg = t1 - t0
    beat = max(ST["beat"], 0.4)
    shot_len = max(beat * 8, 2.6)            # 每镜 8 拍
    n = shots_n
    real_n = max(2, int(seg / shot_len))
    fs = []
    for i in range(min(n, real_n + 1)):
        p = PILOTS / f"{name}_{i}.png"
        img = frames_fn(i % shots_n)
        img.save(p); fs.append(p)
    # 每镜时长按剩余均分（首末各留 0.3s 淡入出）
    per = seg / len(fs)
    parts = []
    for i, p in enumerate(fs):
        frames = max(int(per * FPS), 1)
        z = f"z='min(1+0.0009*on,{1+0.0009*frames:.3f})'" if i % 2 == 0 else "z='max(1.10-0.001*on,1.001)'"
        parts.append(f"[{i}:v]scale=1920:1080,zoompan={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                     f"d={frames}:s=1280x720:fps={FPS}[v{i}]")
    parts.append("".join(f"[v{i}]" for i in range(len(fs))) + "concat=n=%d:v=1:a=0[vc]" % len(fs))
    parts.append(f"[vc]fade=t=in:d=0.35,fade=t=out:st={seg-0.5:.2f}:d=0.5,{GRADES[grade]},"
                 f"noise=alls=5:allf=t,vignette=PI/5,format=yuv420p[vout]")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for p in fs:
        cmd += ["-i", str(p)]
    cmd += ["-ss", f"{t0:.2f}", "-t", f"{seg:.2f}", "-i", str(WAV),
            "-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{len(fs)}:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(PILOTS / f"MV0001_pilot_{name}.mp4")]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FAIL", name, r.stderr[-500:]); sys.exit(1)
    print("PILOT OK", name, f"{seg:.1f}s", "shots", len(fs))

def chorus_window():
    """副歌窗口：whisper 行含「西元」关键词优先；否则取能量最高段中段 24s"""
    for l in ST.get("lines", []):
        if ("西元" in l["text"] or "元前" in l["text"]) and l["end"] - l["start"] > 4:
            return l["start"] - 2.5, l["end"] + 1.5
    secs = sorted(ST["sections"], key=lambda s: -s["db"])
    s = secs[0]
    return s["s"], min(s["e"], s["s"] + 26)

def main():
    dur = ST["duration"]
    # 试跑 1：rap 开场段（真词窗 28-51s：法典→距今→橱窗→凝视链）
    build("intro", 28.0, 51.0, frame_A, "A", 4, "爱在西元前", "试跑·开场段")
    # 试跑 2：副歌刻字段（真词窗 76-110s：写在西元前→深埋→刻下了永远→一切又重演）
    build("chorus", 76.0, 110.0, frame_C, "C1", 4, "爱在西元前", "试跑·副歌刻字段")
    print("ALL PILOTS DONE ->", PILOTS)

if __name__ == "__main__":
    main()
