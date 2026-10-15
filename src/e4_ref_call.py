#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E4 card-line shared shell (tech#180 leg-2 / tech#63 candidate B):
fly an E4 audience-reference verdict from ONE parameterized file
instead of a per-card launcher copy.

Why: the generator (tech#113, C-46) ended the HAND-copy era by baking
the prompt into a per-card e4_call_cpu.py at staging time -- every
card still ships one generated launcher copy plus its .out/.err
debris, and every same-round E4 leg pays a generate+dispatch pair.
R-20261010-07 candidate B named the end state: ONE shared shell in
src/, parameterized by the prompt file, zero per-card copies ("e4
shell zero-copy"). This is that shell.

Anti-drift by construction -- this file imports, it never re-states:
  * CANONICAL_QUESTIONS / build_prompt / UsageError come from
    src/os/e4_launcher_gen.py (single source of the E4 question
    contract; the double-append guard refuses a body that already
    carries the question block).
  * The auto-ledger + auto-stage machinery (tech#173/#174) is the
    generator's AUTO_LEDGER_BLOCK rendered with the E4 seat identity
    and EXECUTED here -- the block stays the single source; this
    shell is a third CONSUMER of it, not a third copy (the tech#124
    third-copy doctrine is satisfied by execution, not extraction:
    the generated launchers embed the block, this shell runs the
    very same code).

CPU lane laws (tech#169, O-20260913-2215): the CPU face is legal
24/7, the CEO 10% CPU margin survives as num_thread=4 (default), and
zero GPU touch is asserted by the flight itself (options num_gpu=0).
No GPU preflight: this is a same-round direct shell, not a
fire-gated staged launcher; the probe-gated path for cold /
starve-risk windows stays fire_consume.py --cpu-lane + a generated
launcher (mis-wiring guard: this file's name carries no "_cpu", so
fire_consume --cpu-lane refuses it loudly -- by design, fire_consume
cannot pass launcher args, so a parameterized shell is structurally
a direct-invocation face).

Liveness: /api/tags 2s probe -> rc 3 (never burn the 1500s hat on a
dead server; s1 doctrine R2257).

Evidence lands in the ITEM directory (the prompt file's dir --
tech#63 "evidence unified in the item dir"): e4-result.json (five-key
parity lane/material/model/ts/verdict, the R2261 audit shape) + the
shared auto-ledger (expert-calls row + expert-verdicts archive) +
auto-stage (git add of the raw result json).

rc contract (mirrors the CPU-variant generated launcher):
  0 = verdict landed in e4-result.json (incl. TIMEOUT/EMPTY verdicts)
  2 = usage error (missing/empty --prompt-file, body already carries
      the question block, missing/empty --questions-file, bad
      --timeout/--threads)
  3 = liveness or transport error, NO result file (re-dispatch later)

Usage:
  python src/e4_ref_call.py --prompt-file <e4-body.txt> [--label L]
      [--model qwen2.5:14b] [--timeout 1500] [--threads 4]
      [--questions-file QF]

--label defaults to the prompt file's parent directory name with a
trailing '-tmp' stripped (MC-20261016-REACT-v22-tmp ->
MC-20261016-REACT-v22), matching the card-line label style; a
root-level prompt file falls back to the file stem.
"""
from __future__ import unicode_literals

import argparse
import io
import json
import os
import sys
import time
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, 'os'))

import e4_launcher_gen as _gen  # noqa: E402  single source of the E4 contract

UsageError = _gen.UsageError  # one class, no fork

TAGS_URL = 'http://localhost:11434/api/tags'
GENERATE_URL = 'http://localhost:11434/api/generate'
LANE = 'cpu'
RESULT_NAME = 'e4-result.json'
LIVENESS_CAP_S = 2


def default_label(prompt_path):
    """Pure: item-dir-derived label ('x-tmp' -> 'x'; root file -> stem)."""
    parent = os.path.basename(
        os.path.dirname(os.path.abspath(prompt_path)))
    if parent.endswith('-tmp'):
        parent = parent[:-len('-tmp')]
    if not parent:
        parent = os.path.splitext(
            os.path.basename(os.path.abspath(prompt_path)))[0]
    return parent


def assemble_prompt(body, questions):
    """Single-source passthrough to the generator's build_prompt
    (double-append guard included)."""
    return _gen.build_prompt(body, questions)


def render_ledger_block():
    """Pure: the shared AUTO_LEDGER_BLOCK with the E4 seat identity --
    the exact substitution the generator applies to the E4 card
    faces, so shell flights and generated-launcher flights log
    byte-identically (same block, same behavior)."""
    block = _gen.AUTO_LEDGER_BLOCK
    block = block.replace('__EXPERT_ID__', repr(_gen.E4_EXPERT_ID))
    block = block.replace('__ROLE_DEPT_EXPR__', repr(_gen.E4_ROLE_DEPT))
    return block


def run_ledger_block(result, here, material, model):
    """EXECUTE the shared block (single source, not a copy).

    Binds the names the block expects (HERE / MATERIAL / MODEL /
    result / io / os / time) and runs it verbatim: ledger row,
    verdict archive and auto-stage behave byte-identically to the
    generated launchers because it is literally the same code. Best
    effort by the tech#173 contract -- a write failure WARNs, it
    never changes the verdict or the rc."""
    namespace = {
        'HERE': here, 'MATERIAL': material, 'MODEL': model,
        'result': result, 'io': io, 'os': os, 'time': time,
        '__name__': 'e4_ref_call_auto_ledger',
    }
    exec(compile(render_ledger_block(), '<auto-ledger-block>', 'exec'),
         namespace)


def _liveness_ok(cap_s=LIVENESS_CAP_S):
    """True when ollama answers /api/tags inside the cap. Never
    raises -- an unreachable server reads as not-ok (rc 3)."""
    try:
        with urllib.request.urlopen(TAGS_URL, timeout=cap_s) as resp:
            resp.read()
        return True
    except Exception:
        return False


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    ap = argparse.ArgumentParser(
        description='E4 audience-reference shared shell (tech#180 '
                    'leg-2): CPU-lane direct flight from a prompt '
                    'body file, zero per-card launcher copies.')
    ap.add_argument('--prompt-file', required=True,
                    help='hand-written E4 body file (narrative '
                         'WITHOUT the question block; canonical '
                         'questions are appended by the shared '
                         'contract)')
    ap.add_argument('--label',
                    help='material label for result json + ledger '
                         '(default: prompt file parent dir name '
                         'with trailing -tmp stripped)')
    ap.add_argument('--model', default='qwen2.5:14b')
    ap.add_argument('--timeout', type=int, default=1500)
    ap.add_argument('--threads', type=int, default=4,
                    help='CPU threads (CEO 10%% margin law)')
    ap.add_argument('--questions-file',
                    help='override the canonical question block')
    args = ap.parse_args(argv)

    try:
        if args.timeout <= 0 or args.threads <= 0:
            raise UsageError('--timeout/--threads must be positive')
        if not os.path.isfile(args.prompt_file):
            raise UsageError('prompt body file not found: '
                             + args.prompt_file)
        body = io.open(args.prompt_file, encoding='utf-8-sig').read()
        if not body.strip():
            raise UsageError('prompt body file is empty: '
                             + args.prompt_file)
        if args.questions_file:
            if not os.path.isfile(args.questions_file):
                raise UsageError('questions file not found: '
                                 + args.questions_file)
            questions = io.open(args.questions_file,
                                encoding='utf-8-sig').read()
            if not questions.strip():
                raise UsageError('questions file is empty: '
                                 + args.questions_file)
        else:
            questions = _gen.CANONICAL_QUESTIONS
        prompt = assemble_prompt(body, questions)
    except UsageError as exc:
        print('USAGE-ERROR:', exc)
        return 2

    label = (args.label or '').strip() or default_label(args.prompt_file)
    here = os.path.dirname(os.path.abspath(args.prompt_file))

    if not _liveness_ok():
        print('LIVENESS-FAIL ollama /api/tags unreachable (%ds cap)'
              % LIVENESS_CAP_S, flush=True)
        return 3

    result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'),
              'model': args.model, 'material': label, 'lane': LANE}
    payload = json.dumps({'model': args.model, 'prompt': prompt,
                          'stream': False,
                          'options': {'num_gpu': 0,
                                      'num_thread': args.threads}}
                        ).encode('utf-8')
    request = urllib.request.Request(
        GENERATE_URL, data=payload,
        headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request,
                                    timeout=args.timeout) as resp:
            body_json = json.loads(resp.read().decode('utf-8',
                                                      'replace'))
        result['verdict'] = ((body_json.get('response') or '').strip()
                             or 'EMPTY-RESPONSE')
    except Exception as exc:
        text = '%s: %s' % (type(exc).__name__, exc)
        if 'timed out' in text.lower() or 'timeout' in text.lower():
            result['verdict'] = 'TIMEOUT-%ds' % args.timeout
        else:
            print('TRANSPORT-ERROR %s' % text, flush=True)
            return 3
    io.open(os.path.join(here, RESULT_NAME), 'w',
            encoding='utf-8').write(
        json.dumps(result, ensure_ascii=False, indent=2))
    run_ledger_block(result, here, label, args.model)
    print('DONE' if not result['verdict'].startswith('TIMEOUT')
          else 'TIMEOUT')
    return 0


if __name__ == '__main__':
    sys.exit(main())
