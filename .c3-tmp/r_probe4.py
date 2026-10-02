import io, os, re, subprocess

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(BS, ".c3-tmp", "r_probe4_out.txt")

def rd(p, n=None, tail=False):
    t = io.open(p, encoding="utf-8", errors="replace").read().splitlines()
    if tail:
        t = t[-n:]
    elif n:
        t = t[:n]
    return "\n".join(t)

with io.open(OUT, "w", encoding="utf-8") as f:
    # 1. grep --poster usage
    f.write("== grep --poster in py/md/txt ==\n")
    for root, dirs, files in os.walk(BS):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
        for x in files:
            if x.endswith((".py", ".md", ".txt")):
                p = os.path.join(root, x)
                try:
                    t = io.open(p, encoding="utf-8", errors="replace").read()
                except Exception:
                    continue
                for m in re.finditer(r".{0,120}--poster.{0,200}", t):
                    f.write(p.replace(BS, ".") + " :: " + m.group(0).replace("\n", " | ") + "\n")
    # 2. v20 review doc
    f.write("\n== review-20261002-mcdaily-v20.md (full) ==\n")
    f.write(rd(os.path.join(BS, "docs", "reviews", "review-20261002-mcdaily-v20.md")) + "\n")
    # 3. backlog tail (latest items)
    f.write("\n== backlog tail 60 lines ==\n")
    f.write(rd(os.path.join(BS, "src", "os", "backlog.md"), 60, tail=True) + "\n")
    # 4. finished.md F-105 block
    fm = io.open(os.path.join(BS, "output", "finished.md"), encoding="utf-8", errors="replace").read()
    i = fm.rfind("F-105")
    f.write("\n== finished.md F-105 region (from rfind, 3000 chars) ==\n")
    f.write(fm[i-500:i+3000] + "\n")
    # 5. cards README v20 row + tail
    f.write("\n== cards/README.md tail 40 lines ==\n")
    f.write(rd(os.path.join(BS, "data", "storylines", "cards", "README.md"), 40, tail=True) + "\n")
    # 6. station-reviews tail
    f.write("\n== station-reviews tail 25 lines ==\n")
    f.write(rd(os.path.join(BS, "docs", "reviews", "station-reviews.md"), 25, tail=True) + "\n")
    # 7. queue E30 line
    qt = io.open(os.path.join(BS, "docs", "self-improvement-queue.md"), encoding="utf-8", errors="replace").read()
    f.write("\n== queue E30/D/DAILY mentions ==\n")
    for m in re.finditer(r".{0,80}E30.{0,400}", qt):
        f.write(m.group(0).replace("\n", " | ") + "\n---\n")
print("OK")
