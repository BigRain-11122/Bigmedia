# -*- coding: utf-8 -*-
# MD-0002 voiceover leg 1 (R1954): per-shot TTS for the three-voice drama
# episode. Narrator = light-cyber production default voice (texture is an
# assembly-leg face, applied to the whole track there); system + afeng are
# tier voices per tech#2 adjudication (CosyVoice3 retired -> edge-tts tier
# direct-out; Shanghai-dialect crossover stays a reserved candidate,
# R1785 anchor).
#
# Air-budget law per shot: the validated script fixes 6.00s per shot; a
# spoken line must leave >=0.30s of air (<=5.70s). Over-length lines get
# mechanical rate bumps (+8%, then +15%) keeping text verbatim; anything
# still over is recorded as a shot-extension candidate for the assembly
# leg (drama-ep window 60-90s absorbs the extension - law profile in
# src/render/emotive_tts.py).
#
# Outputs:
#   data/storylines/audio/MD-0002-voice-v1-shotNN.mp3  per-shot segments
#   data/storylines/audio/MD-0002-voice-v1-draft.mp3    flat preview concat
#   data/storylines/drama/md0002/voice-v1.json          cast + readings
# Run: python data/storylines/drama/md0002/gen-voice-v1.py
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # md0002 -> drama -> storylines -> data -> repo
SCRIPT = Path(__file__).resolve().parent / "script-content-v1.json"
AUDIO_DIR = ROOT / "data" / "storylines" / "audio"
OUT_JSON = Path(__file__).resolve().parent / "voice-v1.json"

SHOT_S = 6.00          # validated script allocation (13 x 6 = 78s)
AIR_MIN_S = 0.30       # minimum air inside a shot window
FIT_MAX_S = SHOT_S - AIR_MIN_S
RATE_BUMPS = [0, 8, 15]  # % added to the cast base rate, tried in order
WINDOW = (60.0, 90.0)    # drama-ep episode window (charter)

CAST = {
    "narrator": {"voice": "zh-CN-YunyangNeural", "flags": []},
    # system: low, restrained mechanical broadcast -> deeper male tier,
    # slowed, pitch dropped
    "system": {"voice": "zh-CN-YunjianNeural",
               "flags": ["--rate=-10%", "--pitch=-3Hz"]},
    # afeng: street-warm carrying voice (68yo vendor); Mandarin tier
    # direct-out this pass - Shanghai-dialect coloring = reserved
    # cross-language candidate (R1785), not reachable with edge-tts tiers
    "afeng": {"voice": "zh-CN-XiaoxiaoNeural",
              "flags": ["--rate=+4%", "--pitch=+2Hz"]},
}

DRAFT_GAP_S = 0.35  # flat preview concat only; real gaps = assembly leg


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print("FAIL: %s" % " ".join(cmd))
        print(r.stderr.decode("utf-8", "replace")[-500:])
        sys.exit(1)
    return r


def probe_dur(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)])
    return float(r.stdout.decode("ascii").strip())


def synth(voice, flags, text, out_path):
    cmd = (["edge-tts", "--voice", voice] + flags +
           ["--text", text, "--write-media", str(out_path)])
    run(cmd)
    return probe_dur(out_path)


