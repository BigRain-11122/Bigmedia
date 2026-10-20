# -*- coding: utf-8 -*-
"""AIGC implicit-label metadata gate (GB 45438-2025 / TC260-PG-20257A).

Embed and verify the seven-field AIGC JSON in an MP4/MOV file's
moov.udta.meta box. Field names and the ffmpeg one-liner follow the
in-repo research canon
(docs/research/R-20260927-bigstream-04-aigc-labeling-recsys-weekly-scan.md
section 10.1, source TC260-PG-20257A V1.0-202508 appendix E):

    {"Label","ContentProducer","ProduceID","ReservedCode1",
     "ContentPropagator","PropagateID","ReservedCode2"}

The video stream is copied, never re-encoded, so embedding cannot change
picture quality (frame count / duration / bitrate stay identical).

ASCII rule: source is pure ASCII; Chinese label text is supplied on the
command line by the caller, never hardcoded here.

Exit codes: 0 = pass; 1 = gate FAIL; 2 = bad args / ffmpeg or ffprobe error.

Usage:
    python src/aigc_metadata.py --verify FILE
    python src/aigc_metadata.py --in IN.mp4 --out OUT.mp4 \
        --producer "NAME" --produce-id "ID" [--label AIGC] \
        [--propagator NAME] [--propagate-id ID] [--reserved1 S] [--reserved2 S]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

FIELDS = (
    "Label",
    "ContentProducer",
    "ProduceID",
    "ReservedCode1",
    "ContentPropagator",
    "PropagateID",
    "ReservedCode2",
)

# ffprobe tags can arrive lowercased depending on the demuxer
_TAG_CANDIDATES = ("AIGC", "aigc")


def run(cmd):
    """Run a command, return (rc, stdout, stderr) as text."""
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    return proc.returncode, out, err


def probe(path):
    """ffprobe the file, return (format_tags, streams, duration)."""
    rc, out, err = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    if rc != 0:
        raise RuntimeError("ffprobe failed: %s" % err.strip())
    data = json.loads(out)
    fmt = data.get("format", {})
    tags = {k.lower(): v for k, v in (fmt.get("tags") or {}).items()}
    streams = data.get("streams", [])
    duration = fmt.get("duration")
    return tags, streams, duration


def video_facts(streams):
    """First video stream's identity facts (used to prove stream copy)."""
    for s in streams:
        if s.get("codec_type") == "video":
            return {
                "codec": s.get("codec_name"),
                "width": s.get("width"),
                "height": s.get("height"),
                "frames": s.get("nb_frames"),
                "duration": s.get("duration"),
                "bitrate": s.get("bit_rate"),
            }
    return {}


def build_payload(args):
    """Seven-field JSON string, in the standard's field order."""
    payload = {
        "Label": args.label,
        "ContentProducer": args.producer,
        "ProduceID": args.produce_id,
        "ReservedCode1": args.reserved1 or "",
        "ContentPropagator": args.propagator or "",
        "PropagateID": args.propagate_id or "",
        "ReservedCode2": args.reserved2 or "",
    }
    return payload


def parse_embedded(tags):
    """Return the parsed AIGC payload from format tags, or None."""
    for key in _TAG_CANDIDATES:
        raw = tags.get(key.lower())
        if not raw:
            continue
        try:
            return json.loads(raw)
        except ValueError:
            return {"_raw_unparseable": raw}
    return None


