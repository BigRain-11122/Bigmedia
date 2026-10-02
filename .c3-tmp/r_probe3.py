import io, os, json, re

BS = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUT = os.path.join(BS, ".c3-tmp", "r_probe3_out.txt")

st = json.load(io.open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
r989 = [l for l in st.get("log", []) if " R989:" in l][-1]

pool = json.load(io.open(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json", encoding="utf-8"))

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("== R989 log tail (last 2200 chars) ==\n" + r989[-2200:] + "\n\n")
    f.write("== axes keys ==\n" + ", ".join(pool["axes"].keys()) + "\n")
    f.write("top-level keys: " + ", ".join(pool.keys()) + "\n\n")
    consumed = {
        "求新": [4, 7, 12, 3, 11, 14],
        "怀旧": [0, 3, 1],
        "侠气": [5, 13, 2, 0, 1],
        "烟火": [4, 13, 3, 12],
        "秩序": [4, 12, 14, 16],
        "逍遥": [3, 15, 1, 17],
    }
    bad_words = ["年味", "过年", "除夕", "春节", "拜年", "红包", "爆竹", "守岁", "团圆饭"]
    for ax in ["求新", "怀旧", "侠气", "烟火", "秩序", "逍遥"]:
        fest = pool["axes"][ax]["festival"]
        f.write(f"== {ax} festival ({len(fest)} lines) ==\n")
        for i, ln in enumerate(fest):
            used = i in consumed.get(ax, [])
            bad = any(w in ln for w in bad_words)
            tag = "USED" if used else ("XiangweiAVOID" if bad else "FREE")
            f.write(f"[{i}] {tag} {ln}\n")
        f.write("\n")
    # v20 piece + tmp dir contents
    for d in ["MC-20261002-DAILY-v20", "MC-20261002-DAILY-v20-tmp"]:
        p = os.path.join(BS, "data", "storylines", "cards", d)
        if os.path.isdir(p):
            f.write(f"== {d} ==\n")
            for x in sorted(os.listdir(p)):
                f.write("  " + x + "\n")
    # F-106 mentions in finished.md with context
    fm = io.open(os.path.join(BS, "output", "finished.md"), encoding="utf-8", errors="replace").read()
    f.write("== F-106 mentions ==\n")
    for m in re.finditer(r"F-106", fm):
        s = max(0, m.start() - 200)
        f.write(fm[s:m.end() + 200].replace("\n", " | ") + "\n---\n")
    # review doc for v20 tail (M4.5 structure) - just list reviews dir latest 6
    rd = os.path.join(BS, "docs", "reviews")
    fs = sorted(os.listdir(rd))[-6:]
    f.write("== reviews latest ==\n" + "\n".join(fs) + "\n")
print("OK")
