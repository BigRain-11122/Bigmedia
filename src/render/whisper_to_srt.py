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

Usage:
    python src/render/whisper_to_srt.py --audio a.mp3 --out a.srt
    python src/render/whisper_to_srt.py --audio a.mp3 --out a.srt --model small

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


def transcribe_to_cues(audio, model_size="small", language="zh",
                       max_chars=20):
    """Run faster-whisper CPU int8 with word timestamps, return
    (cues, dropped, info_duration)."""
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(audio), language=language, word_timestamps=True, vad_filter=True)
    words = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({"start": w.start, "end": w.end, "word": w.word})
    cues = build_cues(words, max_chars)
    fixed, dropped = clamp_overlaps(cues)
    return fixed, dropped, float(getattr(info, "duration", 0.0))


def main(argv=None):
    ap = argparse.ArgumentParser(description="faster-whisper SRT alignment")
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--max-chars", type=int, default=20)
    args = ap.parse_args(argv)
    audio = Path(args.audio)
    if not audio.exists():
        print("FAIL audio not found: %s" % audio)
        return 2
    try:
        cues, dropped, dur = transcribe_to_cues(
            audio, args.model, args.language, args.max_chars)
    except Exception as e:  # model load/download or transcription failure
        print("FAIL transcribe: %s: %s" % (type(e).__name__, e))
        return 2
    if not cues:
        print("FAIL no cues produced for %s" % audio)
        return 2
    write_srt(cues, args.out)
    print("OK %s -> %s cues=%d dropped=%d audio_dur=%.2fs model=%s-int8-cpu"
          % (audio, args.out, len(cues), dropped, dur, args.model))
    return 0


if __name__ == "__main__":
    sys.exit(main())
