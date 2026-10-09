#!/usr/bin/env python3
"""explore#25 dual-voice alternation trial (P-5 pre-read de-risk).

Production-representative: re-assembles the real MD-0001 role segments
(13 shots, 4 voices: narrator/lamp/tower/cat) with three switch-gap legs:

  A deepdive-seg : voice-switch gap = DEEPDIVE_SEG_GAP_BASE (2.0s) + jitter
                   (emotive_tts --deepdive segment-boundary param reuse)
  B hand-band    : voice-switch gap = 0.35s +-0.05 (hand-arranged,
                   natural band >= 0.3s floor per queue item 25)
  C subfloor     : voice-switch gap = 0.15s flat (negative control,
                   below the 0.3s natural-band floor)

Same-voice boundaries are held IDENTICAL across legs (seeded HUMAN band
0.30s +-0.18, floor 0.12) so the switch gap is the only variable.

Then runs the S2 asr-check QC recipe (medium int8 + beam5 + no-context,
CPU by default) on each leg and writes machine readouts:
  - anchor survival per role (vs single-voice baselines R1786/R1787)
  - cue count / glue detection at switch boundaries
  - planned gaps + measured cue boundary deltas
ASCII-only script; Chinese anchors live in r1864_anchors.json (data file).
"""
import json
import random
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEGDIR = REPO / "data/storylines/drama/md0001/tts/segments"
BEATS = REPO / "data/storylines/drama/md0001/tts/md0001-full.beats.txt"
ANCHORS = json.loads((REPO / ".c3-tmp/r1864_anchors.json").read_text(encoding="utf-8"))
OUT = REPO / ".c3-tmp/r1864-duovoice"
OUT.mkdir(exist_ok=True)

SWITCH_SEED = 20261010
SAME_SEED = 7919
DEEPDIVE_BASE, DEEPDIVE_SPREAD = 2.0, 0.4   # emotive_tts law profile constants
HAND_MID, HAND_SPREAD = 0.35, 0.05          # hand-arranged band (floor 0.3)
SUBFLOOR = 0.15                              # negative control
HUMAN_BASE, HUMAN_SPREAD = 0.30, 0.18        # emotive_tts HUMAN_GAP band


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("FAIL cmd rc=%d: %s" % (r.returncode, " ".join(map(str, cmd))[:160]))
        print((r.stderr or "")[-500:])
        sys.exit(1)
    return r


def probe_dur(p):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(p)])
    return float(r.stdout.strip())


def parse_beats():
    shots = []
    for ln in BEATS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        parts = [x.strip() for x in ln.split("|")]
        shots.append({"slot": parts[1], "text": parts[2]})
    return shots


def norm_cjk(s):
    return "".join(re.findall(r"[\u4e00-\u9fff0-9A-Za-z]", s))


