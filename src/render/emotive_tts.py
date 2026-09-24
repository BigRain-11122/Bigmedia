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

Human-feel dial (O-20260923-2210-bm-a: remove the cheap AI-generated feel
from the bottom layer; seeded = fully reproducible):
    --human SEED           micro-prosody jitter per segment (rate +-3%,
    pitch +-2Hz), varied breathing gaps between beats (0.12-0.48s instead
    of TTS's zero-gap metronome), a synthesized breath after long
    sentences (brown-noise, band-passed, ~50% of boundaries), and a low
    room-tone noise bed under the voice. Cue/card timeline follows the
    actual probed durations of every inserted element - no drift.

Encoding rule: this source is pure ASCII; Chinese lives in the beats file.
Usage:
    python src/render/emotive_tts.py --beats FILE --voice VOICE --out DIR
        [--cyber light|mid|full] [--human SEED]
        [--template CARDS_JSON] [--order STR]
"""
import json
import random
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


# ---- human-feel dial (O-20260923-2210-bm-a) -------------------------------
# The tells of a cheap AI voice track: every sentence the exact same voice
# settings, zero gap between sentences (TTS metronome), no air, no breath.
# These helpers add seeded micro-variance; the seed keeps renders
# reproducible so reviews/ASR gates are stable across re-runs.

HUMAN_RATE_JIT = (-3, 3)     # % per segment
HUMAN_PITCH_JIT = (-2, 2)     # Hz per segment
HUMAN_GAP_BASE = 0.30         # s between beats (mid point)
HUMAN_GAP_SPREAD = 0.18       # +- s -> 0.12..0.48 realized range
HUMAN_BREATH_AFTER_S = 4.2   # insert breath after segments this long
HUMAN_BREATH_PROB = 0.5       # ...but only with this probability
HUMAN_ROOMTONE_AMP = 0.006    # pink noise bed amplitude (~-44 dB)


def human_series(seed, n):
    """Seeded per-segment jitter plan: [(rate_jit, pitch_jit), ...]."""
    rng = random.Random(seed)
    return [(rng.randint(*HUMAN_RATE_JIT), rng.randint(*HUMAN_PITCH_JIT))
            for _ in range(n)]


def boundary_plan(seed, durations):
    """Seeded plan for the n-1 boundaries between beats: list of
    {"gap": seconds, "breath": bool} keyed off the duration of the beat
    BEFORE the boundary. Deterministic in (seed, durations)."""
    rng = random.Random((seed * 7919) + 17)
    plan = []
    for d in durations[:-1]:
        gap = round(HUMAN_GAP_BASE + rng.uniform(-HUMAN_GAP_SPREAD,
                                                 HUMAN_GAP_SPREAD), 3)
        breath = d >= HUMAN_BREATH_AFTER_S and rng.random() < HUMAN_BREATH_PROB
        plan.append({"gap": gap, "breath": breath})
    return plan


def jitter_flags(flags, rate_jit, pitch_jit):
    """Apply per-segment jitter to a profile flag list: existing rate/pitch
    values shift, absent flags are added (body has none = pure default)."""
    out = []
    seen_rate = seen_pitch = False
    for f in flags:
        if f.startswith("--rate="):
            val = int(f[len("--rate="):].rstrip("%"))
            out.append("--rate=%+d%%" % (val + rate_jit))
            seen_rate = True
        elif f.startswith("--pitch="):
            val = int(f[len("--pitch="):].rstrip("Hz"))
            out.append("--pitch=%+dHz" % (val + pitch_jit))
            seen_pitch = True
        else:
            out.append(f)
    if not seen_rate:
        out.append("--rate=%+d%%" % rate_jit)
    if not seen_pitch:
        out.append("--pitch=%+dHz" % pitch_jit)
    return out


def parse_beats(path):
    """Parse the beats file (PROFILE | card a / card b | spoken text).
    Shared with src/ai_feel_check.py - single source of the data
    contract. Raises ValueError on malformed lines."""
    beats = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            raise ValueError("bad beat line: %s" % line[:40])
        profile, card, spoken = parts
        if profile not in PROFILES:
            raise ValueError("unknown profile: %s" % profile)
        beats.append({"profile": profile,
                      "card_lines": [c.strip() for c in card.split("/") if c.strip()],
                      "text": spoken})
    return beats


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
    human_seed = None
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
        elif argv[i] == "--human":
            i += 1
            human_seed = int(argv[i])
        i += 1
    if not (beats_path and voice and out_dir):
        print("usage: emotive_tts.py --beats FILE --voice VOICE --out DIR"
              " [--cyber light|mid|full] [--human SEED]"
              " [--template CARDS_JSON] [--order STR]")
        return 2
    if cyber and cyber not in CYBER_CHAINS:
        print("FAIL unknown --cyber level: %s (light|mid|full)" % cyber)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = PROFILES
    if cyber in CYBER_PITCH_HZ:
        profiles = cyberize(PROFILES, CYBER_PITCH_HZ[cyber],
                            CYBER_RATE_SHIFT[cyber])

    beats = parse_beats(beats_path)

    # ---- phase 1: synthesize segments (with per-segment human jitter) --
    jit = human_series(human_seed, len(beats)) if human_seed is not None else None
    durations = []
    for idx, b in enumerate(beats):
        seg = out_dir / ("seg%02d.mp3" % idx)
        flags = profiles[b["profile"]]
        if jit:
            flags = jitter_flags(flags, *jit[idx])
        cmd = ["edge-tts", "--voice", voice] + flags + \
              ["--text", b["text"], "--write-media", str(seg)]
        run(cmd)
        d = probe_dur(seg)
        durations.append(d)

    # ---- phase 2: boundary elements + cue/card timeline --------------
    # human off = zero-gap TTS metronome (the classic AI tell); human on =
    # seeded varied gaps (+ optional breaths), timeline follows probed
    # durations of every inserted element, so SRT/cards never drift.
    if human_seed is not None:
        plan = boundary_plan(human_seed, durations)
    else:
        plan = [{"gap": 0.0, "breath": False} for _ in range(len(beats) - 1)]

    segs, cues, cards, spoken_lines = [], [], [], []
    t0 = 0.0
    for idx, b in enumerate(beats):
        seg = out_dir / ("seg%02d.mp3" % idx)
        d = durations[idx]
        segs.append(seg)
        cues.append((idx + 1, t0, t0 + d, b["text"]))
        cards.append({"start": round(t0, 2), "end": None,
                     "lines": b["card_lines"]})
        spoken_lines.append(b["text"])
        t0 += d
        if idx < len(plan):
            item = plan[idx]
            if item["breath"]:
                br = out_dir / ("breath%02d.mp3" % idx)
                run(["ffmpeg", "-y",
                     "-f", "lavfi", "-i",
                     "anoisesrc=color=brown:amplitude=0.05:duration=0.22:seed=%d"
                     % (101 + idx),
                     "-af", "highpass=f=200,lowpass=f=800,afade=t=in:d=0.05,"
                            "afade=t=out:st=0.13:d=0.09",
                     "-ar", "24000", "-ac", "1",
                     "-c:a", "libmp3lame", "-qscale:a", "4", str(br)])
                segs.append(br)
                t0 += probe_dur(br)
            if item["gap"] > 0:
                si = out_dir / ("gap%02d.mp3" % idx)
                run(["ffmpeg", "-y", "-f", "lavfi",
                     "-i", "anullsrc=r=24000:cl=mono",
                     "-t", "%.3f" % item["gap"],
                     "-c:a", "libmp3lame", "-qscale:a", "4", str(si)])
                segs.append(si)
                t0 += probe_dur(si)

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

    if human_seed is not None:
        # room tone + a whisper of early reflections: kills the "raw TTS
        # in a vacuum" feel. Duration preserved (noise bed = same length).
        pre = probe_dur(audio)
        raw = out_dir / "audio-pre-room.mp3"
        audio.replace(raw)
        run(["ffmpeg", "-y", "-i", str(raw),
             "-f", "lavfi", "-i",
             "anoisesrc=color=pink:amplitude=%g:duration=%.3f"
             % (HUMAN_ROOMTONE_AMP, pre),
             "-filter_complex",
             "[0:a]aecho=0.6:0.12:11|23:0.05|0.03[v];"
             "[1:a]lowpass=f=4000[nt];"
             "[v][nt]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "[a]", "-c:a", "libmp3lame", "-qscale:a", "4", str(audio)])
        post = probe_dur(audio)
        if abs(post - pre) > 0.35:
            print("FAIL room-tone mix drifted duration %.2fs -> %.2fs" % (pre, post))
            return 1
        print("OK human=seed%d room tone %.2fs -> %.2fs" % (human_seed, pre, post))

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
    if human_seed is not None:
        meta["human"] = {
            "seed": human_seed,
            "gap_base_s": HUMAN_GAP_BASE,
            "gap_spread_s": HUMAN_GAP_SPREAD,
            "breath_after_s": HUMAN_BREATH_AFTER_S,
            "breath_prob": HUMAN_BREATH_PROB,
            "roomtone_amp": HUMAN_ROOMTONE_AMP,
        }

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
        # 2026-09-25 #23 v14 + D-BS-03 4.5: mechanical square-bracket
        # AIGC body (prose notice retired with this batch).
        "aigc_notice": base_cfg.get(
            "aigc_notice", "[AIGC\u00b7AI \u751f\u6210\u5185\u5bb9]"),
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
