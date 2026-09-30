import os, glob, datetime, json

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = []
A = out.append

# 1. mtimes of lc004 tmp files (which are post-R686-commit 14:25)
d = os.path.join(repo, ".lc004-tmp")
A("=== .lc004-tmp mtimes ===")
for p in sorted(os.listdir(d), key=lambda x: os.path.getmtime(os.path.join(d, x))):
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(d, p))).strftime("%H:%M:%S")
    A(f"{mt} {p}")

# 2. renders output for lc-004
A("=== output/renders lc-004 ===")
for p in glob.glob(os.path.join(repo, "output", "renders", "*")):
    b = os.path.basename(p).lower()
    if "lc-004" in b or "lc004" in b:
        A(p.replace(repo, ".") + " | " + datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%H:%M:%S") + f" | {os.path.getsize(p)}")

# 3. key file contents
for rel in (".lc004-tmp/s2-results.md", ".lc004-tmp/render_call.py", ".lc004-tmp/s2_gates.py"):
    p = os.path.join(repo, *rel.split("/"))
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            A(f"===== {rel} =====")
            A(f.read())
    else:
        A(f"MISSING {rel}")

# 4. cards-v1-matched.json + cards.json
for rel in ("data/sources/lc004/cards-v1-matched.json", ".lc004-tmp/cards.json"):
    p = os.path.join(repo, *rel.split("/"))
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            A(f"===== {rel} (mtime {datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%H:%M:%S')}) =====")
            A(f.read()[:2600])
    else:
        A(f"MISSING {rel}")

# 5. source footage params via ffprobe
import subprocess
ft = os.path.join(repo, "data", "sources", "footage", "census-card-v16-vertical.mp4")
r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", ft], capture_output=True, text=True, encoding="utf-8")
try:
    j = json.loads(r.stdout)
    st0 = j["streams"][0]
    A(f"=== v16-vertical ffprobe: {st0.get('codec_name')} {st0.get('width')}x{st0.get('height')} @ {st0.get('avg_frame_rate')} dur={j['format'].get('duration')} ===")
except Exception as ex:
    A("ffprobe err: " + str(ex))

# 6. lc003 render_call.py for comparison (which output name pattern)
with open(os.path.join(repo, ".lc003-tmp", "render_call.py"), encoding="utf-8") as f:
    A("===== .lc003-tmp/render_call.py (reference) =====")
    A(f.read())

# 7. queue E section current state (E lines only)
with open(os.path.join(repo, "docs", "self-improvement-queue.md"), encoding="utf-8") as f:
    q = f.read()
for ln in q.splitlines():
    if ln.strip().startswith("- **E") or ln.strip().startswith("**E"):
        A("Q| " + ln.strip()[:300])

# 8. renders README tail (last 8 lines)
with open(os.path.join(repo, "output", "renders", "README.md"), encoding="utf-8") as f:
    rr = f.read().splitlines()
A("=== renders README last 10 lines ===")
for ln in rr[-10:]:
    A(ln[:240])

with open(os.path.join(repo, ".c3-tmp", "probe-round3.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("WROTE", len(out), "lines")