def verify(path, expect=None, quiet=False):
    """Check the embedded seven-field payload. Returns list of FAIL strings."""
    fails = []
    tags, streams, duration = probe(path)
    payload = parse_embedded(tags)
    if payload is None:
        fails.append("no AIGC tag in file metadata")
        payload = {}
    elif "_raw_unparseable" in payload:
        fails.append("AIGC tag is not valid JSON: %s" % payload["_raw_unparseable"])
        payload = {}
    else:
        missing = [f for f in FIELDS if f not in payload]
        if missing:
            fails.append("missing field(s): %s" % ", ".join(missing))
        empty_required = [
            f for f in ("Label", "ContentProducer", "ProduceID") if not payload.get(f)
        ]
        if empty_required:
            fails.append("empty required field(s): %s" % ", ".join(empty_required))
        for key, want in (expect or {}).items():
            if want is not None and payload.get(key) != want:
                fails.append("%s mismatch: got %r want %r" % (key, payload.get(key), want))

    if not quiet:
        print("file: %s" % path)
        print("duration: %s" % duration)
        print("video: %s" % json.dumps(video_facts(streams), sort_keys=True))
        print("payload: %s" % json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if fails:
        for f in fails:
            print("FAIL: %s" % f)
    elif not quiet:
        print("RESULT: PASS (seven-field AIGC metadata readable)")
    return fails


def embed(args):
    """Stream-copy the input to output with the AIGC metadata added."""
    src = Path(args.input)
    dst = Path(args.output)
    if not src.is_file():
        print("input not found: %s" % src)
        return 2
    if dst.exists() and not args.force:
        print("output exists (use --force to overwrite): %s" % dst)
        return 2

    payload = build_payload(args)
    missing = [f for f in ("Label", "ContentProducer", "ProduceID") if not payload[f]]
    if missing:
        print("refusing to embed with empty field(s): %s" % ", ".join(missing))
        return 2

    meta = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    cmd = [
        "ffmpeg",
        "-y" if args.force else "-n",
        "-v",
        "error",
        "-i",
        str(src),
        "-map",
        "0",
        "-c",
        "copy",
        "-metadata",
        "AIGC=%s" % meta,
        "-movflags",
        "use_metadata_tags",
        str(dst),
    ]
    rc, out, err = run(cmd)
    if rc != 0:
        print("ffmpeg failed rc=%d: %s" % (rc, (err or out).strip()[-2000:]))
        return 2

    before = probe(src)
    after = probe(dst)
    facts_before = video_facts(before[1])
    facts_after = video_facts(after[1])
    if facts_before != facts_after:
        print("FAIL: video stream changed by embedding")
        print("  before: %s" % json.dumps(facts_before, sort_keys=True))
        print("  after : %s" % json.dumps(facts_after, sort_keys=True))
        return 1

    print("embedded: %s -> %s (%d bytes)" % (src.name, dst.name, dst.stat().st_size))
    print("stream copy verified: %s" % json.dumps(facts_after, sort_keys=True))
    expect = {
        "Label": payload["Label"],
        "ContentProducer": payload["ContentProducer"],
        "ProduceID": payload["ProduceID"],
    }
    fails = verify(dst, expect=expect)
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIGC implicit-label metadata gate")
    ap.add_argument("--in", dest="input", help="input media file (embed mode)")
    ap.add_argument("--out", dest="output", help="output media file (embed mode)")
    ap.add_argument("--verify", metavar="FILE", help="verify mode: read back the tag")
    ap.add_argument("--label", default="AIGC", help="Label value (default AIGC)")
    ap.add_argument("--producer", help="ContentProducer (service provider name)")
    ap.add_argument("--produce-id", dest="produce_id", help="ProduceID (content number)")
    ap.add_argument("--propagator", help="ContentPropagator (publishing platform)")
    ap.add_argument("--propagate-id", dest="propagate_id", help="PropagateID")
    ap.add_argument("--reserved1", default="", help="ReservedCode1")
    ap.add_argument("--reserved2", default="", help="ReservedCode2")
    ap.add_argument("--force", action="store_true", help="overwrite output")
    ap.add_argument(
        "--expect-produce-id",
        dest="expect_produce_id",
        help="verify mode: require this ProduceID",
    )
    args = ap.parse_args(argv)

    if args.verify:
        expect = {}
        if args.expect_produce_id:
            expect["ProduceID"] = args.expect_produce_id
        fails = verify(args.verify, expect=expect)
        return 1 if fails else 0

    if not (args.input and args.output and args.producer and args.produce_id):
        ap.error("embed mode needs --in --out --producer --produce-id")
    return embed(args)


if __name__ == "__main__":
    sys.exit(main())