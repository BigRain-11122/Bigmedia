# r1312 weekly-report status check: log heads R1295-R1302, weekly_report.py output path, existing report files
import json, os, re, glob, time

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
L = []
add = L.append

state = json.load(open(os.path.join(repo, "src", "os", "state.json"), encoding="utf-8"))
log = state.get("log", [])

add("== log heads R1295..R1302 ==")
for line in log:
    m = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} R(129[5-9]|130[0-2]):", line[:22])
    if m:
        add(line[:550])
        add("")

# full R1310 line (next-wave enumeration tail)
add("== R1310 full line ==")
for line in log:
    if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} R1310:", line[:22]):
        add(line[-1400:])
add("")

# weekly_report.py output path
add("== weekly_report.py paths ==")
src = open(os.path.join(repo, "src", "weekly_report.py"), encoding="utf-8").read()
for i, l in enumerate(src.splitlines()):
    if re.search(r"out|write|REPORT|reports|\.md", l) and ("path" in l.lower() or "open(" in l or "OUT" in l or "argparse" in l or "add_argument" in l or "default" in l):
        add(f"{i+1}| {l.strip()[:160]}")
add("")

# existing weekly report files
add("== weekly report files on disk ==")
for pat in ["**/*weekly*", "**/*W4?*report*", "**/reports/*"]:
    for f in glob.glob(os.path.join(repo, pat), recursive=True):
        if ".git" in f or "node_modules" in f:
            continue
        rel = os.path.relpath(f, repo)
        if re.search(r"weekly|W4\d", rel) and not rel.endswith(".py"):
            add(time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(f))) + "  " + rel)
add("")

# P-20260928-02 first-review mention in logs (shoud check if done)
add("== log grep weekly report / CLOUD_LINE / R658 recent ==")
for line in log[-40:]:
    if re.search(r"周报|weekly_report|CLOUD_LINE", line):
        add(line[:400])
        add("--")

out = os.path.join(repo, ".c3-tmp", "r1312_weekly.txt")
open(out, "w", encoding="utf-8").write("\n".join(L))
print("done", len(L))
