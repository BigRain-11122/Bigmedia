# -*- coding: utf-8 -*-
# R702 #93 execute: Class-A direct clear of _trash-20260928 (trashed auto-saves staging)
# + historical-renders bucket quantification for cleanup-decision suggestion face
import os, io, time, shutil

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
out = []
def w(s): out.append(s)
def sf(n):
    x = float(n)
    for u in ['B','KB','MB','GB']:
        if x < 1024: return "%.1f%s" % (x, u)
        x /= 1024.0
    return "%.2fTB" % x

TRASH = os.path.join(ROOT, ".codely-cli", "_trash-20260928")
# safety: verify the trash contains ONLY auto-saves staging before clearing
entries = os.listdir(TRASH)
sub = os.path.join(TRASH, "auto-saves")
assert entries == ["auto-saves"], "unexpected trash layout: %s" % entries
assert os.path.isdir(sub)
names = sorted(os.listdir(sub))
assert all(n.startswith(("chat-auto-save-", "chat-export-auto-save-")) for n in names), "non-autosave file in trash"
total = 0; cnt = 0
for dp, dn, fn in os.walk(TRASH):
    for f in fn:
        total += os.path.getsize(os.path.join(dp, f)); cnt += 1
dates = sorted(set(n[15:25] for n in names if n.startswith("chat-auto-save-")))
w("PRE: _trash-20260928 entries=%d files=%d size=%s date-range=%s..%s" % (len(names), cnt, sf(total), dates[0] if dates else "?", dates[-1] if dates else "?"))

shutil.rmtree(TRASH)
w("CLEARED: _trash-20260928 removed (Class-A direct clear per S11: auto-saves category, client-rotated trash staging, no in-transit refs)")
assert not os.path.exists(TRASH)

# verify live auto-saves untouched
live = os.path.join(ROOT, ".codely-cli", "auto-saves")
lc = len(os.listdir(live))
w("POST: live repo auto-saves items=%d (untouched)" % lc)

# historical-renders bucket quantification (cleanup-decision SUGGESTION face, no execution)
rd = os.path.join(ROOT, "output", "renders")
CURRENT = {
    "bs-001-v15-shipinhao-60s.mp4", "bs-002-v15-shipinhao-60s.mp4",
    "bs-003-v15-shipinhao-60s.mp4", "bs-004-v15-shipinhao-60s.mp4",
    "bs-001-v15-douyin-9x16.mp4",       # C1 backup slot (R316)
    "bs-001-v14b-douyin-9x16.mp4",      # F-006 DY current
    "bs-001-dd-v1-bilibili-16x9.mp4",   # F-005 DD current
    "bs-006-v1-shipinhao-60s.mp4",      # F-049 current
    "bs-005-v1-shipinhao-60s.mp4",      # in-chain blocked (material window)
    "bs-005e-v1-shipinhao-60s.mp4",     # in-chain blocked variant
    "lc-001-v1-shipinhao-60s.mp4", "lc-002-v1-shipinhao-60s.mp4",
    "lc-003-v1-shipinhao-60s.mp4", "lc-004-v1-shipinhao-60s.mp4",
    "lc-005-v1-shipinhao-60s.mp4", "lc-006-v1-shipinhao-60s.mp4",
    "lc-007-v1-shipinhao-60s.mp4", "lc-008-v1-shipinhao-60s.mp4",
    "README.md",
}
cur_sz = 0; cur_n = 0; hist_mp4 = 0.0; hist_n = 0; aux_sz = 0; aux_n = 0
hist_list = []
for f in sorted(os.listdir(rd)):
    fp = os.path.join(rd, f)
    if not os.path.isfile(fp): continue
    s = os.path.getsize(fp)
    if f in CURRENT or f.endswith(".plan.json") and f.replace(".mp4.plan.json", ".mp4") in CURRENT:
        cur_sz += s; cur_n += 1
    elif f.endswith(".mp4"):
        hist_mp4 += s; hist_n += 1; hist_list.append((s, f))
    else:
        aux_sz += s; aux_n += 1
w("renders: current+in-chain=%d files %s | historical-mp4=%d files %s | aux(png/json of hist)=%d files %s" % (
    cur_n, sf(cur_sz), hist_n, sf(hist_mp4), aux_n, sf(aux_sz)))
hist_list.sort(reverse=True)
for s, f in hist_list[:12]:
    w("  hist %-12s %s" % (sf(s), f))
w("hist top12=%s rest=%d small files" % (sf(sum(s for s,_ in hist_list[:12])), max(0, hist_n-12)))

io.open(os.path.join(TMP, "r702_clear.txt"), "w", encoding="utf-8").write("\n".join(out))
print("CLEAR_DONE lines=%d" % len(out))
