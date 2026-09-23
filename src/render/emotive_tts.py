# -*- coding: utf-8 -*-
"""BigStream emotive TTS - sentence-level prosody variation (order O-1918).

Beats file (UTF-8 data), one beat per line:
    PROFILE | card line 1 / card line 2 / ... | spoken text

Each beat is synthesized with its PROFILE's edge-tts rate/pitch flags, so the
voice rises and falls across the script instead of droning at one setting.
Outputs (to --out DIR):
    audio.mp3      concatenated segments (ffmpeg concat demuxer)
    subs.srt       one cue per beat, cumulative offsets via ffprobe
    cards.json     beat-aligned card timeline (card cut = word boundary =
                   the cut-point discipline of O-1918)
    voiceover.txt  plain spoken text (renderer --strict baseline)

Encoding rule: this source is pure ASCII; Chinese lives in the beats file.
Usage:
    python src/render/emotive_tts.py --beats FILE --voice VOICE --out DIR
"""
import json
import subprocess
import sys
from pathlib import Path

PROFILES = {
    "hook":  ["--rate=-8%", "--pitch=-3Hz"],
    "punch": ["--rate=+6%", "--pitch=+3Hz"],
    "body":  [],
    "wink":  ["--rate=+8%", "--pitch=+4Hz"],
    "turn":  ["--rate=-10%", "--pitch=-2Hz"],
    "beat":  ["--rate=-14%", "--pitch=-4Hz"],
    "proof": ["--rate=+5%", "--pitch=+2Hz"],
    "close": ["--rate=-10%", "--pitch=-2Hz"],
    "cta":   ["--rate=+3%", "--pitch=+2Hz"],
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL: %s" % " ".join(cmd))
        print(r.stderr[-1000:])
        sys.exit(1)
    return r


def probe_dur(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)])
    return float(r.stdout.strip())


def fmt_ts(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms >= 1000:
        ms = 999
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def main(argv):
    beats_path = voice = out_dir = None
    i = 1
    while i < len(argv):
        if argv[i] == "--beats":
            i += 1
            beats_path = Path(argv[i])
        elif argv[i] == "--voice":
            i += 1
            voice = argv[i]
        elif argv[i] == "--out":
            i += 1
            out_dir = Path(argv[i])
        i += 1
    if not (beats_path and voice and out_dir):
        print("usage: emotive_tts.py --beats FILE --voice VOICE --out DIR")
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    beats = []
    for line in beats_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            print("FAIL bad beat line: %s" % line[:40])
            return 2
        profile, card, spoken = parts
        if profile not in PROFILES:
            print("FAIL unknown profile: %s" % profile)
            return 2
        beats.append({"profile": profile,
                      "card_lines": [c.strip() for c in card.split("/") if c.strip()],
                      "text": spoken})

    segs, cues, cards, spoken_lines = [], [], [], []
    t0 = 0.0
    for idx, b in enumerate(beats):
        seg = out_dir / ("seg%02d.mp3" % idx)
        cmd = ["edge-tts", "--voice", voice] + PROFILES[b["profile"]] + \
              ["--text", b["text"], "--write-media", str(seg)]
        run(cmd)
        d = probe_dur(seg)
        segs.append(seg)
        cues.append((idx + 1, t0, t0 + d, b["text"]))
        cards.append({"start": round(t0, 2), "end": None,
                     "lines": b["card_lines"]})
        spoken_lines.append(b["text"])
        t0 += d

    for c in cards:
        pass
    for j, c in enumerate(cards):
        c["end"] = round(cues[j + 1][1], 2) if j + 1 < len(cards) else round(t0, 2)

    lst = out_dir / "concat.txt"
    lst.write_text("\n".join("file '%s'" % s.resolve().as_posix() for s in segs),
                   encoding="ascii")
    audio = out_dir / "audio.mp3"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c:a", "libmp3lame", "-qscale:a", "4", str(audio)])

    srt = out_dir / "subs.srt"
    srt_lines = []
    for idx, a, z, text in cues:
        srt_lines += [str(idx), "%s --> %s" % (fmt_ts(a), fmt_ts(z)), text, ""]
    srt.write_text("\n".join(srt_lines), encoding="utf-8")

    (out_dir / "voiceover.txt").write_text(
        "\n".join(spoken_lines) + "\n", encoding="utf-8")

    meta = {
        "meta": {
            "topic": "v3-emotive",
            "variant": "shipinhao 60s card cut (9:16)",
            "tool": "src/render/emotive_tts.py",
            "voice": voice,
            "beats": str(beats_path),
            "order": "O-20260923-1918-bm-a (emotive voice + beat-aligned cuts)",
            "storyboard": "one beat = one card = one cut (cut on word boundary)",
            "red_line": "aigc_notice burns into every frame for the full duration (CONSTITUTION §2-4); publish also requires M4 gate + platform AIGC switch",
        },
        "video": {"width": 1080, "height": 1920, "fps": 30, "bg": "black"},
        "font": {
            "file": "C:/Windows/Fonts/msyh.ttc",
            "cards_size": 60,
            "subs_size": 44,
            "aigc_size": 30,
            "subs_bottom": 300,
            "line_spacing": 14,
        },
        "aigc_notice": "\u672c\u89c6\u9891\u7531 AI \u751f\u6210 \u00b7 AIGC \u4f9d\u6cd5\u6807\u8bc6",
        "tail": 0.8,
        "cards": cards,
    }
    (out_dir / "cards.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("OK beats=%d duration=%.2fs audio=%s" % (len(beats), t0, audio))
    for idx, a, z, text in cues:
        print("  cue%02d %6.2fs-%6.2fs %s" % (idx, a, z, text[:18]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
