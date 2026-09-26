# -*- coding: utf-8 -*-
# r431 P-2026-09-26-07 evidence: ollama serve residency + model ladder self-check (12GB tier) + model-large-file law (git scan)
import subprocess, io, os, json, urllib.request, datetime

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(repo)
L = []
def log(s):
    L.append(s); print(s)

now = datetime.datetime.now()
log("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 1) ollama serve residency: API answer + process table + startup autostart lnk
try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=10) as r:
        tags = json.loads(r.read().decode("utf-8"))
    models = sorted(m["name"] for m in tags.get("models", []))
    log("ollama_api_tags_ok=true models=%d" % len(models))
    for m in models:
        log("  model=" + m)
    by_name = {m["name"]: m for m in tags.get("models", [])}
    for n in sorted(by_name):
        d = by_name[n]
        log("  detail=%s size_GB=%.2f family=%s quant=%s ctx=%s" % (
            n, d.get("size", 0) / 1e9, (d.get("details") or {}).get("family", "?"),
            (d.get("details") or {}).get("quantization_level", "?"), (d.get("details") or {}).get("context_length", "?")))
except Exception as e:
    log("ollama_api_tags_ok=false err=%r" % (e,))

r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq ollama.exe"], capture_output=True, text=True, encoding="gbk", errors="replace")
log("ollama_exe_rows=%d" % sum(1 for x in (r.stdout or "").splitlines() if "ollama.exe" in x.lower()))
for x in (r.stdout or "").splitlines():
    if "ollama.exe" in x.lower():
        log("  proc=" + " ".join(x.split()))

lnk = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "Ollama.lnk")
log("startup_lnk=%s path_has_ollama=%s" % (os.path.exists(lnk), "Ollama" in lnk))

# 2) GPU VRAM tier
r = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.used", "--format=csv,noheader"], capture_output=True, text=True)
log("gpu=" + (r.stdout.strip() or "n/a"))

# 3) model large-file law: git tracked big files scan (U187 >95MB absolute ban; scan >50MB)
# ls-files -s -z gives "mode SP sha SP tab path" entries; sizes come from cat-file --batch-check on SHAs
r = subprocess.run(["git", "ls-files", "-s", "-z"], capture_output=True)
entries = []
for tok in r.stdout.split(b"\0"):
    if not tok:
        continue
    line = tok.decode("utf-8", errors="replace")
    head, _, path = line.partition("\t")
    parts = head.split()
    if len(parts) >= 2:
        entries.append((parts[1], path))
log("git_tracked_files=%d" % len(entries))
shas = [e[0] for e in entries]
# ls-tree -r -l HEAD: "<mode> <type> <sha>\t<size>\t<path>" - single command, no stdin quirks
r2 = subprocess.run(["git", "ls-tree", "-r", "-l", "HEAD"], capture_output=True, text=True, encoding="utf-8", errors="replace")
sizes = {}
for line in (r2.stdout or "").splitlines():
    left, tab, path = line.partition("\t")
    if not tab:
        continue
    tok = left.split()
    if len(tok) >= 4 and tok[3].isdigit():
        sizes[path] = int(tok[3])
log("git_size_rows_parsed=%d" % len(sizes))
big50, big95, maxf = [], [], (0, "")
for sha, path in entries:
    sz = sizes.get(path, 0)
    if sz > maxf[0]:
        maxf = (sz, path)
    if sz > 50 * 1024 * 1024:
        big50.append((sz, path))
    if sz > 95 * 1024 * 1024:
        big95.append((sz, path))
log("git_tracked_gt50MB=%d" % len(big50))
log("git_tracked_gt95MB=%d (U187 absolute ban)" % len(big95))
log("git_tracked_max=%dMB %s" % (maxf[0] // 1048576, maxf[1][:80]))
for sz, path in big50[:10]:
    log("  big50=%dMB %s" % (sz // 1048576, path[:80]))
files = [p for _, p in entries]

# 4) model dirs outside git + gitignore coverage + no LFS
piper = os.path.join(repo, "data", "assets", "piper-models")
log("piper_dir_exists=%s" % os.path.isdir(piper))
if os.path.isdir(piper):
    tot = 0
    for root, _, fs in os.walk(piper):
        for fn in fs:
            fp = os.path.join(root, fn)
            try:
                tot += os.path.getsize(fp)
                log("  piper_file=%s %dMB" % (os.path.relpath(fp, piper)[:60], os.path.getsize(fp) // 1048576))
            except OSError:
                pass
    log("piper_total_MB=%d (on-disk, untracked)" % (tot // 1048576))
tracked_assets = [f for f in files if f.startswith("data/assets/")]
log("git_tracked_data_assets=%d" % len(tracked_assets))
log("git_tracked_piper=%d" % len([f for f in files if "piper" in f.lower()]))
r3 = subprocess.run(["git", "check-ignore", "-v", "data/assets/piper-models/model.onnx"], capture_output=True, text=True, encoding="utf-8", errors="replace")
log("git_check_ignore_piper=%s" % ((r3.stdout or "").strip()[:100] if (r3.stdout or "").strip() else "NOT-IGNORED(empty)"))
gi = ""
gip = os.path.join(repo, ".gitignore")
if os.path.exists(gip):
    gi = io.open(gip, encoding="utf-8", errors="replace").read()
log("gitignore_has_piper=%s" % ("piper" in gi))
ga = os.path.join(repo, ".gitattributes")
lfs = False
if os.path.exists(ga):
    lfs = "filter=lfs" in io.open(ga, encoding="utf-8", errors="replace").read()
log("gitattributes_lfs=%s" % lfs)
oll = os.path.join(os.environ.get("USERPROFILE", ""), ".ollama", "models")
log("ollama_models_dir_outside_repo=%s" % (os.path.isdir(oll) and not os.path.normpath(oll).startswith(os.path.normpath(repo))))

with io.open(os.path.join(repo, ".c3-tmp", "r431_p07.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("evidence=.c3-tmp/r431_p07.txt")
