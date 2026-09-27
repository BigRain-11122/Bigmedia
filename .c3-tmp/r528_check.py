import os, io, json, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r528_check.txt")
out = []
def w(s):
    out.append(str(s))

now = datetime.datetime.now()
w("now=" + now.strftime("%Y-%m-%d %H:%M:%S"))

# 0. production self-heal + tick
with io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8") as f:
    st = json.load(f)
w("production=" + str(st.get("production")) + " tick=" + str(st.get("tick")))

# 1. orders anchor check
od = os.path.join(ROOT, "orders")
oms = sorted(p for p in os.listdir(od) if p.startswith("O-") and p.endswith(".md"))
w("orders_O_count=" + str(len(oms)))
anchor = os.path.join(od, "O-20260927-1050-HQ-C.md")
if os.path.exists(anchor):
    am = os.path.getmtime(anchor)
    w("anchor_mtime=" + datetime.datetime.fromtimestamp(am).strftime("%Y-%m-%d %H:%M:%S"))
    new_since = [p for p in oms if os.path.getmtime(os.path.join(od, p)) > am and p != "O-20260927-1050-HQ-C.md"]
    w("orders_new_or_edited_since_anchor=" + (",".join(new_since) if new_since else "NONE"))
else:
    w("anchor MISSING")

# 2. ledger five-mode strict @ line count (anchor 31)
LED = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
try:
    with io.open(LED, encoding="utf-8", errors="replace") as f:
        ltext = f.read()
    tags = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
    led_lines = [ln for ln in ltext.splitlines() if any(t in ln for t in tags)]
    w("ledger_five_mode_lines=" + str(len(led_lines)))
    for ln in led_lines[-3:]:
        w("  led_tail: " + ln[:100])
except Exception as e:
    w("ledger_ERR=" + repr(e))

# 3. decisions non-empty UTF-8 line count (anchor 56)
DEC = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
try:
    with io.open(DEC, encoding="utf-8") as f:
        dtext = f.read()
    dnz = [ln for ln in dtext.splitlines() if ln.strip()]
    w("decisions_nonempty=" + str(len(dnz)))
except Exception as e:
    w("decisions_ERR=" + repr(e))

# 4. backlog top lines (claimability)
with io.open(os.path.join(ROOT, "src", "os", "backlog.md"), encoding="utf-8") as f:
    bl = f.read().splitlines()
w("--- backlog head (first 22 lines) ---")
for ln in bl[:22]:
    w("  BL| " + ln)

# 5. footage newest (#78 SC-003-01 render leg supply window)
fd = os.path.join(ROOT, "data", "sources", "footage")
if os.path.isdir(fd):
    fms = sorted(((os.path.getmtime(os.path.join(fd, p)), p) for p in os.listdir(fd)), reverse=True)
    for m, p in fms[:5]:
        w("footage_newest: " + p + " " + datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S"))

# 6. index.lock
w("index_lock=" + str(os.path.exists(os.path.join(ROOT, ".git", "index.lock"))))

# 7. daily brief in-place check
for d in ("2026-09-27", "2026-09-28"):
    w("daily_" + d + "=" + str(os.path.exists(os.path.join(ROOT, "data", "intel", "daily", d + ".md"))))

# 8. BigLife census/anchors C-00030/31 (#63 supply-gated)
fg = r"C:\Users\sjs20\Desktop\FluxGroup"
bl_anchor_dir = None
for d in os.listdir(fg):
    if "biglife" in d.lower():
        cand = os.path.join(fg, d, "census", "anchors")
        if os.path.isdir(cand):
            bl_anchor_dir = cand
            break
if bl_anchor_dir:
    names = sorted(os.listdir(bl_anchor_dir))
    w("biglife_anchors_count=" + str(len(names)) + " tail=" + ",".join(names[-3:]))
    w("anchor_C00030=" + str(any("C-00030" in n for n in names)).lower())
    w("anchor_C00031=" + str(any("C-00031" in n for n in names)).lower())
else:
    w("biglife_anchors_dir=NOT_FOUND")

# 9. storylines subdomains newest (bm-a writing signs)
sd = os.path.join(ROOT, "data", "storylines")
if os.path.isdir(sd):
    for sub in sorted(os.listdir(sd)):
        subp = os.path.join(sd, sub)
        if not os.path.isdir(subp):
            continue
        newest = (0, None)
        for dirpath, dirnames, filenames in os.walk(subp):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                m = os.path.getmtime(fp)
                if m > newest[0]:
                    newest = (m, os.path.relpath(fp, subp))
        w("storylines/" + sub + " newest=" + (newest[1] or "-") + " " + datetime.datetime.fromtimestamp(newest[0]).strftime("%m-%d %H:%M") if newest[1] else "storylines/" + sub + " empty")

# 10. HQ-FEEDBACK mtime
hqf = os.path.join(ROOT, "HQ-FEEDBACK.md")
if os.path.exists(hqf):
    w("hq_feedback_mtime=" + datetime.datetime.fromtimestamp(os.path.getmtime(hqf)).strftime("%Y-%m-%d %H:%M:%S"))

# 11. global-benchmarks head date (7-day gate, next ~10-01)
gb = os.path.join(ROOT, "docs", "global-benchmarks.md")
if os.path.exists(gb):
    with io.open(gb, encoding="utf-8") as f:
        gtext = f.read(4000)
    for ln in gtext.splitlines():
        if "2026-09" in ln and ("更新" in ln or "记录" in ln):
            w("benchmarks_head: " + ln[:80])
            break

with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("CHECK_DONE lines=" + str(len(out)))
