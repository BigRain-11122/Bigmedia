# -*- coding: utf-8 -*-
"""R2005 residue close (same-round addendum, tick unchanged).

Round-body final verification discovered the audio-line cleanup-hook miss:
SC-005-05/06 TTS working dirs left 75 untracked files (10.59MB) across 9+
rounds (R1996/R2000 close lists committed only the hand-off face). This
addendum: (a) appends clause 7 to the R2005 state log line (addition, not
rewrite - wrong-account-stays-visible law), (b) batch-commits the residue
aligned with the sc001-*/sc005-01..03 full-commit precedent, alongside the
tech#114 guard-candidate seed row. Tick/ts untouched."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "os"))

from close_commit import run_close_commit  # noqa: E402

ADDENDUM = (
    "⑦轮末清理钩追补收口（round body 终验发现·同轮收口）=sc005-05/06-v1-tmp TTS 中间件"
    "75 件（10.59MB）批量入账（R1996/R2000 收账清单漏 TTS 工作目录面=tech#81 自含律只锚 "
    ".c3-tmp 的盲区第二案〔R1895 首案〕·五前例 sc001-*/sc005-01..03 全量 commit 范式对齐"
    "+「mp3 gitignored」旧注记对 tmp 子目录不成立勘正〔gitignore L24 只盖顶层〕）+"
    "tech#114 audio tmp 收口完整性守卫候选种子入队"
)

state_path = ROOT / "src" / "os" / "state.json"
data = json.loads(state_path.read_text(encoding="utf-8"))
last = data["log"][-1]
if ADDENDUM[:24] not in last:
    data["log"][-1] = last + "——" + ADDENDUM
    tmp = state_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(state_path)
    print("LOG-ADDENDUM appended (tick untouched=%s)" % data["tick"])
else:
    print("LOG-ADDENDUM already present, skip")

residue = sorted(
    str(p) for p in
    (ROOT / "data" / "storylines" / "audio").glob("sc005-0[56]-v1-tmp/*")
    if p.is_file())
# keep only files git reports as untracked (defensive: skip already-tracked)
import subprocess  # noqa: E402
st = subprocess.run(
    ["git", "status", "--porcelain", "-z", "--untracked-files=all",
     "--", "data/storylines/audio/sc005-05-v1-tmp",
     "data/storylines/audio/sc005-06-v1-tmp"],
    cwd=str(ROOT), capture_output=True)
reported = set()
for tok in st.stdout.decode("utf-8", "replace").split("\0"):
    if len(tok) >= 4 and tok[2] == " ":
        reported.add(tok[3:])
untracked = []
for p in residue:
    rel = str(Path(p).relative_to(ROOT)).replace("\\", "/")
    if rel in reported:
        untracked.append(p)
print("residue files on disk=%d untracked=%d" % (len(residue), len(untracked)))

files = untracked + [
    str(ROOT / "src" / "os" / "state.json"),
    str(ROOT / "state" / "queue" / "tech.md"),
    str(ROOT / ".c3-tmp" / "r2005_residue_close.py"),
]
rc, lines = run_close_commit(
    files,
    "R2005 residue close: batch-commit SC-005-05/06 TTS tmp intermediates "
    "(75 files, 10.59MB - R1996/R2000 close lists missed the audio tmp "
    "working-dir face, second cleanup-hook recurrence; aligned with "
    "sc001/sc005-01..03 full-commit precedent; gitignore L24 top-level-only "
    "noted); tech#114 guard-candidate seed; state log addendum [via bm-a]",
    push=True,
)
for ln in lines:
    print(ln)
print("RESIDUE-CLOSE-RC", rc)
sys.exit(rc)
