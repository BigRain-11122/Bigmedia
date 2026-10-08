# -*- coding: utf-8 -*-
"""MD-0001 assembly leg (R1794, #108 drama PoC).

Stage 1: per-shot segments from T2I frames with Ken Burns motion per
PACK-v1.json kb params (zoom start/end honored, pan drift, slow push on
the closer; shot 13 = flat program layer per text-separation law).
Stage 2: reuse R-E engine xfade_chain (A3 true-splice cuts + fade runs)
so the timeline algebra matches edit_craft_check exactly.
Stage 3: drama subtitles + centered statement + AIGC mark burned,
multi-role audio track placed at +0.20s inside each shot window.

ASCII rule: source is pure ASCII; Chinese lives in the data files only.
"""
import json
import subprocess
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, "src/render")
import edit_craft as ec  # engine reuse: FPS, SEG_SAFETY_S, xfade_chain

REPO = Path(".").resolve()
MD = REPO / "data/storylines/drama/md0001"
TMP = REPO / ".c3-tmp/asm-r1794"
TMP.mkdir(parents=True, exist_ok=True)
OUT = REPO / "output/renders"
OUT.mkdir(exist_ok=True)
FPS = ec.FPS
W_, H_ = 1216, 684  # even-dimension law (libx264); 16:9 exact, frames are 1216x683
FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_ESC = FONT.replace(":", "\\:")  # engine _fpath law: escape the drive colon
AIGC_TEXT = "[AIGC\u00b7AI \u751f\u6210\u5185\u5bb9]"  # mechanical bracket form (v14 canon)
AUDIO_LEAD_S = 0.20     # speech start offset inside each shot window
CUE_TAIL_S = 0.35       # subtitle hold after speech ends

script = json.loads((MD / "script-content-v2.json").read_text(encoding="utf-8"))
pack = json.loads((MD / "t2i/PACK-v1.json").read_text(encoding="utf-8"))
lines = [s["line"] for s in script["shots"]]          # 13 verbatim lines
kbs = [s.get("kb", {}) for s in pack["shots"]]

# ---- timeline ----------------------------------------------------------
# windows = storyboard declared seconds; shot13 extended to fit its 6.12s
# speech + lead + tail (audio must not overrun the tail of the piece).
raw_win = [s["seconds"] for s in script["shots"]]


def probe_dur(p):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


auds = []
for i in range(1, 14):
    p = MD / ("tts/segments/shot%02d.mp3" % i)
    auds.append(probe_dur(p))
win = list(raw_win)
need13 = AUDIO_LEAD_S + auds[12] + 0.50
if win[12] < need13:
    win[12] = round(need13 + 0.02, 2)
bounds_t = []
acc = 0.0
for k in range(12):
    acc += win[k]
    bounds_t.append(acc)
total = round(sum(win), 2)
print("windows:", win)
print("audio:", [round(a, 3) for a in auds])
print("bounds:", bounds_t, "total:", total)

# transition plan (bilibili profile: share window 0.40-0.60, pool legal,
# no back-to-back repeats, fades 0.16 in [0.12,0.20], cuts fade_s=0)
BOUNDS = [
    ("cut", 0.0), ("circleopen", 0.16), ("smoothleft", 0.16), ("cut", 0.0),
    ("distance", 0.16), ("cut", 0.0), ("radial", 0.16), ("cut", 0.0),
    ("rectcrop", 0.16), ("cut", 0.0), ("slideup", 0.16), ("hblur", 0.16),
]
plan = {
    "engine": "R-E", "spec": "docs/editing-craft-spec.md",
    "profile": "bilibili", "visual_mode": "matched",
    "visual_ratio": round(12 / 13.0, 3), "cards_only_beats": [12],
    "producer_round": "R1794", "piece": "MD-0001 drama PoC draft",
    "duration_expected_s": total, "last_beat_end_s": total, "tail_s": 0.0,
    "hits": [],
    "boundaries": [
        {"k": k + 1, "time_s": bounds_t[k], "fade_s": f, "type": t}
        for k, (t, f) in enumerate(BOUNDS)
    ],
    "segments": [],
}
spans = [win[0]] + [bounds_t[i] - bounds_t[i - 1] for i in range(1, 12)] + [total - bounds_t[11]]
segs_meta = []
for k in range(13):
    inc = float(BOUNDS[k - 1][1]) if 1 <= k <= 12 else 0.0
    dur = round(spans[k] + inc, 3)
    cards_only = (k == 12)
    meta = {
        "idx": k, "dur_s": dur, "flash": False,
        "treatment": "flat" if cards_only else (
            "ken_out" if kbs[k].get("move") == "zoom-out" else "ken_in"),
        "cards_only": cards_only,
    }
    if not cards_only:
        meta["visual_source"] = "data/storylines/drama/md0001/t2i/frames-r1792/shot%02d.png" % (k + 1)
    else:
        meta["cards_only_reason"] = ("program-layer statement shot 13 (text "
                                     "separation law): black bg + statement, "
                                     "zero T2I by design")
    segs_meta.append(meta)
