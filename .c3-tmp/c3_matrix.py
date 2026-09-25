# -*- coding: utf-8 -*-
"""C3 edge-tts emotion dial experiment (self-improvement queue C3).

Repro: python .c3-tmp/c3_matrix.py   (edge-tts + ffmpeg on PATH; corpus =
.c3-tmp/corpus.txt UTF-8; voice = zh-CN-YunyangNeural = production default).
Axes measured (all local, zero cloud-API tokens):
  A0  PROFILES deltas manifest?  hook/punch/body on same text
      (duration = rate proxy, spectral centroid = pitch proxy)
  A1  rate sweep      -14% / 0 / +8%          (duration proxy)
  A2  pitch sweep     -12Hz / 0 / +12Hz       (centroid proxy)
  A3  volume sweep    -50% / 0 / +50%         (RMS via volumedetect)
  A4  cyber-light survival: centroid pre -> post light chain
      (validates "light keeps the emotive melody" claim by measurement)
  A5  within-sentence stepped pitch: head neutral + tail -8Hz, concat,
      halves' centroids + seam duration algebra
Outputs .c3-tmp/c3-results.txt. Negative results are recorded as-is.
"""
import re
import subprocess
from pathlib import Path

TMP = Path(__file__).resolve().parent
VOICE = "zh-CN-YunyangNeural"
LIGHT = ("highpass=f=110,lowpass=f=7800,vibrato=f=30:d=0.10,"
         "acrusher=bits=10:mode=log:aa=0.15:mix=0.50,alimiter=limit=0.95")


def sh(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("cmd failed: %s ... %s"
                           % (" ".join(cmd[:5]), r.stderr[-300:]))
    return r


def synth(name, text, flags):
    out = TMP / (name + ".mp3")
    r = sh(["edge-tts", "--voice", VOICE] + flags +
           ["--text", text, "--write-media", str(out)], check=False)
    if r.returncode != 0:
        return None
    return out


def dur(p):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", str(p)])
    return float(r.stdout.strip())


def rms(p):
    r = sh(["ffmpeg", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    x = re.search(r"max_volume:\s*(-?[\d.]+) dB", r.stderr)
    return (float(m.group(1)) if m else None,
            float(x.group(1)) if x else None)


def centroid(p):
    """Mean spectral centroid (Hz) over voiced frames via aspectralstats.
    Silence frames report ~1 Hz and are excluded (>=50 Hz = voiced proxy).
    Channel index in the metadata key varies; match any. None if n/a."""
    r = sh(["ffmpeg", "-i", str(p),
            "-af", "aspectralstats=measure=centroid,"
                   "ametadata=print:key=lavfi.aspectralstats.1.centroid:file=-",
            "-f", "null", "-"], check=False)
    if r.returncode != 0:
        return None
    vals = [float(v) for v in re.findall(
        r"lavfi\.aspectralstats\.\d+\.centroid=([\d.]+)", r.stdout)]
    voiced = [v for v in vals if v >= 50.0]
    if not voiced:
        return None
    return round(sum(voiced) / len(voiced), 1)


def main():
    lines = [l for l in (TMP / "corpus.txt").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    s1, s2, s2a, s2b = lines[0], lines[1], lines[2], lines[3]
    res = []

    def row(tag, val):
        res.append((tag, val))
        print("  %s | %s" % (tag, val))

    print("C3 matrix start (voice=%s)" % VOICE)

    # A0: production PROFILES deltas on same text (hook/punch/body)
    for tag, flags in [("hook", ["--rate=-8%", "--pitch=-3Hz"]),
                      ("punch", ["--rate=+6%", "--pitch=+3Hz"]),
                      ("body", [])]:
        p = synth("a0_" + tag, s1, flags)
        row("A0 profile=%s" % tag, "dur=%.3fs centroid=%s" % (dur(p), centroid(p)))

    # A1: rate sweep
    for tag, flags in [("rate_m14", ["--rate=-14%"]),
                       ("rate_0", []),
                       ("rate_p8", ["--rate=+8%"])]:
        p = synth("a1_" + tag, s1, flags)
        row("A1 %s" % tag, "dur=%.3fs" % dur(p))

    # A2: pitch sweep (centroid proxy)
    cps = {}
    for tag, flags in [("pitch_m12", ["--pitch=-12Hz"]),
                       ("pitch_0", []),
                       ("pitch_p12", ["--pitch=+12Hz"])]:
        p = synth("a2_" + tag, s1, flags)
        cps[tag] = centroid(p)
        row("A2 %s" % tag, "dur=%.3fs centroid=%s" % (dur(p), cps[tag]))

    # A3: volume sweep (RMS proxy)
    for tag, flags in [("vol_m50", ["--volume=-50%"]),
                       ("vol_0", []),
                       ("vol_p50", ["--volume=+50%"])]:
        p = synth("a3_" + tag, s1, flags)
        if p is None:
            row("A3 %s" % tag, "edge-tts REJECTED --volume (negative result)")
            continue
        m, x = rms(p)
        row("A3 %s" % tag, "mean=%sdB max=%sdB dur=%.3fs" % (m, x, dur(p)))

    # A4: cyber-light survival (does the pitch melody survive the texture?)
    for tag in ["pitch_m12", "pitch_p12"]:
        src = TMP / ("a2_%s.mp3" % tag)
        dst = TMP / ("a4_%s_light.mp3" % tag)
        sh(["ffmpeg", "-y", "-i", str(src), "-af", LIGHT,
            "-c:a", "libmp3lame", "-qscale:a", "4", str(dst)])
        post = centroid(dst)
        pre = cps.get(tag)
        delta = None if (pre is None or post is None) else round(post - pre, 1)
        row("A4 light %s" % tag, "centroid %s -> %s (delta=%s Hz)"
            % (pre, post, delta))

    # A5: within-sentence stepped pitch (declining tail)
    pa = synth("a5_partA", s2a, [])
    pb = synth("a5_partB", s2b, ["--pitch=-8Hz"])
    ca, cb = centroid(pa), centroid(pb)
    da, db = dur(pa), dur(pb)
    lst = TMP / "a5_concat.txt"
    lst.write_text("file '%s'\nfile '%s'\n"
                   % (pa.resolve().as_posix(), pb.resolve().as_posix()),
                   encoding="ascii")
    pc = TMP / "a5_stepped.mp3"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c:a", "libmp3lame", "-qscale:a", "4", str(pc)])
    dc = dur(pc)
    row("A5 stepped halves", "durA=%.3fs durB=%.3fs concat=%.3fs "
        "(sum=%.3f padding=%.3fs) centroidA=%s centroidB=%s"
        % (da, db, dc, da + db, dc - da - db, ca, cb))
    m, x = rms(pc)
    row("A5 stepped whole", "mean=%sdB max=%sdB" % (m, x))

    out = TMP / "c3-results.txt"
    out.write_text("\n".join("%s | %s" % r for r in res) + "\n",
                   encoding="utf-8")
    print("OK %d rows -> %s" % (len(res), out))


if __name__ == "__main__":
    main()
