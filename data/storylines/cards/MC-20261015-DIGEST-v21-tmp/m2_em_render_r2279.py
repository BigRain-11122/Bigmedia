# -*- coding: utf-8 -*-
"""em-check + subs + poster render for MC-20261015-DIGEST-v21 (M2)."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(os.path.dirname(HERE), "MC-20261015-DIGEST-v21")
CARDS = os.path.join(CARDS_DIR, "cards.json")
PNG = os.path.join(CARDS_DIR, "MC-20261015-DIGEST-v21.png")
SUBS = os.path.join(CARDS_DIR, "subs.srt")
FRAME_W, MARGIN = 1080, 80
SUBS_BOTTOM_LINE = "基于硅基城市真实事件（机制建设日令批台账档案）"

_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(_repo_root, "src", "render"))
from render_card_video import _em_cost  # noqa: E402


def cost(s):
    return sum(_em_cost(ch) for ch in s)


def main():
    d = json.load(open(CARDS, encoding="utf-8"))
    lines = d["cards"][0]["lines"]
    h1 = lines[0]
    h2s = lines[1:]
    c_h1 = cost(h1)
    costs = [(s, cost(s)) for s in h2s]

    # ladder: cap at 40 (v20 same-layout proven tier; 44 fails VERTICAL fit --
    # r2279 pixel evidence: last body band merged with subs band, 61px union).
    for size in range(40, 27, -2):
        budget = (FRAME_W - 2 * MARGIN) / float(size)
        worst = budget - max(c for _, c in costs)
        if worst >= 0.30:
            chosen = size
            budget_final = budget
            worst_final = worst
            break
    report = []
    if chosen is None:
        print("EM-FAIL: no ladder size fits")
        return 1

    d["font"]["h2_size"] = chosen
    with open(CARDS, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)

    with open(SUBS, "w", encoding="utf-8", newline="\n") as f:
        f.write("1\n00:00:00,000 --> 00:00:03,000\n%s\n" % SUBS_BOTTOM_LINE)

    out = ["em-check-r2279 (DIGEST-v21 M2 front-fit, ladder even-steps, v20 format)"]
    out.append("h2_size=%d budget=%.2fem" % (chosen, budget_final))
    for s, c in costs:
        m = budget_final - c
        out.append("%s %6.2fem margin %+6.2f  %s" %
                   ("OK " if m >= 0 else "NG ", c, m, s))
    out.append("H1=%.2fem (h1 own face, h1_size=%d)" % (c_h1, d["font"]["h1_size"]))
    c_subs = cost(SUBS_BOTTOM_LINE)
    subs_budget = (FRAME_W - 2 * MARGIN) / float(d["font"]["subs_size"])
    out.append("subs %.2fem < %.2fem budget %s" %
               (c_subs, subs_budget, "OK" if c_subs <= subs_budget else "NG"))
    if worst_final < 0.30 or c_subs > subs_budget:
        out.append("ALL-HORIZ: FAIL")
        report_txt = "\n".join(out) + "\n"
        open(os.path.join(CARDS_DIR, "em-check-r2279.txt"), "w",
             encoding="utf-8", newline="\n").write(report_txt)
        print(report_txt)
        return 1
    out.append("ALL-HORIZ: PASS")
    report_txt = "\n".join(out) + "\n"
    open(os.path.join(CARDS_DIR, "em-check-r2279.txt"), "w",
         encoding="utf-8", newline="\n").write(report_txt)
    print(report_txt)

    r = subprocess.run([sys.executable, os.path.join("src", "render",
                     "render_card_video.py"), "--cards", CARDS, "--poster", PNG],
                       capture_output=True)
    print("render rc=%d" % r.returncode)
    if r.returncode != 0:
        print(r.stdout.decode("utf-8", "replace")[-1500:])
        print(r.stderr.decode("utf-8", "replace")[-1500:])
        return 1
    print("poster: %s (%d bytes)" % (PNG, os.path.getsize(PNG)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
