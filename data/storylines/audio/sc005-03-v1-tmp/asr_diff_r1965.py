# -*- coding: utf-8 -*-
"""SC-005-03-v1 ASR final-track diff quantification (S2 evidence).

Adapted from asr_diff_r1963.py (SC-005-01, R1963) for the SC-005-03
final track: compares the whisper medium-int8-cpu QC transcript against
the TTS source lines, reports site/char counts and char-position rate.
Difflib on a normalized char stream (strip punctuation/spaces/latin case).
"""
import difflib
import io
import re
import sys

SRC_TEXT = "data/storylines/audio/sc005-03-v1-tmp/voiceover.txt"
SRT = "data/storylines/audio/sc005-03-v1-tmp/asr-check.srt"


def load_srt_text(path):
    lines = io.open(path, encoding="utf-8-sig").read().splitlines()
    out = []
    for ln in lines:
        if ln.strip().isdigit() or "-->" in ln or not ln.strip():
            continue
        out.append(ln.strip())
    return "".join(out)


def norm(s):
    s = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", s)
    return s.lower()


def main():
    src = norm(io.open(SRC_TEXT, encoding="utf-8").read())
    asr = norm(load_srt_text(SRT))
    sm = difflib.SequenceMatcher(a=src, b=asr, autojunk=False)
    sites = 0
    diff_chars = 0
    details = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        sites += 1
        diff_chars += max(i2 - i1, j2 - j1)
        details.append((tag, src[i1:i2], asr[j1:j2]))
    print("src_chars=%d asr_chars=%d" % (len(src), len(asr)))
    print("diff_sites=%d diff_chars=%d charpos=%.1f%%" % (
        sites, diff_chars, 100.0 * diff_chars / max(1, len(src))))
    for tag, a, b in details:
        print("%s | src[%s] -> asr[%s]" % (tag, a, b))


if __name__ == "__main__":
    sys.exit(main())
