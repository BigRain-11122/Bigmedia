import subprocess, os
from PIL import Image, ImageDraw
os.makedirs(r".bs012-tmp\frameverify-r1679", exist_ok=True)
vid = "output/renders/bs-012-v1-shipinhao-60s.mp4"
heads = [0.25, 4.69, 9.50, 14.50, 19.39, 23.70, 29.09, 33.27, 38.77, 43.68, 48.22, 53.01]
cross = [4.30, 4.42, 4.55, 27.75, 27.87, 28.00, 42.82, 42.94, 43.07]
ends = [9.10, 28.70, 43.30]
frames = [("h%02d" % i, t) for i, t in enumerate(heads)] + [("x%02d" % i, t) for i, t in enumerate(cross)] + [("e%02d" % i, t) for i, t in enumerate(ends)]
for name, t in frames:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", vid, "-frames:v", "1",
                    r".bs012-tmp\frameverify-r1679\%s.png" % name], check=True)
CW, CH = 360, 640
cols, rows = 6, 4
tile = Image.new("RGB", (cols * CW, rows * CH), (10, 10, 10))
d = ImageDraw.Draw(tile)
for idx, (name, t) in enumerate(frames):
    im = Image.open(r".bs012-tmp\frameverify-r1679\%s.png" % name).resize((CW, CH))
    x, y = (idx % cols) * CW, (idx // cols) * CH
    tile.paste(im, (x, y))
    d.rectangle([x, y, x + 108, y + 26], fill=(0, 0, 0))
    d.text((x + 6, y + 6), "%s t=%.2f" % (name, t), fill=(0, 255, 120))
tile.save(r".bs012-tmp\frameverify-r1679\tile-24.png")
# two full-res text-integrity samples
for name, t in [("full-hook", 0.30), ("full-b8", 38.90)]:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", vid, "-frames:v", "1",
                    r".bs012-tmp\frameverify-r1679\%s.png" % name], check=True)
print("OK", len(frames), "frames tiled +2 full-res")
