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

Cyber voice dial (O-20260923-2136-bm-a: voice more cyber/robotic):
    --cyber light|mid|full   post-processing texture on the final audio.
    light = keep emotive prosody, add subtle machine texture;
    mid   = flatten pitch to robot monotone + metallic chain;
    full  = deep-synthesis chain (pitch dropped, band-limited, crushed).
    Chains are duration-preserving (asetrate drop compensated by atempo),
    asserted by ffprobe before/after, so SRT cues and card cuts stay valid.

    --template CARDS_JSON  adopt font/video/aigc_notice/tail/meta sections
                           from an existing cards file (e.g. the v7-vis
                           visual-spec template) instead of built-in defaults.
    --order STR            override meta.order for provenance.

Encoding rule: this source is pure ASCII; Chinese lives in the beats file.
Usage:
    python src/render/emotive_tts.py --beats FILE --voice VOICE --out DIR
        [--cyber light|mid|full] [--template CARDS_JSON] [--order STR]
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

# O-20260923-2136-bm-a cyber dial: light keeps the emotive melody and only
# adds texture; mid/full flatten pitch to robot monotone (rate variation
# stays = rhythm preserved, melody removed) and push the texture harder.
# Every chain is duration-preserving: the asetrate pitch drop is exactly
# compensated by atempo=1/factor, everything else (vibrato/acrusher/EQ/
# echo) keeps sample count - so SRT cues and card cuts stay valid.
CYBER_PITCH_HZ = {"mid": -8, "full": -12}
CYBER_RATE_SHIFT = {"mid": "-4%", "full": "-8%"}

CYBER_CHAINS = {
    # cold narrator: barely machined, fully intelligible
    "light": ("highpass=f=110,lowpass=f=7800,"
              "vibrato=f=30:d=0.10,"
              "acrusher=bits=10:mode=log:aa=0.15:mix=0.50,"
              "alimiter=limit=0.95"),
    # standard robot: metallic flutter + band-limited + light slapback
    "mid": ("asetrate=24000*0.95,aresample=48000,atempo=1.0526,"
            "highpass=f=150,lowpass=f=5200,"
            "vibrato=f=42:d=0.22,"
            "acrusher=bits=8:mode=log:aa=0.12:mix=0.80,"
            "aecho=0.6:0.25:22|38:0.10|0.06,"
            "alimiter=limit=0.95"),
    # deep synthesis: pitch-dropped terminal voice, rate-crushed
    "full": ("asetrate=24000*0.90,aresample=48000,atempo=1.1111,"
             "highpass=f=180,lowpass=f=3800,"
             "vibrato=f=52:d=0.32,"
             "acrusher=bits=7:mode=log:aa=0.10:samples=3:mix=0.85,"
             "aecho=0.6:0.30:18|33|60:0.12|0.08|0.05,"
             "alimiter=limit=0.90"),
}


def cyberize(profiles, pitch_hz, rate_shift):
    """Flatten a profile table toward robot monotone: uniform pitch, rate
    variation kept (rhythm stays, melody goes) plus a global rate shift."""
    shift = int(rate_shift.rstrip("%"))
    out = {}
    for name, flags in profiles.items():
        new_flags = []
        for f in flags:
            if f.startswith("--rate="):
                val = int(f[len("--rate="):].rstrip("%"))
                new_flags.append("--rate=%+d%%" % (val + shift))
            elif f.startswith("--pitch="):
                continue
            else:
                new_flags.append(f)
        new_flags.append("--pitch=%dHz" % pitch_hz)
        out[name] = new_flags
    return out


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
    cyber = template = order = None
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
        elif argv[i] == "--cyber":
            i += 1
            cyber = argv[i]
        elif argv[i] == "--template":
            i += 1
            template = argv[i]
        elif argv[i] == "--order":
            i += 1
            order = argv[i]
        i += 1
    if not (beats_path and voice and out_dir):
        print("usage: emotive_tts.py --beats FILE --voice VOICE --out DIR"
              " [--cyber light|mid|full] [--template CARDS_JSON] [--order STR]")
        return 2
    if cyber and cyber not in CYBER_CHAINS:
        print("FAIL unknown --cyber level: %s (light|mid|full)" % cyber)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = PROFILES
    if cyber in CYBER_PITCH_HZ:
        profiles = cyberize(PROFILES, CYBER_PITCH_HZ[cyber],
                            CYBER_RATE_SHIFT[cyber])

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
        cmd = ["edge-tts", "--voice", voice] + profiles[b["profile"]] + \
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

    if cyber:
        pre = probe_dur(audio)
        raw = out_dir / "audio-raw.mp3"
        audio.replace(raw)
        run(["ffmpeg", "-y", "-i", str(raw), "-af", CYBER_CHAINS[cyber],
             "-c:a", "libmp3lame", "-qscale:a", "4", str(audio)])
        post = probe_dur(audio)
        if abs(post - pre) > 0.35:
            print("FAIL cyber chain drifted duration %.2fs -> %.2fs"
                  " (SRT/card timeline would break)" % (pre, post))
            return 1
        print("OK cyber=%s voice %.2fs -> %.2fs (chain preserved timeline)"
              % (cyber, pre, post))

    srt = out_dir / "subs.srt"
    srt_lines = []
    for idx, a, z, text in cues:
        srt_lines += [str(idx), "%s --> %s" % (fmt_ts(a), fmt_ts(z)), text, ""]
    srt.write_text("\n".join(srt_lines), encoding="utf-8")

    (out_dir / "voiceover.txt").write_text(
        "\n".join(spoken_lines) + "\n", encoding="utf-8")

    base_cfg = {}
    if template:
        base_cfg = json.loads(Path(template).read_text(encoding="utf-8"))
        notice = str(base_cfg.get("aigc_notice", "")).strip()
        if not notice:
            print("FAIL template %s has empty aigc_notice (red line)" % template)
            return 2

    meta = dict(base_cfg.get("meta") or {})
    meta.update({
        "topic": meta.get("topic", "v3-emotive"),
        "variant": meta.get("variant", "shipinhao 60s card cut (9:16)"),
        "tool": "src/render/emotive_tts.py",
        "voice": voice,
        "beats": str(beats_path),
        "order": order or meta.get(
            "order", "O-20260923-1918-bm-a (emotive voice + beat-aligned cuts)"),
    })
    if cyber:
        meta["cyber"] = {"level": cyber, "chain": CYBER_CHAINS[cyber]}

    cards_doc = {
        "meta": meta,
        "video": base_cfg.get("video") or {
            "width": 1080, "height": 1920, "fps": 30, "bg": "black"},
        "font": base_cfg.get("font") or {
            "file": "C:/Windows/Fonts/msyh.ttc",
            "cards_size": 60,
            "subs_size": 44,
            "aigc_size": 30,
            "subs_bottom": 300,
            "line_spacing": 14,
        },
        "aigc_notice": base_cfg.get(
            "aigc_notice", "\u672c\u89c6\u9891\u7531 AI \u751f\u6210 \u00b7 AIGC \u4f9d\u6cd5\u6807\u8bc6"),
        "tail": base_cfg.get("tail", 0.8),
        "cards": cards,
    }
    (out_dir / "cards.json").write_text(
        json.dumps(cards_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("OK beats=%d duration=%.2fs audio=%s" % (len(beats), t0, audio))
    for idx, a, z, text in cues:
        print("  cue%02d %6.2fs-%6.2fs %s" % (idx, a, z, text[:18]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
