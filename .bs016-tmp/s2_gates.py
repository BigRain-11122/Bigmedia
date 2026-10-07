import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
cmds = [
    ["python", "src/ai_feel_check.py", "--beats", "data/sources/bs016/voiceover-v3.beats.txt", "--srt", ".bs016-tmp/subs.srt"],
    ["python", "src/edit_craft_check.py", "--plan", "output/renders/bs-016-v1-shipinhao-60s.mp4.plan.json", "--srt", ".bs016-tmp/subs.srt", "--profile", "shipinhao"],
    ["python", "src/platform_spec_check.py", "--video", "output/renders/bs-016-v1-shipinhao-60s.mp4", "--platform", "\u5fae\u4fe1\u89c6\u9891\u53f7"],
]
out = []
for c in cmds:
    r = subprocess.run(c, capture_output=True)
    out.append("### " + " ".join(c[1:3]) + " -> exit " + str(r.returncode))
    out.append(r.stdout.decode("utf-8", "replace"))
    err = r.stderr.decode("utf-8", "replace").strip()
    if err:
        out.append("[stderr] " + err[:400])
text = "\n".join(out)
with open(".bs016-tmp/s2-results.txt", "w", encoding="utf-8") as f:
    f.write(text)
print(text)
