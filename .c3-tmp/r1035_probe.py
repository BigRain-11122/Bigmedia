# -*- coding: utf-8 -*-
"""Fast-path probe R1035: state tail + backlog top + orders + git + group ledger scan."""
import json, os, re, io, subprocess, glob

OUT = io.open(os.path.join(os.path.dirname(__file__), 'r1035_probe_fast.txt'), 'w', encoding='utf-8')
def w(s): OUT.write(s + "\n")

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
GRP = r'C:\Users\sjs20\Desktop\FluxGroup'

# 1) state.json
st = json.load(io.open(os.path.join(ROOT, 'src/os/state.json'), encoding='utf-8'))
w("=== state.json ===")
w("tick=%s" % st.get('tick'))
w("ts=%s" % st.get('ts'))
w("task=%s" % st.get('task'))
w("production=%s" % (st.get('production') or st.get('mode') or 'n/a'))
logs = st.get('log') or []
w("log_len=%d" % len(logs))
for line in logs[-4:]:
    w("LOG| " + line[:400])
wm = st.get('decisions_watermark') or {}
w("wm_dnums=%s" % json.dumps(wm.get('dnums', wm), ensure_ascii=False)[:600])

# 2) git status
w("=== git status --short (BigStream) ===")
p = subprocess.run(['git', 'status', '--short'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
w(p.stdout.strip()[:1500] or "(clean)")
w("HEAD| " + subprocess.run(['git','log','-1','--format=%h %ad %s','--date=format:%m-%d %H:%M'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8').stdout.strip())

# 3) orders latest
w("=== orders/ latest ===")
files = glob.glob(os.path.join(ROOT, 'orders', '*'))
files.sort(key=lambda f: os.path.getmtime(f))
for f in files[-4:]:
    w("ORDER| %s (mtime %s)" % (os.path.basename(f), __import__('datetime').datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m-%d %H:%M')))

# 4) group decisions.md: dispatch board head + D/C set diff
w("=== group decisions.md ===")
dec = io.open(os.path.join(GRP, 'docs', 'decisions.md'), encoding='utf-8').read()
dnums = sorted(set(re.findall(r'[DC]-\d{8}-\d{2}', dec)))
old = set(wm.get('dnums', [])) if isinstance(wm.get('dnums'), list) else set(re.findall(r'[DC]-\d{8}-\d{2}', json.dumps(wm.get('dnums', ''))))
new = [d for d in dnums if d not in old]
w("dec_total=%d new_vs_wm=%s" % (len(dnums), new if new else "(none)"))
head = dec[:3000]
w("--- decisions.md head (dispatch board) ---")
for ln in head.splitlines()[:40]:
    w("DEC| " + ln[:200])

# 5) evolution-ledger @BigStream lines
w("=== evolution-ledger @BigStream scan ===")
led = io.open(os.path.join(GRP, 'cph4', 'evolution-ledger.md'), encoding='utf-8').read()
pat = re.compile(r'@(BigStream|七线全司|全司|六司|八线全量)')
hits = []
for i, ln in enumerate(led.splitlines()):
    if pat.search(ln):
        hits.append((i + 1, ln.strip()))
w("ledger_at_hits=%d" % len(hits))
for n, ln in hits[-6:]:
    w("LED| L%d %s" % (n, ln[:300]))

OUT.close()
print("probe done")