def main():
    cast = json.loads((REPO / "data/storylines/drama/md0001/tts/cast.json").read_text(encoding="utf-8"))
    role_of = {}
    for role, spec in cast["roles"].items():
        for s in spec["shots"]:
            role_of[s] = role
    shots = parse_beats()
    assert len(shots) == 13, "expected 13 shots, got %d" % len(shots)

    segs, durs = [], []
    for i in range(1, 14):
        p = SEGDIR / ("shot%02d.mp3" % i)
        assert p.exists(), "missing %s" % p
        segs.append(p)
        durs.append(probe_dur(p))

    # boundary classification (gap AFTER shot idx, 0-based idx = shot idx+1)
    kinds = []
    for i in range(12):
        kinds.append("switch" if role_of[i + 1] != role_of[i + 2] else "same")
    print("speech_total=%.2fs switches=%d same=%d"
          % (sum(durs), kinds.count("switch"), kinds.count("same")))

    # seeded gap plans; same-voice gaps shared across legs (control variable)
    rng_s = random.Random(SWITCH_SEED)
    rng_h = random.Random(SAME_SEED)
    same_gaps = [round(max(0.12, HUMAN_BASE + rng_h.uniform(-HUMAN_SPREAD, HUMAN_SPREAD)), 3)
                 for _ in range(12)]
    legs = {
        "legA-deepdive-seg": [round(DEEPDIVE_BASE + rng_s.uniform(0, DEEPDIVE_SPREAD), 3)
                              for _ in range(12)],
        "legB-hand-band": [round(HAND_MID + rng_s.uniform(-HAND_SPREAD, HAND_SPREAD), 3)
                           for _ in range(12)],
        "legC-subfloor": [SUBFLOOR] * 12,
    }
    manifests = {}
    for name, sw in legs.items():
        gaps = [sw[i] if kinds[i] == "switch" else same_gaps[i] for i in range(12)]
        parts, t0, rows = [], 0.0, []
        for i, seg in enumerate(segs):
            rows.append({"shot": i + 1, "role": role_of[i + 1],
                         "start": round(t0, 3), "end": round(t0 + durs[i], 3),
                         "gap_before": None if i == 0 else gaps[i - 1],
                         "boundary_before": None if i == 0 else kinds[i - 1]})
            parts.append(seg)
            t0 += durs[i]
            if i < 12:
                g = gaps[i]
                gp = OUT / ("%s_gap%02d.mp3" % (name, i))
                run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                     "-t", "%.3f" % g, "-c:a", "libmp3lame", "-qscale:a", "4", str(gp)])
                parts.append(gp)
                t0 += g
        lst = OUT / (name + ".txt")
        lst.write_text("\n".join("file '%s'" % p.resolve().as_posix() for p in parts),
                       encoding="ascii")
        audio = OUT / (name + ".mp3")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
             "-c:a", "libmp3lame", "-qscale:a", "4", str(audio)])
        manifests[name] = {"audio": audio.name, "total_s": round(t0, 3),
                           "switch_gap_s": [gaps[i] for i in range(12) if kinds[i] == "switch"],
                           "same_gap_s": [gaps[i] for i in range(12) if kinds[i] == "same"],
                           "shots": rows}
        print("OK %s total=%.2fs (mp3 %.2fs)" % (name, t0, probe_dur(audio)))

    (OUT / "manifests.json").write_text(
        json.dumps(manifests, ensure_ascii=False, indent=1), encoding="utf-8")

    # ASR QC recipe (medium int8 + beam5 + no-context, CPU default)
    for name in legs:
        r = subprocess.run([sys.executable, "src/render/whisper_to_srt.py",
                            "--audio", str(OUT / (name + ".mp3")),
                            "--out", str(OUT / (name + ".srt")),
                            "--model", "medium", "--beam-size", "5", "--no-context"],
                           capture_output=True, text=True,
                           env=dict(**__import__("os").environ, HF_HUB_OFFLINE="1"))
        print("ASR %s rc=%d %s" % (name, r.returncode, (r.stdout or "").strip()[-160:]))
        if r.returncode != 0:
            print((r.stderr or "")[-400:])
            sys.exit(1)

    # readouts
    def parse_srt(p):
        blocks = re.split(r"\n\n+", p.read_text(encoding="utf-8-sig").strip())
        cues = []
        for b in blocks:
            m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", b)
            if not m:
                continue
            f = [int(x) for x in m.groups()]
            a = f[0] * 3600 + f[1] * 60 + f[2] + f[3] / 1000.0
            z = f[4] * 3600 + f[5] * 60 + f[6] + f[7] / 1000.0
            txt = "\n".join(b.splitlines()[2:]) if len(b.splitlines()) > 2 else ""
            cues.append((a, z, norm_cjk(txt)))
        return cues

    report = {}
    for name, mf in manifests.items():
        cues = parse_srt(OUT / (name + ".srt"))
        full = "".join(c[2] for c in cues)
        per_shot = []
        for row in mf["shots"]:
            anchors = ANCHORS["anchors"][str(row["shot"])]
            hit = [a for a in anchors if norm_cjk(a) in full]
            per_shot.append({"shot": row["shot"], "role": row["role"],
                             "anchor_hit": hit, "n_anchor": len(anchors),
                             "pass": len(hit) > 0})
        role_pass = {}
        for pr in per_shot:
            role_pass.setdefault(pr["role"], [0, 0])
            role_pass[pr["role"]][0] += 1 if pr["pass"] else 0
            role_pass[pr["role"]][1] += 1
        # glue detection: one cue containing anchors of two different shots
        glue = 0
        for _, _, ct in cues:
            owners = set()
            for pr in per_shot:
                for a in ANCHORS["anchors"][str(pr["shot"])]:
                    if norm_cjk(a) and norm_cjk(a) in ct:
                        owners.add(pr["shot"])
                        break
            if len(owners) > 1:
                glue += 1
        # measured boundary delta at switches (ASR cue gap across the silence)
        switch_deltas = []
        rows = mf["shots"]
        for i in range(12):
            if mf["shots"][i + 1]["boundary_before"] != "switch":
                continue
            end_prev, start_next = rows[i]["end"], rows[i + 1]["start"]
            prev_cue_end = max((z for a, z, _ in cues if a < end_prev + 0.25), default=None)
            next_cue_start = min((a for a, z, _ in cues if a > end_prev - 0.25), default=None)
            if prev_cue_end is not None and next_cue_start is not None:
                switch_deltas.append(round(next_cue_start - prev_cue_end, 3))
        report[name] = {
            "total_s": mf["total_s"],
            "n_cues": len(cues),
            "n_shots": len(rows),
            "anchor_shot_pass": sum(1 for p in per_shot if p["pass"]),
            "role_pass": {k: "%d/%d" % tuple(v) for k, v in role_pass.items()},
            "glued_cues": glue,
            "planned_switch_gap_s": mf["switch_gap_s"],
            "measured_cue_gap_at_switch_s": switch_deltas,
            "per_shot": per_shot,
        }
        print("%s: cues=%d/13 anchor_pass=%d/13 roles=%s glue=%d"
              % (name, report[name]["n_cues"], report[name]["anchor_shot_pass"],
                 report[name]["role_pass"], glue))

    (OUT / "readouts.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE readouts -> %s" % (OUT / "readouts.json"))


if __name__ == "__main__":
    main()
