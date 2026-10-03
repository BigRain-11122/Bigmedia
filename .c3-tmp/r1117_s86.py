import json, io, os

HQ = r"C:\Users\sjs20\Desktop\FluxGroup"
p = json.load(io.open(HQ + r"\life\BigLife\cognition\pools.json", encoding="utf-8"))

def count(v):
    if isinstance(v, dict):
        return sum(count(x) for x in v.values())
    if isinstance(v, list):
        return len(v)
    return 0

axes = p.get("axes", p)
na = sum(count(v) for v in axes.values())
ns = sum(count(v) for v in p.get("sprite", {}).values())
ic = HQ + r"\life\BigLife\cognition\interchat-ledger.jsonl"
nl = sum(1 for _ in io.open(ic, encoding="utf-8")) if os.path.exists(ic) else -1
an = sorted(os.listdir(HQ + r"\life\BigLife\census\anchors"))
io.open(r".c3-tmp\r1117_s86.txt", "w", encoding="utf-8").write(
    "axes_lines=%d sprite_lines=%d total=%d interchat=%d anchors=%d tail=%s\n"
    % (na, ns, na + ns, nl, len(an), an[-2:]))
print("ok")
