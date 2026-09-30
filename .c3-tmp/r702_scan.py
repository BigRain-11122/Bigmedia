# -*- coding: utf-8 -*-
# R702 #93 media/ 10.2GB layered audit scan (P-20260929-13, resource-chain S3/S11)
import os, subprocess, io, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
MEDIA = r"C:\Users\sjs20\Desktop\FluxGroup\media"
TMP = os.path.join(ROOT, ".c3-tmp")
NOW = time.time()
out = []
def w(s): out.append(s)
def sf(n):
    x = float(n)
    for u in ['B','KB','MB','GB']:
        if x < 1024: return "%.1f%s" % (x, u)
        x /= 1024.0
    return "%.2fTB" % x

def git_lines(args):
    r = subprocess.run(["git"]+args, cwd=ROOT, capture_output=True, timeout=900)
    return r.stdout.decode("utf-8", errors="replace").splitlines()

tracked = set(git_lines(["ls-files"]))
untracked = set(git_lines(["ls-files","--others","--exclude-standard"]))
ignored = set(git_lines(["ls-files","--others","--ignored","--exclude-standard"]))
w("git sets: tracked=%d untracked=%d ignored=%d" % (len(tracked), len(untracked), len(ignored)))

def cat_of(rp, is_git):
    if is_git: return "git"
    if rp in tracked: return "tracked"
    if rp in ignored: return "ignored"
    if rp in untracked: return "untracked"
    return "tracked2"  # inside git dir edge / recheck

def scan_tree(base, label):
    total=0; cnt=0; cats={}; big=[]; topdir={}
    for dirpath, dirnames, filenames in os.walk(base):
        rel = os.path.relpath(dirpath, base)
        is_git = (rel == ".git" or rel.startswith(".git"+os.sep))
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            try: sz = os.path.getsize(fp)
            except OSError: continue
            total += sz; cnt += 1
            rp = os.path.relpath(fp, base).replace("\\","/")
            c = cat_of(rp, is_git)
            cats[c] = cats.get(c,0)+sz
            big.append((sz, rp, c))
            top = rp.split("/")[0] if "/" in rp else "(root)"
            topdir[top] = topdir.get(top,0)+sz
    w("[%s] total=%s files=%d" % (label, sf(total), cnt))
    for c,v in sorted(cats.items(), key=lambda kv:-kv[1]):
        w("  cat %-10s %s" % (c, sf(v)))
    w("  -- top dirs:")
    for t,v in sorted(topdir.items(), key=lambda kv:-kv[1])[:14]:
        w("  %-28s %s" % (t, sf(v)))
    big.sort(reverse=True)
    w("  -- top 30 files:")
    for sz,rp,c in big[:30]:
        w("  %-12s %-8s %s" % (sf(sz), c, rp))
    return big, cats, total

w("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
big, cats, total = scan_tree(ROOT, "BigStream repo")

# media-level siblings (media/.codely-cli etc.)
m_total = 0; m_cnt = 0
for entry in os.listdir(MEDIA):
    fp = os.path.join(MEDIA, entry)
    if os.path.abspath(fp) == ROOT: continue
    if os.path.isfile(fp):
        s = os.path.getsize(fp); m_total += s; m_cnt += 1
        w("[media-sibling] %s %s" % (entry, sf(s)))
    else:
        st=0; cn=0
        for dp,dn,fn in os.walk(fp):
            for f in fn:
                try: st += os.path.getsize(os.path.join(dp,f)); cn+=1
                except OSError: pass
        w("[media-sibling] %s %s files=%d" % (entry, sf(st), cn))
        m_total += st; m_cnt += cn
w("[media total excl BigStream] %s files=%d" % (sf(m_total), m_cnt))

# renders mp4 breakdown (expired-export cleanup-decision face)
rd = os.path.join(ROOT, "output", "renders")
mp4 = []
for f in sorted(os.listdir(rd)):
    fp = os.path.join(rd, f)
    if os.path.isfile(fp):
        mp4.append((os.path.getsize(fp), f))
mp4.sort(reverse=True)
w("-- output/renders files=%d total=%s" % (len(mp4), sf(sum(s for s,_ in mp4))))
for s,f in mp4:
    w("  %-12s %s" % (sf(s), f))

# auto-saves census (candidates)
w("-- auto-saves census (water line: 30d / 500 items, S11 Class-A):")
CANDS = [
    r"C:\Users\sjs20\.codely-cli\auto-saves",
    os.path.join(MEDIA, ".codely-cli", "auto-saves"),
    os.path.join(ROOT, ".codely-cli", "auto-saves"),
    r"C:\Users\sjs20\Desktop\FluxGroup\.codely-cli\auto-saves",
]
for cpath in CANDS:
    if not os.path.exists(cpath):
        w("  ABSENT %s" % cpath); continue
    items = []
    for dp,dn,fn in os.walk(cpath):
        for f in fn:
            fp = os.path.join(dp,f)
            try:
                st = os.stat(fp)
                items.append((st.st_mtime, st.st_size, os.path.relpath(fp, cpath)))
            except OSError: pass
    old = [it for it in items if it[0] < NOW - 30*86400]
    w("  %s items=%d size=%s old30d=%d oldsize=%s newest=%s" % (
        cpath, len(items), sf(sum(it[1] for it in items)), len(old),
        sf(sum(it[1] for it in old)),
        time.strftime("%Y-%m-%d", time.localtime(max(it[0] for it in items))) if items else "-"))
    for it in sorted(items)[:5]:
        w("    oldest %s %s" % (time.strftime("%Y-%m-%d", time.localtime(it[0])), it[2][:100]))

# HF cache (root-cause verification face)
hf = r"C:\Users\sjs20\.cache\huggingface\hub"
if os.path.exists(hf):
    st=0; cn=0; newest=0
    for dp,dn,fn in os.walk(hf):
        for f in fn:
            try:
                s = os.path.getsize(os.path.join(dp,f)); st+=s; cn+=1
                newest = max(newest, os.path.getmtime(os.path.join(dp,f)))
            except OSError: pass
    w("-- hf-cache hub: %s files=%d newest=%s" % (sf(st), cn, time.strftime("%Y-%m-%d %H:%M", time.localtime(newest))))

io.open(os.path.join(TMP, "r702_scan.txt"), "w", encoding="utf-8").write("\n".join(out))
print("SCAN_DONE lines=%d" % len(out))