def main():
    doc = json.loads(SCRIPT.read_text(encoding="utf-8"))
    shots = doc["shots"]
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for sh in shots:
        cast = CAST[sh["speaker"]]
        chosen_flags = None
        chosen_dur = None
        bump = None
        for pct in RATE_BUMPS:
            flags = list(cast["flags"])
            if pct:
                flags = [("--rate=+%d%%" % pct) if f.startswith("--rate=")
                         else f for f in flags] or ["--rate=+%d%%" % pct]
            seg = AUDIO_DIR / ("MD-0002-voice-v1-shot%02d.mp3" % sh["id"])
            d = synth(cast["voice"], flags, sh["line"], seg)
            if d <= FIT_MAX_S:
                chosen_flags, chosen_dur, bump = flags, d, pct
                break
            chosen_flags, chosen_dur, bump = flags, d, pct
        # extend-shot keeps NATURAL delivery: the extension exists to
        # preserve the verbatim anchor's own pacing, so a rushed +15%
        # take defeats the purpose - re-synth at the cast base instead.
        if chosen_dur > FIT_MAX_S and bump:
            seg = AUDIO_DIR / ("MD-0002-voice-v1-shot%02d.mp3" % sh["id"])
            chosen_flags = list(cast["flags"])
            chosen_dur = synth(cast["voice"], chosen_flags, sh["line"], seg)
            bump = 0
        verdict = ("fit" if chosen_dur <= FIT_MAX_S else "extend-shot")
        row = {
            "id": sh["id"], "scene": sh["scene"], "speaker": sh["speaker"],
            "line": sh["line"], "voice": cast["voice"],
            "flags": chosen_flags, "rate_bump_pct": bump,
            "duration_s": round(chosen_dur, 2),
            "air_s_in_6s_window": round(SHOT_S - chosen_dur, 2),
            "verdict": verdict,
        }
        if verdict == "extend-shot":
            row["shot_extend_s"] = round(chosen_dur + AIR_MIN_S, 1)
        rows.append(row)
        print("shot%02d %-8s d=%.2fs bump=%+d%% %s | %s"
              % (sh["id"], sh["speaker"], chosen_dur, bump,
                 verdict, sh["line"][:18]), flush=True)

    # flat preview concat (assembly leg will rebuild with the drama-ep law)
    segs = [AUDIO_DIR / ("MD-0002-voice-v1-shot%02d.mp3" % r["id"])
            for r in rows]
    parts = []
    for i, seg in enumerate(segs):
        parts.append(seg)
        if i + 1 < len(segs):
            gap = AUDIO_DIR / ("_md0002_gap%02d.mp3" % i)
            run(["ffmpeg", "-y", "-f", "lavfi",
                 "-i", "anullsrc=r=24000:cl=mono",
                 "-t", "%.2f" % DRAFT_GAP_S,
                 "-c:a", "libmp3lame", "-qscale:a", "4", str(gap)])
            parts.append(gap)
    lst = AUDIO_DIR / "_md0002_concat.txt"
    lst.write_text("\n".join("file '%s'" % p.resolve().as_posix()
                             for p in parts), encoding="ascii")
    draft = AUDIO_DIR / "MD-0002-voice-v1-draft.mp3"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:a", "libmp3lame", "-qscale:a", "4", str(draft)])
    for g in AUDIO_DIR.glob("_md0002_gap*.mp3"):
        g.unlink()
    lst.unlink()
    draft_dur = probe_dur(draft)

    speech = sum(r["duration_s"] for r in rows)
    ext = sum(r.get("shot_extend_s", SHOT_S) - SHOT_S for r in rows
              if r["verdict"] == "extend-shot")
    proj_min = speech + 0.12 * (len(rows) - 1)
    proj_max = speech + ext + 1.5 * (len(rows) - 1)
    out = {
        "meta": {
            "piece": doc["title"],
            "leg": "voice-v1 (assembly input segments)",
            "tool": "data/storylines/drama/md0002/gen-voice-v1.py",
            "source_script": str(SCRIPT.relative_to(ROOT)),
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "air_budget": {"shot_s": SHOT_S, "air_min_s": AIR_MIN_S,
                           "fit_max_s": FIT_MAX_S,
                           "rate_bumps_pct": RATE_BUMPS},
            "cast_note": ("tier direct-out per tech#2; narrator texture "
                          "(cyber light) is an assembly-leg whole-track "
                          "face; afeng Shanghai-dialect coloring = "
                          "reserved cross-language candidate (R1785)"),
        },
        "cast": CAST,
        "shots": rows,
        "totals": {
            "sum_speech_s": round(speech, 2),
            "draft_concat_s": round(draft_dur, 2),
            "projected_assembly_min_s": round(proj_min, 2),
            "projected_assembly_max_s": round(proj_max, 2),
            "drama_ep_window_s": list(WINDOW),
            "window_ok": WINDOW[0] <= proj_min and proj_max <= WINDOW[1],
            "extend_shots": [r["id"] for r in rows
                             if r["verdict"] == "extend-shot"],
        },
    }
    OUT_JSON.write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("== voice-v1: speech=%.2fs draft=%.2fs projected=%.1f-%.1fs "
          "window=%s extend=%s ==" %
          (speech, draft_dur, proj_min, proj_max,
           "OK" if out["totals"]["window_ok"] else "CHECK",
           out["totals"]["extend_shots"] or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
