"""R1939 same-text verification: SRT cues vs beats spoken column (SC-004-01-v1)."""
import io
import sys

SRT = r"data/storylines/audio/sc004-01-v1-tmp/subs.srt"
BEATS = r"data/storylines/audio/SC-004-01-v1.beats.txt"


def load_srt(path):
    blocks = [b for b in io.open(path, encoding="utf-8").read().strip().split("\n\n") if b.strip()]
    cues = []
    for b in blocks:
        lines = b.splitlines()
        cues.append("".join(lines[2:]).strip())
    return cues


def load_beats(path):
    out = []
    for line in io.open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        out.append(line.split("|")[2].strip())
    return out


def main():
    cues = load_srt(SRT)
    beats = load_beats(BEATS)
    out = ["cues=%d beats=%d" % (len(cues), len(beats))]
    miss = 0
    if len(cues) != len(beats):
        miss += 1
        out.append("COUNT-MISMATCH")
    for i in range(min(len(cues), len(beats))):
        c = cues[i].replace(" ", "")
        b = beats[i].replace(" ", "")
        if c != b:
            miss += 1
            out.append("MISS cue%02d" % (i + 1))
            out.append("  srt : " + cues[i][:70])
            out.append("  beat: " + beats[i][:70])
    # hook/close structural checks (audio line discipline)
    beats_raw = [l.strip() for l in io.open(BEATS, encoding="utf-8") if l.strip()]
    hook = beats_raw[0]
    close = beats_raw[-1]
    out.append("hook-triple-decl: ai-gen=%s archive=%s inference=%s" % (
        "AI" in hook or "AI 参与生成" in hook, "真实事件" in hook and "档案" in hook, "合理推演" in hook))
    out.append("close-inference-decl: %s" % ("合理推演" in close))
    out.append("SAME-TEXT miss=%d" % miss)
    txt = "\n".join(out)
    io.open(sys.argv[1] if len(sys.argv) > 1 else "/dev/null", "w", encoding="utf-8").write(txt) if len(sys.argv) > 1 else None
    print(txt.encode("ascii", "backslashreplace").decode("ascii"))
    sys.exit(1 if miss else 0)


if __name__ == "__main__":
    main()
