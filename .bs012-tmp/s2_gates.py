import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
cmds = [
    ["python", "src/ai_feel_check.py", "--beats", "data/sources/bs012/voiceover-v4.beats.txt", "--srt", ".bs012-tmp/subs.srt"],
    ["python", "src/edit_craft_check.py", "--plan", "output/renders/bs-012-v1-shipinhao-60s.mp4.plan.json", "--srt", ".bs012-tmp/subs.srt", "--profile", "shipinhao"],
    ["python", "src/platform_spec_check.py", "--video", "output/renders/bs-012-v1-shipinhao-60s.mp4", "--platform", "\u5fae\u4fe1\u89c6\u9891\u53f7"],
]
for c in cmds:
    r = subprocess.run(c, capture_output=True)
    print("### " + " ".join(c[1:3]) + " -> exit " + str(r.returncode))
    print(r.stdout.decode("utf-8", "replace"))
    err = r.stderr.decode("utf-8", "replace").strip()
    if err:
        print("[stderr]", err[:400])
