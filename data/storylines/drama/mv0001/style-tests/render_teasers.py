# -*- coding: utf-8 -*-
"""MV-0001《爱在西元前》风格测试片段·渲染腿（PIL 程序化画面 + FFmpeg 动效/剪辑/调色）
5 支片段 × ~18s ·1280x720 ·占位画面（非 AI 图·真图走 bm-c 夜窗）·每支独立调色+节拍剪辑。
CEO 令 P-2026-10-08-05 第四追加令：先出片段看方向。"""
import json, math, pathlib, subprocess, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = pathlib.Path(__file__).parent
CONCEPTS = json.loads((HERE / "concepts.json").read_text(encoding="utf-8"))

W, H = 1600, 900          # 渲染画布（出片 720p 留裁切余量）
FPS = 24
BEAT = 60.0 / 72.0        # 72bpm
SHOT_BEATS = 5
SHOT = BEAT * SHOT_BEATS  # ≈4.167s
ENDCARD = 1.8

def font(name, size, bold=False):
    cands = []
    if bold:
        cands += [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]
    cands += [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]
    for c in cands:
        p = pathlib.Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

F_TITLE = font("yh", 116, bold=True)
F_LOG = font("yh", 46)
F_SMALL = font("yh", 34)
F_TINY = font("yh", 26)

def cjk_w(draw, xy, text, f, fill, anchor="mm"):
    draw.text(xy, text, font=f, fill=fill, anchor=anchor)

