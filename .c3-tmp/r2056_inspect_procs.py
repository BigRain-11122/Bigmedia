# r2056: inspect aihot_procs verdict enum priority (tech#131 preflight)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "os"))
import aihot_procs as ap

src = Path(ap.__file__).read_text(encoding="utf-8")
i = src.find("def topology_verdict")
if i < 0:
    for name in ("def build_result", "def decide", "def make_result"):
        i = src.find(name)
        if i >= 0:
            break
print(src[i:i + 2600])
