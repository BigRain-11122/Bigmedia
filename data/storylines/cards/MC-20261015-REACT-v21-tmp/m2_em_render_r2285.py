# -*- coding: utf-8 -*-
"""em-check + subs + poster + mp4 render for MC-20261015-REACT-v21 (M2, R2285)."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(os.path.dirname(HERE), "MC-20261015-REACT-v21")
CARDS = os.path.join(CARDS_DIR, "cards.json")
PNG = os.path.join(CARDS_DIR, "MC-20261015-REACT-v21.png")
MP4 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(HERE)))), "output", "renders", "mc-20261015-react-v21-card.mp4")
SUBS = os.path.join(CARDS_DIR, "subs.srt")
FRAME_W, MARGIN = 1080, 80
SUBS_BOTTOM_LINE = "热点转述自知乎热榜·反应与信条皆取自虚构城市档案"

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

    # ladder: even steps 40..28; pick max feasible tier with >=0.30em margin
    # driver = hot-head line 1st segment = 26.00em -> 34 tier expected (+1.06em).
    chosen = None
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
        f.write("1\n00:00:00,000 --> 00:00:02,600\n%s\n" % SUBS_BOTTOM_LINE)

    out = ["em-check-r2285 (REACT-v21 M2 front-fit, ladder even-steps, v19/v20 format)"]
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
        open(os.path.join(CARDS_DIR, "em-check-r2285.txt"), "w",
             encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
        print("\n".join(out))
        return 1
    out.append("ALL-HORIZ: PASS")
    open(os.path.join(CARDS_DIR, "em-check-r2285.txt"), "w",
         encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n".join(out))

    r = subprocess.run([sys.executable, os.path.join("src", "render",
                     "render_card_video.py"), "--cards", CARDS, "--poster", PNG],
                       capture_output=True)
    print("poster render rc=%d" % r.returncode)
    if r.returncode != 0:
        print(r.stdout.decode("utf-8", "replace")[-800:])
        print(r.stderr.decode("utf-8", "replace")[-800:])
        return 1
    print("poster: %s (%d bytes)" % (PNG, os.path.getsize(PNG)))

    os.makedirs(os.path.dirname(MP4), exist_ok=True)
    r2 = subprocess.run([sys.executable, os.path.join("src", "render",
                         "render_card_video.py"), "--cards", CARDS, "--out", MP4],
                         capture_output=True)
    print("mp4 render rc=%d" % r2.returncode)
    if r2.returncode != 0:
        print(r2.stdout.decode("utf-8", "replace")[-800:])
        print(r2.stderr.decode("utf-8", "replace")[-800:])
        return 1
    print("mp4: %s (%d bytes)" % (MP4, os.path.getsize(MP4)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
