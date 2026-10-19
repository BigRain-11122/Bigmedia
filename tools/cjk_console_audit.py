# -*- coding: utf-8 -*-
"""cjk_console_audit.py -- tech#246 (R2389): repo-wide CJK console-output audit.

Two faces:
  1. STATIC  -- inventory every *.py CLI entry (has __main__ / def main) under
     src/ + tools/ whose source contains CJK; flag whether console hardening
     (sys.stdout.reconfigure(encoding="utf-8") or _harden_console_stdio) is
     present, and whether any *print()/logging* call carries a literal CJK
     string (multi-line call bodies are joined before testing).
  2. SMOKE   -- run a curated, READ-ONLY, zero-required-arg smoke list under
     the DEFAULT console environment (no PYTHONIOENCODING override) and judge
     the raw stdout bytes:
       utf-8 strict decode OK + CJK present  -> PASS  (utf-8 writer)
       utf-8 strict fails, gbk OK + CJK      -> FAIL  (codepage writer)
       UnicodeEncodeError in stderr          -> FAIL  (crash writer)
       no CJK bytes in output                -> ASCII (unaffected face)

Usage:
  python tools/cjk_console_audit.py [--report PATH] [--smoke-only] [--no-smoke]

Judgement stays with the loop (queue tech#246 criteria 1-3).
Report is UTF-8 (this tool hardens its own console first).
"""
import argparse
import io
import os
import re
import subprocess
import sys

CJK = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
HARDEN_MARK = ('reconfigure', '_harden_console_stdio')
OUT_CALL = re.compile(r'\b(print)\s*\(|\.(?:info|warning|error|debug|critical)\s*\(')

# curated smoke list: label, argv, timeout_s -- READ-ONLY tools only.
# mutating/expensive tools (close_commit, export_refresh, self_audit,
# daily_brief, call_expert, render/*, fire_consume, gpu_window_gate,
# e4_launcher_gen, collide_scan(arg-gated)) are static-face only.
SMOKE_LIST = [
    ("readiness.py --summary (hardened ctrl)", [sys.executable, 'src/readiness.py', '--summary'], 90),
    ("loop_health.py --loop (hardened ctrl)", [sys.executable, 'src/os/loop_health.py', '--loop'], 60),
    ("queue_status.py (hardened ctrl)",        [sys.executable, 'src/os/queue_status.py'], 60),
    ("origin_gap_check.py (ascii ctrl)",      [sys.executable, 'src/os/origin_gap_check.py'], 60),
    ("local_rate_report.py (subject)",         [sys.executable, 'src/os/local_rate_report.py'], 60),
    ("tokens_local_meter.py (subject)",        [sys.executable, 'src/os/tokens_local_meter.py'], 60),
    ("ollama_probe.py (subject)",              [sys.executable, 'src/os/ollama_probe.py'], 45),
    ("axis_anchor_check.py --help (subject)",  [sys.executable, 'tools/axis_anchor_check.py', '--help'], 30),
]


def _harden_console_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def _walk_py(roots):
    for root in roots:
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ('__pycache__',)]
            for f in sorted(files):
                if f.endswith('.py'):
                    yield os.path.join(dirpath, f)


def _literal_cjk_print_lines(text):
    """Return count of print()/logging calls whose (possibly multi-line) call
    body contains a literal CJK char. Lines are joined from the call opener
    until parens balance (cap 8 lines)."""
    hits = 0
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not OUT_CALL.search(line):
            continue
        depth = 0
        body = []
        for j in range(i, min(i + 8, len(lines))):
            body.append(lines[j])
            depth += lines[j].count('(') - lines[j].count(')')
            if depth <= 0 and j > i:
                break
            if depth <= 0 and '(' in lines[j]:
                break
        if CJK.search('\n'.join(body)):
            hits += 1
    return hits


def static_face():
    rows = []
    for path in _walk_py(['src', 'tools']):
        try:
            text = io.open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        if ('__main__' not in text) and ('def main' not in text):
            continue
        if not CJK.search(text):
            rows.append((path, 'ascii', 0, '-'))
            continue
        hardened = any(m in text for m in HARDEN_MARK)
        lit = _literal_cjk_print_lines(text)
        rows.append((path, 'hardened' if hardened else 'NO-HARDEN', lit,
                     'console-cjk' if lit else 'cjk-in-file-writes'))
    return rows


def smoke_face():
    results = []
    for label, argv, tmo in SMOKE_LIST:
        env = {k: v for k, v in os.environ.items()
               if k != 'PYTHONIOENCODING'}          # default console face
        try:
            p = subprocess.run(argv, capture_output=True, timeout=tmo, env=env)
        except subprocess.TimeoutExpired:
            results.append((label, 'TIMEOUT', ''))
            continue
        out, err = p.stdout, p.stderr
        blob = out + err
        try:
            s = blob.decode('utf-8')
            judge = 'PASS' if CJK.search(s) else 'ASCII'
            detail = ('utf-8 strict ok, cjk present' if judge == 'PASS'
                      else 'no cjk bytes')
        except UnicodeDecodeError:
            try:
                blob.decode('gbk')
                judge = 'FAIL'
                detail = 'codepage(gbk) bytes on default console'
            except UnicodeDecodeError:
                judge = 'FAIL'
                detail = 'mixed undecodable bytes'
        if p.returncode != 0 and b'UnicodeEncodeError' in blob:
            judge, detail = 'FAIL', 'UnicodeEncodeError crash'
        results.append((label, judge, detail))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='.c3-tmp/cjk_console_audit_report.txt')
    ap.add_argument('--smoke-only', action='store_true')
    ap.add_argument('--no-smoke', action='store_true')
    args = ap.parse_args()
    _harden_console_stdio()

    rep = io.open(args.report, 'w', encoding='utf-8', newline='\n')
    rep.write('# cjk console audit (tech#246) %s\n' % _now())
    if not args.smoke_only:
        rows = static_face()
        rep.write('\n== STATIC FACE: %d CLI entries with CJK in source ==\n' % len(rows))
        hard = sum(1 for r in rows if r[1] == 'hardened')
        for path, state, lit, face in rows:
            rep.write('%-46s %-10s literal-cjk-prints=%d %s\n' % (path, state, lit, face))
        rep.write('summary: hardened=%d NO-HARDEN=%d ascii=%d\n'
                  % (hard, sum(1 for r in rows if r[1] == 'NO-HARDEN'),
                     sum(1 for r in rows if r[1] == 'ascii')))
        print('static: %d entries, hardened=%d' % (len(rows), hard))
    if not args.no_smoke:
        rep.write('\n== SMOKE FACE (default console, raw-byte judged) ==\n')
        for label, judge, detail in smoke_face():
            rep.write('%-44s %-7s %s\n' % (label, judge, detail))
            print('smoke: %-44s %s' % (label, judge))
    rep.close()
    print('report: %s' % args.report)


def _now():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    main()
