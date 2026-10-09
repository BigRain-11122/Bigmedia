# -*- coding: utf-8 -*-
"""faster-whisper -> SRT alignment tool (M2 local chain PoC R-C).

Path A of the dual-path subtitle alignment: ASR with word timestamps
works for ANY audio, including Jason's real voice (persona rule: real
voice first, AI voice only fills gaps). Path B (edge-tts
--write-subtitles, see tts-samples README) only works when the audio
itself is synthesized - so path B is the draft fast-lane and this tool
is the universal lane.

CPU int8 by default (shared-machine etiquette, m2-local-stack S2:
no VRAM contention with the Ollama residents).

C2 calibration (queue R169, v12 mother track = cyber light voice,
57s BGM mix, ref = v11-trim beats, char-level Levenshtein CER):
- small int8 baseline (this tool's defaults) raw CER 13.07%
- beam_size=5: no measurable change (params are noise-level here)
- condition_on_previous_text=False: ~1 char gain + ~30% faster
- domain initial_prompt: DEGRADED (new homophone errors on small)
- medium int8 + beam5 + no-context: raw CER 5.53% -> model size is
  the dominant factor (homophone sites 12 -> 8, real-word damage
  still zero; first model download ~1min, then ~21s per 57s clip)
S2 asr-check QC recipe: --model medium --beam-size 5 --no-context
plus per-piece proper-noun preload via --initial-prompt (P-3 pilot
R1410, A/B on BS-003/BS-004 terminal tracks: proper-noun degraded
sites 13 -> 5 = 62% cut, prompt leakage 0, char-noise rate down on
both tracks; prompt = the piece's own fact-word list, terms already
present in the piece only); small (defaults) stays the fast lane.
Defaults unchanged on purpose: no behavior change without measured
gain.

HF_HUB_OFFLINE pitfall (R638, canonized R644): faster-whisper model
load does an online HF-hub etag check by default; on this machine
that check can hang indefinitely (360MB stalled WS, 20min zero
progress, kill + relaunch needed). Production default env:
    HF_HUB_OFFLINE=1
set it in the shell (or process env) before the first model load
when the local cache is already populated (1.53GB @ 09-24 anchor).
whisper.cpp (ggml path, MIT, OH-20260929-bigstream parked) removes
this class of failure entirely: local ggml model files, no hub.

P-2 pinned-model law (queue R1300 proposal, R1302 pilot): the S2 QC
medium model is pinned at data/assets/models/faster-whisper-medium
(real files, gitignored per the model-file law, outside the group
disk-sweep Class-A list). resolve_model() prefers the pinned copy and
falls back to the hub name when absent. Five-incident chain anchor:
R701/R761/R801/R806/R809 (+ R1302 open = sixth) - HF cache swept
while the ASR lane depends on it, 1.46GB re-download each time.
Pinned loads read the local dir directly: no hub contact, no etag
check, so the R638 offline-hang class does not apply either. Pin
record + integrity observation face: data/pipeline/asr-pin.json
(readiness probe asr-pin check).

Usage:
    python src/render/whisper_to_srt.py --audio a.mp3 --out a.srt
    python src/render/whisper_to_srt.py --audio a.mp3 --out a.srt --model small
    python src/render/whisper_to_srt.py --audio a.mp3 --out a.srt \
        --model medium --beam-size 5 --no-context   # S2 QC pass

ASCII rule: code/comments English; Chinese only in data files.
Exit codes: 0 ok; 2 bad args/model or transcription error.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from srt_fix import clamp_overlaps, write_srt  # noqa: E402


# clause/sentence enders; kept as escapes per the ASCII code rule
BREAK_PUNCT = set(",.!?;..." + "\uff0c\u3002\uff01\uff1f\uff1b\u3001\u2026")

# P-2 pinned-model store: data/assets/models/ (gitignored, sweep-safe)
PINNED_MODELS_DIR = Path(__file__).resolve().parents[2] / "data" / "assets" / "models"


def resolve_model(model_size):
    """P-2 pinned-model law: return the pinned local dir for model_size
    when the pinned copy exists, else the value unchanged (hub name or
    explicit caller path). Pinned loads skip the HF hub entirely."""
    if "\\" in model_size or "/" in model_size or Path(model_size).exists():
        return model_size  # explicit path from caller: respect as-is
    pinned = PINNED_MODELS_DIR / ("faster-whisper-%s" % model_size)
    if (pinned / "model.bin").is_file():
        return str(pinned)
    return model_size


def build_cues(words, max_chars=20):
    """Group word timestamps into cues of at most ~max_chars visible
    chars. Cues close on: silence gaps > 1s, a punctuation ender once
    the cue is at least half budget (natural clause end), or overflow
    (preferring the last in-cue punctuation over a mid-word hard cut -
    CJK word tokens are often single chars). Pure function."""
    cues, cur = [], []
    cur_len = 0

    def close_upto(idx):
        nonlocal cur_len
        head, tail = cur[:idx + 1], cur[idx + 1:]
        cues.append((head[0][0], head[-1][1],
                     "".join(t for _, _, t in head).strip()))
        del cur[:idx + 1]
        cur_len = sum(len(t.strip()) for _, _, t in cur)

    for w in words:
        s, e, t = float(w["start"]), float(w["end"]), str(w["word"])
        if not t.strip():
            continue
        if cur and s - cur[-1][1] > 1.0:
            close_upto(len(cur) - 1)
        cur.append((s, e, t))
        cur_len += len(t.strip())
        if t.strip()[-1] in BREAK_PUNCT and cur_len >= max_chars * 0.5:
            close_upto(len(cur) - 1)
        elif cur_len > max_chars:
            if len(cur) == 1:
                close_upto(0)  # single oversize token: keep it whole
            else:
                cut = max(
                    (i for i in range(len(cur) - 1)
                     if cur[i][2].strip() and cur[i][2].strip()[-1] in BREAK_PUNCT),
                    default=len(cur) - 2)
                close_upto(cut)
                while len(cur) > 1 and cur_len > max_chars:
                    close_upto(len(cur) - 2)
    if cur:
        close_upto(len(cur) - 1)
    return cues


def load_noise_dict(path):
    """Load the ASR noise dictionary (opt-in, tech#12 R1827).
    Returns list of (noise, true, cls) sorted longest-noise-first so a
    longer phrase entry always wins over a substring entry. Data file:
    data/pipeline/asr-noise-dict-v1.json (evidence-anchored pairs).
    QC-channel only - never wire this into real-voice lanes."""
    import json
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = [(str(e["noise"]), str(e["true"]), str(e.get("class", "guarded")))
               for e in data.get("entries", [])]
    entries.sort(key=lambda x: len(x[0]), reverse=True)
    return entries


def apply_noise_dict(cues, entries, expect_text=None):
    """Replace noise->true in cue text. 'safe' entries fire
    unconditionally; 'guarded' entries only fire when expect_text
    (the piece's own beats) contains the true term - collision
    guard so a common-word mishear never rewrites legitimate text
    in a piece that does not contain the true term. Pure function;
    timestamps untouched. Returns (new_cues, applied, skipped_guard)."""
    out, applied, skipped = [], 0, 0
    for s, e, text in cues:
        for noise, true, cls in entries:
            if noise not in text:
                continue
            if cls == "safe" or (expect_text is not None and true in expect_text):
                text = text.replace(noise, true)
                applied += 1
            else:
                skipped += 1
        out.append((s, e, text))
    return out, applied, skipped


def transcribe_to_cues(audio, model_size="small", language="zh",
                       max_chars=20, beam_size=1,
                       condition_on_previous_text=True,
                       initial_prompt=None):
    """Run faster-whisper CPU int8 with word timestamps, return
    (cues, dropped, info_duration). C2 param face exposed here;
    see module docstring for measured calibration values."""
    from faster_whisper import WhisperModel
    model = WhisperModel(resolve_model(model_size), device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(audio), language=language, word_timestamps=True, vad_filter=True,
        beam_size=beam_size,
        condition_on_previous_text=condition_on_previous_text,
        initial_prompt=initial_prompt)
    words = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({"start": w.start, "end": w.end, "word": w.word})
    cues = build_cues(words, max_chars)
    fixed, dropped = clamp_overlaps(cues)
    return fixed, dropped, float(getattr(info, "duration", 0.0))


def build_parser():
    ap = argparse.ArgumentParser(description="faster-whisper SRT alignment")
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--max-chars", type=int, default=20)
    ap.add_argument("--beam-size", type=int, default=1,
                    help="beam width; 1 = greedy (measured: no gain "
                         "on the cyber-light track class)")
    ap.add_argument("--no-context", action="store_true",
                    help="condition_on_previous_text=False; short-clip "
                         "QC recipe (measured: ~1 char gain, ~30%% faster)")
    ap.add_argument("--initial-prompt", default=None,
                    help="domain bias prompt (small model: measured "
                         "DEGRADED, use with caution; P-3 pilot R1410: "
                         "medium-int8 + targeted per-piece proper-noun "
                         "preload MEASURED GAIN - 62 percent proper-noun "
                         "degradation cut, zero leak)")
    ap.add_argument("--noise-dict", default=None,
                    help="OPT-IN homophone noise dictionary (tech#12 "
                         "R1827, data/pipeline/asr-noise-dict-v1.json). "
                         "S2 asr-check QC channel only; default off = "
                         "zero behavior change; never for real-voice "
                         "transcripts")
    ap.add_argument("--expect", default=None,
                    help="reference text (the piece's own beats file) "
                         "for the guarded-entry collision gate; only "
                         "meaningful together with --noise-dict")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    audio = Path(args.audio)
    if not audio.exists():
        print("FAIL audio not found: %s" % audio)
        return 2
    try:
        cues, dropped, dur = transcribe_to_cues(
            audio, args.model, args.language, args.max_chars,
            beam_size=args.beam_size,
            condition_on_previous_text=not args.no_context,
            initial_prompt=args.initial_prompt)
    except Exception as e:  # model load/download or transcription failure
        print("FAIL transcribe: %s: %s" % (type(e).__name__, e))
        return 2
    if not cues:
        print("FAIL no cues produced for %s" % audio)
        return 2
    if args.noise_dict:
        entries = load_noise_dict(args.noise_dict)
        expect_text = None
        if args.expect:
            expect_path = Path(args.expect)
            if not expect_path.exists():
                print("FAIL expect reference not found: %s" % expect_path)
                return 2
            expect_text = expect_path.read_text(encoding="utf-8")
        cues, applied, skipped = apply_noise_dict(cues, entries, expect_text)
        print("noise-dict: entries=%d applied=%d skipped_guard=%d expect=%s"
              % (len(entries), applied, skipped,
                 "yes" if expect_text is not None else "no"))
    write_srt(cues, args.out)
    print("OK %s -> %s cues=%d dropped=%d audio_dur=%.2fs model=%s-int8-cpu"
          % (audio, args.out, len(cues), dropped, dur, args.model))
    return 0


if __name__ == "__main__":
    sys.exit(main())
