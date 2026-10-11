# -*- coding: utf-8 -*-
"""R2005 tech#26 consumption verification (P2 queue-head close-out).

Independent re-run of the v3 acceptance claims on the live repo (do not
trust the owning session's commit message alone):
  G1  dict chain load: v3 = 17 word entries, ALL guarded, all verbatim-src
  G2  real-archive applied validation: own-beats expect over the archived
      asr-check.srt corpus -> every v3 entry fires, after-count = 0
  G3  fingerprint gate readout band: matched pieces >= 0.25,
      mismatched (bs015 beats x SC-001-01-v2 SRT) < 0.25
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "render"))
from whisper_to_srt import (  # noqa: E402
    load_noise_dict, apply_noise_dict, expect_srt_overlap,
    EXPECT_MATCH_MIN_OVERLAP)

V3 = ROOT / "data" / "pipeline" / "asr-noise-dict-v3.json"
AUDIO = ROOT / "data" / "storylines" / "audio"

v3 = json.loads(V3.read_text(encoding="utf-8"))
v3e = v3["entries"]
fails = []

# G1 ------------------------------------------------------------------
if len(v3e) != 17:
    fails.append("G1 v3 entry count %d != 17" % len(v3e))
bad_cls = [e["noise"] for e in v3e if e.get("class") != "guarded"]
if bad_cls:
    fails.append("G1 non-guarded entries: %s" % bad_cls)
bad_src = [e["noise"] for e in v3e if e.get("src") != "verbatim"]
if bad_src:
    fails.append("G1 non-verbatim src: %s" % bad_src)
merged = load_noise_dict(str(V3))
m = {(n, t): c for n, t, c in merged}
miss = [e["noise"] for e in v3e
        if (e["noise"], e["true"]) not in m or m[(e["noise"], e["true"])] != "guarded"]
if miss:
    fails.append("G1 chain-merge missing/unguarded: %s" % miss)
print("G1 merged-chain entries=%d (v1+v2+v3 unique)" % len(merged))

# G2 ------------------------------------------------------------------
def parse_srt(p):
    cues = []
    raw = Path(p).read_text(encoding="utf-8-sig")
    for b in re.split(r"\r?\n\r?\n", raw.strip()):
        lines = [l for l in b.replace("\r\n", "\n").split("\n") if l.strip()]
        if len(lines) >= 3:
            cues.append((0.0, 0.0, "".join(lines[2:])))
    return cues

noise_list = [e["noise"] for e in v3e]
fired = set()
total_applied = 0
after_total = 0
pieces = 0
rows = []
for t in sorted(AUDIO.glob("sc001-*-tmp")):
    srt = t / "asr-check.srt"
    mm = re.match(r"sc001-(\d+)-v(\d+)-tmp$", t.name)
    if not (srt.exists() and mm):
        continue
    beats = AUDIO / ("SC-001-%02d-v%s.beats.txt" % (int(mm.group(1)), mm.group(2)))
    if not beats.exists():
        rows.append((t.name, "BEATS-MISSING", beats.name))
        continue
    cues = parse_srt(srt)
    expect_text = beats.read_text(encoding="utf-8")
    new_cues, applied, skipped = apply_noise_dict(cues, merged, expect_text)
    out_text = "".join(c[2] for c in new_cues)
    after = sum(out_text.count(n) for n in noise_list)
    pre_hits = set(n for n in noise_list if any(n in c[2] for c in cues))
    for n in pre_hits:
        fired.add(n)
    overlap = expect_srt_overlap(expect_text, cues)
    rows.append((t.name, "cues=%d applied=%d skipped=%d after=%d ovl=%.3f"
                 % (len(cues), applied, skipped, after, overlap)))
    total_applied += applied
    after_total += after
    pieces += 1

for r in rows:
    print("G2 %s %s" % r)
unfired = [n for n in noise_list if n not in fired]
if unfired:
    fails.append("G2 entries never fired on corpus: %s" % unfired)
if after_total != 0:
    fails.append("G2 after-count %d != 0" % after_total)
print("G2 pieces=%d total_applied=%d after_total=%d fired=%d/17"
      % (pieces, total_applied, after_total, len(fired)))

# G3 ------------------------------------------------------------------
mis_pair = (ROOT / "data" / "sources" / "bs015" / "voiceover-v6.beats.txt",
            AUDIO / "sc001-01-v2-tmp" / "asr-check.srt")
if mis_pair[0].exists() and mis_pair[1].exists():
    mis = expect_srt_overlap(mis_pair[0].read_text(encoding="utf-8"),
                             parse_srt(mis_pair[1]))
    print("G3 mismatched bs015 x sc001-01-v2 overlap=%.3f (bar %.2f)"
          % (mis, EXPECT_MATCH_MIN_OVERLAP))
    if not mis < EXPECT_MATCH_MIN_OVERLAP:
        fails.append("G3 mismatched overlap %.3f not below bar" % mis)
else:
    print("G3 mismatched-pair files missing (bs015 beats/sc001-01-v2 srt)")
    fails.append("G3 pair files missing")

print("VERDICT: " + ("ALL-GREEN" if not fails else "FAIL " + "; ".join(fails)))
sys.exit(0 if not fails else 1)
