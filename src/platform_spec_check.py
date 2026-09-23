# -*- coding: utf-8 -*-
"""Platform spec gate - duration/aspect machine check (production red line).

Production-chain S3 lists "duration measured" as a mass-production red
line, but until now it had NO tool - v5 (60.58s) and v10 (64.06s) both
slipped past the 60s shipinhao ceiling and were only caught by manual
honesty notes. This gate closes that: ffprobe the rendered file, check
duration + aspect against the platform table in docs/platform-playbook.md
- parsed live from the playbook so the spec has a single source of truth
and cannot drift into a side-table.

ASCII rule: source is pure ASCII; platform names/specs live in the
playbook data file the tool reads.

Exit codes: 0 = pass; 1 = spec FAIL; 2 = bad args / unparseable spec.

Usage:
    python src/platform_spec_check.py --video FILE --platform <name>
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLAYBOOK = REPO / "docs" / "platform-playbook.md"

_ASPECT_RE = re.compile(r"(\d+):(\d+)")
_DUR_S_RE = re.compile(r"(\d+)-(\d+)\s*s\b")
_DUR_MIN_RE = re.compile(r"(\d+)-(\d+)\s*min\b")

# how close w/h must be to the spec ratio to count as matching
_ASPECT_TOL = 0.02


def parse_playbook(text):
    """Parse the platform table rows into
    {platform: {"aspects": ["9:16", ...], "dur_s": (lo, hi) or None}}.
    Rows without a duration range keep dur_s=None (= duration unchecked).
    A row must carry an aspect in form "N:N" to be video-relevant."""
    specs = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("平台", "---", "平台 |"):
            continue
        name, spec_cell = cells[0], cells[2]
        aspects = _ASPECT_RE.findall(spec_cell)
        if not aspects:
            continue
        dur = None
        m = _DUR_S_RE.search(spec_cell)
        if m:
            dur = (int(m.group(1)), int(m.group(2)))
        else:
            m = _DUR_MIN_RE.search(spec_cell)
            if m:
                dur = (int(m.group(1)) * 60, int(m.group(2)) * 60)
        specs[name] = {
            "aspects": ["%s:%s" % (a, b) for a, b in aspects],
            "dur_s": dur,
        }
    return specs


def aspect_name(width, height):
    """Map concrete pixels to the nearest named aspect we track."""
    if not width or not height:
        return None
    ratio = float(width) / float(height)
    for name in ("9:16", "16:9", "3:4"):
        a, b = (int(x) for x in name.split(":"))
        if abs(ratio - a / float(b)) / (a / float(b)) <= _ASPECT_TOL:
            return name
    return None


def probe_video(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1", str(path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL ffprobe exit %d: %s" % (r.returncode, path))
        return None
    w = h = None
    dur = None
    for ln in r.stdout.splitlines():
        if "=" not in ln:
            continue
        key, val = ln.split("=", 1)
        if key == "width":
            w = int(val)
        elif key == "height":
            h = int(val)
        elif key == "duration":
            dur = float(val)
    if not (w and h and dur):
        print("FAIL incomplete probe data for %s" % path)
        return None
    return w, h, dur


def check(spec, width, height, duration):
    """Return findings: list of (level, code, detail), FAIL blocks."""
    findings = []
    got_aspect = aspect_name(width, height)
    if got_aspect not in spec["aspects"]:
        findings.append(("FAIL", "aspect",
                         "%dx%d (%s) not in platform aspects %s"
                         % (width, height, got_aspect, spec["aspects"])))
    else:
        findings.append(("PASS", "aspect", "%dx%d = %s"
                          % (width, height, got_aspect)))
    dur = spec["dur_s"]
    if dur is None:
        findings.append(("INFO", "duration",
                         "platform has no duration range in playbook - unchecked"))
    elif not (dur[0] <= duration <= dur[1]):
        findings.append(("FAIL", "duration",
                         "%.2fs outside %d-%ds platform window"
                         % (duration, dur[0], dur[1])))
    else:
        findings.append(("PASS", "duration",
                         "%.2fs within %d-%ds window (%.1fs headroom)"
                         % (duration, dur[0], dur[1], dur[1] - duration)))
    return findings


def main(argv):
    video = platform = None
    i = 1
    while i < len(argv):
        if argv[i] == "--video":
            i += 1
            video = argv[i]
        elif argv[i] == "--platform":
            i += 1
            platform = argv[i]
        i += 1
    if not (video and platform):
        print("usage: platform_spec_check.py --video FILE --platform NAME")
        return 2
    if not PLAYBOOK.exists():
        print("FAIL playbook not found: %s" % PLAYBOOK)
        return 2
    specs = parse_playbook(PLAYBOOK.read_text(encoding="utf-8"))
    if platform not in specs:
        print("FAIL unknown or non-video platform: %s (known: %s)"
              % (platform, ", ".join(sorted(specs))))
        return 2
    probed = probe_video(video)
    if not probed:
        return 2
    w, h, dur = probed
    findings = check(specs[platform], w, h, dur)
    fails = [f for f in findings if f[0] == "FAIL"]
    for lv, code, detail in findings:
        print("[%s] %s: %s" % (lv, code, detail))
    print("SUMMARY: %s -> %s" % (platform, "exit 1" if fails else "pass"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
