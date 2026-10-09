"""R1868 explore#11 evidence probe: GPU idle-band distribution readout.

Reads the P-33 collector ledger (BigCompute state/gpu-util/samples.jsonl,
read-only) and computes utilization / free-VRAM band distributions plus
dual-gate "runnable now" shares for the last 48h and 7d windows.

Zero GPU, zero network, read-only. Output: JSON evidence file (UTF-8, no
BOM). Empirical anchor for R-20261010-bigstream-11 (GPU idle-time task
candidate design, headroom guard parameterization).

Band conventions:
- util bands follow tech#16 BANDS (<10 idle / 10-30 light / 30-70 workload
  / >=70 saturated).
- free-VRAM bands map to candidate gates: <2048 = tech#44 DEFER line;
  2048-4096 = embedding-class; 4096-8192 = whisper-large-class;
  >=8192 = review-14b-class headroom zone.
- dual-gate idle = util < 20 AND free >= gate (the design core: util-only
  triggers are false starts when the card is memory-resident).
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

LEDGER = (Path(__file__).resolve().parents[3]
          / "compute" / "BigCompute" / "state" / "gpu-util"
          / "samples.jsonl")
OUT = Path(__file__).resolve().parent / "r1868_idle_bands_evidence.json"
TOTAL_MIB = 12282  # RTX 4070 SUPER 12GB, memory-anchored reading
UTIL_IDLE = 20.0   # dual-gate util line (design value, see doc)


def load_rows(path):
    rows = []
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        ts = str(rec.get("ts", ""))[:19]
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            continue
        util = rec.get("util_pct")
        mem = rec.get("mem_used_mib")
        if not isinstance(util, (int, float)) or not isinstance(mem, (int, float)):
            continue
        rows.append((dt, float(util), float(mem)))
    return rows


def window_stats(rows, hours):
    if not rows:
        return None
    cut = rows[-1][0] - timedelta(hours=hours)
    win = [r for r in rows if r[0] >= cut]
    n = len(win)
    if n == 0:
        return {"n": 0}
    util_bands = {"lt10": 0, "10_30": 0, "30_70": 0, "ge70": 0}
    free_bands = {"lt2048": 0, "2048_4096": 0, "4096_8192": 0, "ge8192": 0}
    dual = {2048: 0, 4096: 0, 8192: 0, 11264: 0}
    for _, util, mem in win:
        free = TOTAL_MIB - mem
        if util < 10:
            util_bands["lt10"] += 1
        elif util < 30:
            util_bands["10_30"] += 1
        elif util < 70:
            util_bands["30_70"] += 1
        else:
            util_bands["ge70"] += 1
        if free < 2048:
            free_bands["lt2048"] += 1
        elif free < 4096:
            free_bands["2048_4096"] += 1
        elif free < 8192:
            free_bands["4096_8192"] += 1
        else:
            free_bands["ge8192"] += 1
        if util < UTIL_IDLE:
            for gate in dual:
                if free >= gate:
                    dual[gate] += 1
    pct = lambda v: round(100.0 * v / n, 1)
    return {
        "n": n,
        "span": [win[0][0].isoformat(), win[-1][0].isoformat()],
        "util_bands_pct": {k: pct(v) for k, v in util_bands.items()},
        "free_bands_pct": {k: pct(v) for k, v in free_bands.items()},
        "dual_gate_idle_share_pct": {str(k): pct(v) for k, v in dual.items()},
        "last_sample": {"ts": win[-1][0].isoformat(),
                        "util_pct": win[-1][1], "mem_used_mib": win[-1][2]},
    }


def main():
    rows = load_rows(LEDGER)
    out = {
        "probe": "r1868_idle_bands_probe.py",
        "ledger": str(LEDGER),
        "total_mib": TOTAL_MIB,
        "util_idle_line": UTIL_IDLE,
        "total_rows": len(rows),
        "ledger_span": [rows[0][0].isoformat(), rows[-1][0].isoformat()]
        if rows else None,
        "last48h": window_stats(rows, 48),
        "last7d": window_stats(rows, 24 * 7),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print("wrote", OUT)
    print(json.dumps(out["last48h"], ensure_ascii=False))
    print(json.dumps(out["last7d"], ensure_ascii=False))


if __name__ == "__main__":
    main()
