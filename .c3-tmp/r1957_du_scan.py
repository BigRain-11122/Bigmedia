# r1957: precise du attribution for BigStream #112 reduction plan (read-only scan)
# targets: FluxGroup media/ tree + BigStream repo heavy dirs
import os, sys, io, json, time

def dir_size(path):
    total = 0
    files = 0
    largest = []  # top files
    for root, dirs, files_list in os.walk(path):
        for name in files_list:
            fp = os.path.join(root, name)
            try:
                sz = os.path.getsize(fp)
            except OSError:
                continue
            total += sz
            files += 1
            largest.append((sz, fp))
    largest.sort(reverse=True)
    return total, files, largest

def mb(x):
    return round(x / 1048576.0, 1)

targets = []
media_root = r"C:\Users\sjs20\Desktop\FluxGroup\media"
repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

print("== media/ top-level ==")
rows = []
for entry in sorted(os.scandir(media_root), key=lambda e: e.name):
    if entry.is_dir():
        t, f, _ = dir_size(entry.path)
        rows.append((t, entry.name, f))
    else:
        rows.append((entry.stat().st_size, entry.name + " (file)", 1))
for t, name, f in sorted(rows, reverse=True):
    print(f"{mb(t):>10} MB  {f:>7}f  {name}")
grand = sum(t for t, _, _ in rows)
print(f"{mb(grand):>10} MB  TOTAL media/")

print()
print("== BigStream repo internal (heavy dirs, gitignored faces) ==")
faces = [
    ("data/assets", os.path.join(repo, "data", "assets")),
    ("data/sources", os.path.join(repo, "data", "sources")),
    ("output", os.path.join(repo, "output")),
    ("data/pipeline", os.path.join(repo, "data", "pipeline")),
    ("data/storylines", os.path.join(repo, "data", "storylines")),
    (".c3-tmp", os.path.join(repo, ".c3-tmp")),
    (".aihot-tmp", os.path.join(repo, ".aihot-tmp")),
    ("scratch", os.path.join(repo, "scratch")),
]
repo_rows = []
for label, p in faces:
    if not os.path.isdir(p):
        continue
    t, f, top = dir_size(p)
    repo_rows.append((t, label, f, top))
for t, label, f, top in sorted(repo_rows, reverse=True):
    print(f"{mb(t):>10} MB  {f:>7}f  {label}")
    for sz, fp in top[:4]:
        if sz >= 50 * 1048576:
            print(f"             -> {mb(sz):>9} MB  {os.path.relpath(fp, repo)}")