# ---------- 程序化画面元素 ----------
def wedge_row(d, x0, y0, w, n, size, color, rng):
    """楔形文字风刻痕带（三角+杆·随机朝向）"""
    step = w / max(n, 1)
    for i in range(n):
        x = x0 + step * i + rng.uniform(-step*0.2, step*0.2)
        y = y0 + rng.uniform(-8, 8)
        a = rng.choice([0, 90, 180, 270]) + rng.uniform(-12, 12)
        r = math.radians(a)
        # 杆
        d.line([(x, y), (x+math.cos(r)*size*1.6, y+math.sin(r)*size*1.6)], fill=color, width=max(2, size//4))
        # 三角头
        hx, hy = x+math.cos(r)*size*1.6, y+math.sin(r)*size*1.6
        px, py = -math.sin(r)*size*0.5, math.cos(r)*size*0.5
        d.polygon([(hx, hy), (hx+px, hy+py), (hx+px*0.2-math.cos(r)*size*0.4, hy+py*0.2-math.sin(r)*size*0.4)], fill=color)

def ziggurat(d, cx, base_y, w, steps, color, alpha):
    """阶梯神塔剪影"""
    ov = Image.new("RGBA", d._image.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    sw, sh = w, w * 0.12
    y = base_y
    for i in range(steps):
        dd.rectangle([cx-sw/2, y-sh, cx+sw/2, y], fill=color + (alpha,))
        y -= sh
        sw *= 0.72
    d._image.paste(ov, (0, 0), ov) if hasattr(d, "_image") else None
    return ov

def draw_ziggurat(img, cx, base_y, w, steps, color):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    sw, sh = w, w * 0.14
    y = base_y
    for _ in range(steps):
        dd.rectangle([cx-sw/2, y-sh, cx+sw/2, y], fill=color)
        y -= sh
        sw *= 0.72
    return Image.alpha_composite(img, ov)

def ripples(d, cx, cy, n, maxr, color, width=2, decay=0.82):
    """水波同心弧（逆流感）"""
    for i in range(1, n+1):
        r = maxr * (i / n) ** 1.4
        a = int(200 * (decay ** i))
        d.arc([cx-r, cy-r*0.62, cx+r, cy+r*0.62], 190, 350, fill=color[:3] + (a,) if len(color) > 3 else color, width=width)

def star_field(img, rng, n, tint_gold):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H*0.82)
        r = rng.choice([1, 1, 2, 2, 3])
        a = rng.randint(70, 220)
        c = tint_gold if rng.random() < 0.22 else (210, 225, 245)
        dd.ellipse([x-r, y-r, x+r, y+r], fill=c + (a,))
    return Image.alpha_composite(img, ov)

# ---------- 五种风格渲染 ----------
def base(bg_top, bg_bot):
    img = Image.new("RGBA", (W, H))
    grad = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / H
        grad.putpixel((0, y), tuple(int(bg_top[i]*(1-t) + bg_bot[i]*t) for i in range(3)))
    img = grad.resize((W, H)).convert("RGBA")
    return img, ImageDraw.Draw(img, "RGBA")

def render_frame(style_id, c, shot_idx, rng):
    """每风格 4 帧：构图随 shot 微变（推拉基础上的变化由 ffmpeg zoompan 承担·帧间构图有差异）"""
    img, d = None, None
    if style_id == 1:  # 时空织锦·冷岩+金
        img, d = base((24, 30, 40), (10, 12, 18))
        for row in range(4):
            wedge_row(d, 140, 240 + row*150, W-280, 26 - row*4, 14, (196, 168, 110, 200), rng)
        d.line([(120, 118), (W-120, 118)], fill=(196, 168, 110, 90), width=2)
        d.line([(120, 770), (W-150, 770)], fill=(196, 168, 110, 90), width=2)
    elif style_id == 2:  # 梦回巴比伦·深蓝+金
        img, d = base((8, 16, 38), (2, 4, 12))
        img = star_field(img, rng, 130, (232, 200, 120))
        d = ImageDraw.Draw(img, "RGBA")
        img = draw_ziggurat(img, W//2 + (shot_idx-1.5)*60, 760, 520, 5, (232, 200, 120, 210))
        d = ImageDraw.Draw(img, "RGBA")
        # 星座连线
        pts = [(rng.uniform(120, W-120), rng.uniform(90, 320)) for _ in range(6)]
        for i in range(len(pts)-1):
            d.line([pts[i], pts[i+1]], fill=(140, 170, 220, 70), width=1)
    elif style_id == 3:  # 逆流记忆·冷白蓝
        img, d = base((30, 42, 56), (8, 12, 20))
        cx, cy = W//2, 470
        for i in range(1, 9):
            r = 90 * i
            a = max(30, 150 - i*16)
            d.arc([cx-r, cy-int(r*0.6), cx+r, cy+int(r*0.6)], 180, 360, fill=(180, 205, 235, a), width=2)
        # 橱窗竖框
        d.rectangle([W//2-330, 130, W//2+330, 770], outline=(215, 228, 245, 160), width=3)
        d.line([(W//2, 150), (W//2, 750)], fill=(215, 228, 245, 70), width=1)
        # 双剪影（简约·高级留白）
        for x, s in [(W//2-120, 1.0), (W//2+120, 1.06)]:
            hh = 130*s
            d.ellipse([x-16*s, 610-hh, x+16*s, 610-hh+32*s], fill=(20, 26, 36, 255))
            d.polygon([(x-26*s, 610), (x+26*s, 610), (x+18*s, 610-hh+30*s), (x-18*s, 610-hh+30*s)], fill=(20, 26, 36, 255))
    elif style_id == 4:  # 书卷长歌·土黄+深红（简牍卷轴）
        img, d = base((92, 74, 48), (54, 40, 24))
        for k in range(9):  # 简牍纵列
            x = 120 + k*152
            d.rectangle([x, 100, x+128, H-120], fill=(126, 100, 64, 255))
            d.rectangle([x, 100, x+128, H-120], outline=(60, 42, 24, 255), width=2)
            for row in range(7):
                wedge_row(d, x+14, 168 + row*96, 100, 3, 9, (58, 40, 22, 235), rng)
        d.rectangle([W-260, 620, W-140, 740], fill=(158, 42, 38, 235))  # 印章
        cjk_w(d, (W-200, 680), "西元\n之前", F_SMALL, (238, 226, 200, 255))
    else:  # 5 神殿遗梦·暗红+金
        img, d = base((44, 16, 18), (12, 5, 6))
        img = draw_ziggurat(img, W//2, 860, 900, 3, (255, 196, 120, 26))
        d = ImageDraw.Draw(img, "RGBA")
        # 神殿门（大三角+内门）
        d.polygon([(W//2-380, 840), (W//2, 180), (W//2+380, 840)], outline=(232, 190, 120, 220), width=4)
        d.polygon([(W//2-120, 840), (W//2, 420), (W//2+120, 840)], fill=(18, 7, 8, 255))
        for _ in range(26):  # 火星
            x, y = rng.uniform(W//2-300, W//2+300), rng.uniform(200, 820)
            r = rng.choice([1, 2])
            d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 190, 110, rng.randint(80, 200)))
    # 公共排版：题名+立意+锚（构图避让：标题下移出 zoom 裁切区·文字在上下安全区）
    d = ImageDraw.Draw(img, "RGBA")
    y0 = 150
    cjk_w(d, (W//2, y0), c["title"], F_TITLE, (245, 243, 236, 235))
    cjk_w(d, (W//2, y0 + 100), c["logline"], F_LOG, (235, 230, 218, 205))
    cjk_w(d, (W//2, H - 62), "锚点：" + c["anchor"], F_SMALL, (225, 218, 200, 170))
    cjk_w(d, (120, H - 62), "AI 立意", F_TINY, (200, 196, 184, 120), anchor="lm")
    cjk_w(d, (W - 120, H - 62), "风格测试 %d/5" % style_id, F_TINY, (200, 196, 184, 120), anchor="rm")
    return img.convert("RGB")

def endcard(style_id, c):
    img, d = base((14, 14, 18), (6, 6, 9))
    cjk_w(d, (W//2, 380), c["title"], F_TITLE, (245, 243, 236, 230))
    cjk_w(d, (W//2, 500), "程序化占位画面 · AI 立意已入档 · 完整版换 AI 图", F_LOG, (225, 220, 208, 190))
    cjk_w(d, (W//2, 580), "风格测试 %d/5 · 无声占位" % style_id, F_SMALL, (200, 196, 184, 150))
    return img.convert("RGB")

# ---------- 调色（每风格独立·高级感=低饱和+分区）
GRADES = {
    1: "eq=saturation=0.55:contrast=1.07:brightness=-0.01,colorbalance=bs=0.07:bm=0.04:rs=-0.02,curves=all='0/0.03 0.5/0.52 1/0.97'",
    2: "eq=saturation=0.72:contrast=1.06,colorbalance=bs=0.10:bm=0.06:rm=-0.03,curves=all='0/0.04 0.5/0.5 1/0.96'",
    3: "eq=saturation=0.42:contrast=1.05:brightness=0.02,colorbalance=bs=0.09:bm=0.05,curves=all='0/0.05 0.5/0.54 1/1'",
    4: "eq=saturation=0.62:contrast=1.08,colorbalance=rs=0.09:gs=-0.03:bs=-0.03,curves=all='0/0.02 0.5/0.5 1/0.98'",
    5: "eq=saturation=0.68:contrast=1.12:brightness=-0.03,colorbalance=rs=0.12:bm=0.05:bs=-0.05,curves=all='0/0.02 0.5/0.48 1/0.95'",
}

def zoom_expr(direction, frames):
    if direction > 0:
        return f"z='min(1+0.0009*on,{1+0.0009*frames:.3f})'"
    return f"z='max(1.10-0.001*on,1.001)'"

def make_segment(style_id, c, rng):
    frames_dir = HERE / f"frames_{style_id}"
    frames_dir.mkdir(exist_ok=True)
    paths = []
    for shot in range(4):
        img = render_frame(style_id, c, shot, rng)
        p = frames_dir / f"s{style_id}_{shot}.png"
        img.save(p)
        paths.append(p)
    ec = frames_dir / f"s{style_id}_end.png"
    endcard(style_id, c).save(ec)

    seg_len = SHOT * 4 + ENDCARD
    nshots = int(SHOT * FPS)
    nend = int(ENDCARD * FPS)
    total_beats = int(seg_len / BEAT)
    beat_pts = ",".join(f"{i*BEAT:.4f}" for i in range(total_beats))
    # 脉冲底鼓（72bpm·弱）
    audio = f"aevalsrc='0.30*exp(-16*mod(t\\,{BEAT:.4f}))*sin(2*PI*52*mod(t\\,{BEAT:.4f}))':s=44100:d={seg_len:.3f},volume=-13dB,afade=t=in:d=0.5,afade=t=out:st={seg_len-1.2:.2f}:d=1.2"

    parts = []
    for i, p in enumerate(paths):
        z = zoom_expr(1 if i % 2 == 0 else -1, nshots)
        parts.append(
            f"[{i}:v]scale=1920:1080,zoompan={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nshots}:s=1280x720:fps={FPS}[v{i}]")
    parts.append(f"[4:v]scale=1280:720,zoompan=z='min(1+0.0004*on,1.02)':d={nend}:s=1280x720:fps={FPS}[v4]")
    xfade_parts = []
    # 硬切接 beat：每镜头正好 5 拍·concat 即可（切点天然在拍上）
    parts.append("".join(f"[v{i}]" for i in range(5)) + f"concat=n=5:v=1:a=0[vcat]")
    parts.append(f"[vcat]{GRADES[style_id]},noise=alls=5:allf=t,vignette=PI/5,format=yuv420p[vout]")
    fc = ";".join(parts)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for p in paths:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(ec)]
    cmd += ["-f", "lavfi", "-t", f"{seg_len:.3f}", "-i", audio]
    cmd += ["-filter_complex", fc, "-map", "[vout]", "-map", "5:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "21",
            "-c:a", "aac", "-b:a", "128k", "-shortest",
            str(HERE / f"MV0001_style{style_id}_{c['title']}.mp4")]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("FFMPEG_FAIL", style_id, r.stderr[-600:])
        sys.exit(1)
    print("SEG OK", style_id, c["title"], f"{seg_len:.1f}s")

def main():
    rng = random.Random(20261008)
    for c in CONCEPTS:
        make_segment(c["id"], c, rng)
    print("ALL DONE ->", HERE)

if __name__ == "__main__":
    main()
