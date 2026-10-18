# -*- coding: utf-8 -*-
"""Universal UTF-8-safe capture widget (tech#216, R2356).

Why: PS 5.1 ``>`` redirection re-encodes a native tool's byte stream
through the console codepage and writes a UTF-16 BOM file (tech#198 pit
law; anchors R2331 and R2355 x2: evidence files came back as UTF-16
BOM binary that read_file rejects, killing the chain). The law already
lives in tools/run_suite.ps1's header for the suite lane and in
src/os/probe_capture.py for the three routine probes; this widget
generalizes byte-level capture to ANY ad-hoc CLI capture - the
permanent replacement for the ``>`` habit at the pit's birth place.

One command: run the child, capture raw bytes, decode (utf-8 strict ->
gb18030 -> utf-8/replace), write the output file as UTF-8 WITHOUT BOM,
print a one-line summary, exit with the child's real exit code. OUT is
overwritten by design (same semantics as ``>``, no read-modify-write).

Usage:
    python tools/cap_utf8.py OUT [--timeout N] -- COMMAND [ARGS ...]
Example:
    python tools/cap_utf8.py .c3-tmp/readout.txt -- python src/os/queue_status.py --item 216
"""

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_TIMEOUT_S = 300
USAGE = ("usage: python tools/cap_utf8.py OUT [--timeout N] -- "
         "COMMAND [ARGS ...]")


def child_env():
    """Children print UTF-8 on pipes regardless of console code page."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def decode_output(data):
    """bytes -> text: utf-8 strict, then gb18030 (console-codepage
    family), then utf-8/replace so a file is always writable."""
    if not data:
        return ""
    for enc in ("utf-8", "gb18030"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", "replace")


def run_child(argv, cwd, timeout_s=DEFAULT_TIMEOUT_S):
    """Run child; return (rc, text). Stderr merges with a marker line;
    a timeout returns rc 3 with a partial-output note (probe_capture
    convention)."""
    try:
        proc = subprocess.run(argv, cwd=str(cwd), env=child_env(),
                              capture_output=True, timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or b""
        if isinstance(partial, str):
            partial = partial.encode("utf-8", "replace")
        text = decode_output(partial).rstrip("\n")
        return 3, (text + "\n[timeout after %ds]" % timeout_s).rstrip("\n")
    text = decode_output(proc.stdout or b"").rstrip("\n")
    err = decode_output(proc.stderr or b"").strip()
    if err:
        text = text + "\n[stderr] " + err
    return proc.returncode, text


def write_utf8(path, text):
    """UTF-8 without BOM by design (PS 5.1 `>` trap root-fix)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = argv[1:]
    if len(args) < 3:
        print(USAGE)
        return 2
    out_path, rest = args[0], args[1:]
    timeout_s, cmd, i = DEFAULT_TIMEOUT_S, None, 0
    while i < len(rest):
        if rest[i] == "--timeout" and i + 1 < len(rest):
            try:
                timeout_s = int(rest[i + 1])
            except ValueError:
                print(USAGE)
                return 2
            if timeout_s <= 0:
                print("--timeout must be positive")
                return 2
            i += 2
        elif rest[i] == "--":
            cmd = rest[i + 1:]
            break
        else:
            print(USAGE)
            return 2
    if not cmd:
        print(USAGE)
        return 2
    rc, text = run_child(cmd, os.getcwd(), timeout_s)
    if text and not text.endswith("\n"):
        text += "\n"
    path = write_utf8(out_path, text)
    print("cap-utf8: rc=%d written=%s (%d bytes, utf-8 no-bom)"
          % (rc, path, len(text.encode("utf-8"))))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
