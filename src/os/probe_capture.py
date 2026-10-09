# -*- coding: utf-8 -*-
"""One-shot runner for the three routine probes with UTF-8-safe output capture.

Why (state/queue/tech#25, R1831 incident): PowerShell 5.1 ``>`` redirection
writes UTF-16 BOM files, so probe output saved that way reads back as binary
garbage (four rework rounds to decode). This tool runs the three routine probes
(board_check / readiness / loop_health) as child processes, decodes their UTF-8
stdout, and -- unlike a shell redirect -- writes a single UTF-8 (no BOM) file.

Faces: compact by default (readiness --summary, loop_health --loop = the round
engine's routine consumption faces); --full switches every probe to its audit
face. Exit code = worst probe rc, so callers keep probe semantics.

Usage:
    python src/os/probe_capture.py                    # print compact faces
    python src/os/probe_capture.py --out FILE         # + UTF-8 file, stdout
                                                      #   trimmed to rc lines
    python src/os/probe_capture.py --full             # audit faces
    python src/os/probe_capture.py --echo             # with --out: also print
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_TIMEOUT_S = 120
USAGE = ("usage: python src/os/probe_capture.py "
         "[--out FILE] [--full] [--echo] [--timeout N]")


def build_probes(full):
    """Return [(name, argv)] for the three routine probes in run order."""
    py = sys.executable
    readiness = [py, str(REPO / "src" / "readiness.py")]
    loop_health = [py, str(REPO / "src" / "os" / "loop_health.py")]
    if not full:
        readiness.append("--summary")
        loop_health.append("--loop")
    return [
        ("board_check", [py, str(REPO / "src" / "board_check.py")]),
        ("readiness", readiness),
        ("loop_health", loop_health),
    ]


def child_env():
    """Child probes print UTF-8 on pipes regardless of console code page."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def run_probe(argv, env, cwd, timeout_s=DEFAULT_TIMEOUT_S):
    """Run one probe; return (rc, text). Bytes -> utf-8/replace, stderr merged."""
    try:
        proc = subprocess.run(argv, cwd=str(cwd), env=env,
                              capture_output=True, timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or b""
        if isinstance(partial, str):
            partial = partial.encode("utf-8", "replace")
        text = partial.decode("utf-8", "replace").rstrip("\n")
        return 3, (text + "\n[timeout after %ds]" % timeout_s).strip()
    text = (proc.stdout or b"").decode("utf-8", "replace").rstrip("\n")
    err = (proc.stderr or b"").decode("utf-8", "replace").strip()
    if err:
        text = text + "\n[stderr] " + err
    return proc.returncode, text


def overall_rc(results):
    """Worst probe rc wins; an empty result set is a clean zero."""
    return max([rc for _, rc, _ in results] + [0])


def render_report(results, mode, ts):
    lines = ["# probe-capture %s mode=%s" % (ts, mode)]
    for name, rc, text in results:
        lines.append("=== %s (rc=%d) ===" % (name, rc))
        if text:
            lines.append(text)
    return "\n".join(lines) + "\n"


def write_report(path, text):
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
    out_path, full, echo = None, False, False
    timeout_s = DEFAULT_TIMEOUT_S
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_path = args[i + 1]
            i += 2
        elif args[i] == "--full":
            full = True
            i += 1
        elif args[i] == "--echo":
            echo = True
            i += 1
        elif args[i] == "--timeout" and i + 1 < len(args):
            try:
                timeout_s = int(args[i + 1])
            except ValueError:
                print(USAGE)
                return 2
            if timeout_s <= 0:
                print("--timeout must be positive")
                return 2
            i += 2
        else:
            print(USAGE)
            return 2

    env = child_env()
    results = []
    for name, probe_argv in build_probes(full):
        rc, text = run_probe(probe_argv, env, REPO, timeout_s)
        results.append((name, rc, text))
    mode = "full" if full else "compact"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = render_report(results, mode, ts)

    if out_path is not None:
        path = write_report(out_path, report)
        print("probe-capture: mode=%s overall_rc=%d"
              % (mode, overall_rc(results)))
        for name, rc, _ in results:
            print("  %s: rc=%d" % (name, rc))
        print("written: %s (%d bytes, utf-8 no-bom)"
              % (path, len(report.encode("utf-8"))))
        if echo:
            print(report, end="")
    else:
        print(report, end="")
    return overall_rc(results)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