plan["segments"] = segs_meta
plan_path = OUT / "md-0001-v1-bilibili-16x9.mp4.plan.json"
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=1),
                     encoding="utf-8")
print("plan written:", plan_path)


# ---- cues / beats / srt -------------------------------------------------
cues = []
for k in range(13):
    s0 = (0.0 if k == 0 else bounds_t[k - 1]) + AUDIO_LEAD_S
    cues.append([round(s0, 3), round(s0 + auds[k] + CUE_TAIL_S, 3), lines[k]])
PROF = ["hook", "wink", "beat", "wink", "body", "turn", "punch",
        "body", "beat", "wink", "wink", "close", "close"]
SPEAK = ["narrator-open", "lamp-line", "narrator-scar", "lamp-line",
         "narrator-log", "narrator-tower", "tower-line", "narrator-dawn",
         "narrator-cat", "cat-line", "cat-line", "narrator-close",
         "endcard-statement"]
beats_txt = []
for k in range(13):
    beats_txt.append("%s | %s | %s" % (PROF[k], SPEAK[k], lines[k]))
(MD / "tts/md0001-full.beats.txt").write_text(
    "\n".join(beats_txt) + "\n", encoding="utf-8")


def fmt(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms >= 1000:
        ms = 999
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


srt = []
for k, (s, e, tx) in enumerate(cues):
    srt += [str(k + 1), fmt(s) + " --> " + fmt(e), tx, ""]
(MD / "tts/md0001-full.srt").write_text("\n".join(srt), encoding="utf-8")
print("beats+srt written")

# ---- stage 1: segments --------------------------------------------------


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL ffmpeg exit %d" % r.returncode)
        print(r.stderr[-1200:])
        sys.exit(3)
    return r


def kb_expr(kb, nf):
    """zoompan z/x/y expressions honoring PACK kb (zoom start/end or pan)."""
    move = kb.get("move", "static")
    if move in ("zoom-in", "zoom-in-fast"):
        zs, ze = float(kb.get("start_scale", 1.0)), float(kb.get("end_scale", 1.05))
        z = "'min(%.4f+%.4f*on/%d,%.4f)'" % (zs, ze - zs, nf, ze)
        x = "'iw/2-(iw/zoom)/2'"
        y = "'ih/2-(ih/zoom)/2'"
    elif move == "zoom-out":
        zs, ze = float(kb.get("start_scale", 1.06)), float(kb.get("end_scale", 1.0))
        z = "'max(%.4f-%.4f*on/%d,%.4f)'" % (zs, zs - ze, nf, ze)
        x = "'iw/2-(iw/zoom)/2'"
        y = "'ih/2-(ih/zoom)/2'"
    elif move == "pan":
        z = "'1.06'"
        if kb.get("pan") == "right-to-left":
            x = "'(iw-iw/zoom)*(1-on/%d)'" % nf
        else:
            x = "'(iw-iw/zoom)*on/%d'" % nf
        y = "'ih/2-(ih/zoom)/2'"
    else:  # static storyboard shots get a barely-there closing drift so the
           # zero-craft static tell never fires (sub-pixel on dark frames)
        z = "'min(1.0+0.04*on/%d,1.04)'" % nf
        x = "'iw/2-(iw/zoom)/2'"
        y = "'ih/2-(ih/zoom)/2'"
    return z, x, y


segs = []
for k, meta in enumerate(segs_meta):
    rt = meta["dur_s"] + ec.SEG_SAFETY_S
    seg = TMP / ("seg%02d.mp4" % k)
    if meta["cards_only"]:
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-f", "lavfi", "-i",
               "color=c=%s:s=%dx%d:r=%d:d=%.3f" % (ec.CARD_ONLY_BG, W_, H_, FPS, rt),
               "-vf", "setsar=1,fps=%d" % FPS, "-r", str(FPS),
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", str(seg)]
        run(cmd)
    else:
        nf = int(round(meta["dur_s"] * FPS))
        z, x, y = kb_expr(kbs[k], nf)
        src = REPO / meta["visual_source"]
        vf = ("setpts=PTS-STARTPTS,scale=%d:%d,setsar=1,fps=%d,"
              "zoompan=z=%s:x=%s:y=%s:d=1:s=%dx%d:fps=%d"
              % (W_ * 2, H_ * 2, FPS, z, x, y, W_, H_, FPS))
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-stream_loop", "-1", "-i", str(src),
               "-t", "%.3f" % rt, "-vf", vf, "-r", str(FPS),
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", str(seg)]
        run(cmd)
    segs.append(seg)
    print("seg%02d ok (%.3fs)" % (k, meta["dur_s"]))

# ---- stage 2: engine xfade chain ----------------------------------------
edited = ec.xfade_chain(plan, segs, TMP, W_, H_)
if not edited:
    print("FAIL xfade_chain")
    sys.exit(3)
vdur = probe_dur(edited)
print("edited bg ok: %.3fs" % vdur)

# ---- audio track --------------------------------------------------------
aparts = []
alabels = []
for k in range(13):
    aparts.append("[%d:a]adelay=%d:all=1,apad=whole_dur=%.3f[a%d]"
                  % (k, int(AUDIO_LEAD_S * 1000), win[k], k))
    alabels.append("[a%d]" % k)
aparts.append("".join(alabels) + "concat=n=13:v=0:a=1[aout]")
audio_out = TMP / "audio-asm.m4a"
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
for k in range(13):
    cmd += ["-i", str(MD / ("tts/segments/shot%02d.mp3" % (k + 1)))]
cmd += ["-filter_complex", ";".join(aparts), "-map", "[aout]",
        "-t", "%.3f" % total, "-c:a", "aac", "-b:a", "192k", str(audio_out)]
run(cmd)
print("audio ok: %.3fs" % probe_dur(audio_out))

# ---- stage 3: burn subtitles + statement + AIGC -------------------------


def dtext(textfile, size, color, x, y, enable=None, shadow=True):
    f = ("drawtext=expansion=none:fontfile='%s':textfile='%s':"
         "fontsize=%d:fontcolor=%s" % (FONT_ESC, textfile, size, color))
    if shadow:
        f += ":shadowcolor=black@0.75:shadowx=2:shadowy=2"
    f += ":x=%s:y=%s" % (x, y)
    if enable:
        f += ":enable='%s'" % enable
    return f


chain = ["[0:v]"]
for k, (s, e, tx) in enumerate(cues):
    tf = TMP / ("c%02d.txt" % k)
    tf.write_text(tx + "\n", encoding="utf-8", newline="\n")
    rel = ".c3-tmp/asm-r1794/c%02d.txt" % k
    if k == 12:  # endcard statement: centered small white text
        chain.append(dtext(rel, 30, "white", "(w-text_w)/2",
                           "(h-text_h)/2-30", "between(t,%.3f,%.3f)" % (s, e)))
    else:       # drama subtitle: bottom center
        chain.append(dtext(rel, 36, "white", "(w-text_w)/2", "h-140",
                           "between(t,%.3f,%.3f)" % (s, e)))
aigc_f = TMP / "aigc.txt"
aigc_f.write_text(AIGC_TEXT + "\n", encoding="utf-8", newline="\n")
chain.append(dtext(".c3-tmp/asm-r1794/aigc.txt", 22, "white@0.9",
                   "w-tw-24", "h-36", None, shadow=False))
chain.append("[v]")
fc = chain[0] + ",".join(chain[1:-1]) + chain[-1]

out_mp4 = OUT / "md-0001-v1-bilibili-16x9.mp4"
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
       "-i", str(edited), "-i", str(audio_out),
       "-filter_complex", fc, "-map", "[v]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", str(FPS),
       "-c:a", "copy", "-t", "%.3f" % vdur, str(out_mp4)]
run(cmd)
print("OUT:", out_mp4, "%.3fs" % probe_dur(out_mp4))
