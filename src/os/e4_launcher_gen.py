#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E4 card-line launcher generator (tech#113): turn a hand-written
prompt body into a turnkey e4_call.py in ONE command.

tech#172 family unification: the --expert face (--expert <seat-id>
--material <repo-relative path>) renders the registry-seat launcher
(the R2257 hand-written s1_call_cpu.py lineage) from this same file:
seat model + prompt file + role/dept are read from
data/experts/registry.json AT FLIGHT TIME (never hardcoded, s1_call
doctrine), prompt assembly = call_expert.build_prompt parity
(===== 材料 ===== block, material verbatim), CPU-lane only (the
adopted tech#169 dispatch design; the GPU S1 sibling s1_call.py stays
hand-written per R2257). The landed F-180 s1_call_cpu.py stays
untouched (tech#81 self-containment: in-flight artifacts are not
retrofitted). The auto-ledger machinery (tech#173) is ONE block
shared by all three rendered faces, parametrized on seat identity --
the generator family exists to end hand-copy drift, so its own shared
blocks must not fork per face (E4 GPU / E4 CPU / registry seat).

Why: ~140 hand-copied e4_call.py launchers sit across storylines tmp
dirs (sc001-* audio era + every MC-* card since); the recent card line
alone is v16 (R1536 prototype) -> v17 (R1938) -> v18 (R2001), one
hand-assembly per card. Every copy re-writes the identical machinery
(ollama direct call + UTF-8 stdin pipe + ANSI strip + braille strip +
e4-result.json) and hand-pastes the three questions -- and the copies
have already drifted: v18 says "直说不绕弯/空话套话/指出原文" while
the v13/v17 lineage says "直说不委婉/空洞套话/指出原句" (contract
drift inside hand copies = the evidence this generator exists to end).

Division of labor (tech#101 mirror): the BODY is the hand-crafted
judgment face (role + card lines + background narrative) and stays
hand-written; everything that should be constant -- machinery, the
canonical question block, contract details (R189 braille-strip
lesson, dynamic timeout label, DONE/TIMEOUT semantics) -- is owned by
this generator. The body must NOT already contain the question block
(double-append guard refuses it loudly).

The generated launcher is a staged launcher per the tech#112
fire_consume contract: fire_consume.py dispatches it verbatim the
moment the fire card says fire. Output file is UTF-8 no BOM.

rc contract (consumers gate on rc):
  0 = launcher written
  2 = usage error (missing/empty body file, body already carries the
     question block, missing/empty --label, bad --timeout, --out is an
     existing directory, unreadable --questions-file; tech#172 expert
     face: unknown --expert id, registry seat without prompt_file,
     missing --material file, --expert mixed with --body/--label/
     --questions-file, one of --expert/--material without the other)

The GENERATED launcher's own exit codes (tech#122/123 preflight port):
  0 = E4 verdict written to e4-result.json (including TIMEOUT verdicts)
  4 = window-flip defer (util >= 60% at preflight; R1986 verdict-void law)
  7 = slow-window bail (seat rate probe over 240s cap / 150s slow line)
rc 4/7 write NO e4-result.json -- a preflight bail is not a verdict;
evidence prints go to fire_consume's redirected .out/.err (tech#112).
The 7b wedge probe (tech#120) is deliberately NOT in this face: the
seat rate probe on the REAL seat model is its strict superset (R2025
flight-3: the 7b wedge probe passed while the 14b seat burned --
probe model != seat model is the documented blind spot).
"""
from __future__ import unicode_literals

import argparse
import io
import json
import os
import sys

# Canonical card-form question block (v13/v17 lineage; wording drift in
# the v18 hand copy -- 绕弯/空话/原文 -- is normalized back here).
CANONICAL_QUESTIONS = (
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

QUESTION_MARKER = u'请回答三个问题'

# tech#173 auto-ledger block: every landed verdict self-logs its
# expert-calls row + full-verdict archive at landing time, aligning
# with call_expert.py's audit behavior (before this, CPU-lane flights
# landed with a zero-row ledger and the read-back round backfilled by
# hand = daily drift face, R2258 anchor). Best effort by the
# call_expert contract: a ledger write failure WARNs, it never changes
# the verdict or the rc. Shared verbatim by ALL THREE rendered faces
# (E4 GPU / E4 CPU / registry seat, tech#172) -- seat identity is
# injected via __EXPERT_ID__ (repr'd literal) and __ROLE_DEPT_EXPR__
# (repr'd literal for the E4 faces; the registry-seat face passes the
# flight-time variable name `role_dept` so the dept text stays
# registry-owned). The block must never fork per face -- a per-face
# fork is the drift this generator family exists to end, one level up.
AUTO_LEDGER_BLOCK = r'''
# tech#173 auto-ledger: verdict self-logs its expert-calls row +
# archive (best effort; a write failure WARNs, verdict/rc untouched).
# tech#174 auto-stage: the raw result json self-stages into the repo
# index on landing (best effort, same WARN contract).
EXPERT_ID = __EXPERT_ID__
ROLE_DEPT = __ROLE_DEPT_EXPR__

def _repo_root():
    d = HERE
    while d and d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, '.git')):
            return d
        d = os.path.dirname(d)
    return None

def _auto_ledger(verdict, material, model):
    root = _repo_root()
    if root is None:
        print('WARN auto-ledger skipped (no repo root above %s)' % HERE,
              flush=True)
        return
    try:
        stamp = time.strftime('%Y-%m-%d %H:%M')
        vname = time.strftime('%Y%m%d-%H%M%S') + '-' + EXPERT_ID + '.md'
        vdir = os.path.join(root, 'docs', 'reviews', 'expert-verdicts')
        if not os.path.isdir(vdir):
            os.makedirs(vdir)
        io.open(os.path.join(vdir, vname), 'w', encoding='utf-8').write(
            '# %s - %s结论全文\n\n> 时间=%s · 模型=%s · 材料=%s\n'
            '> 机制=generated launcher auto-ledger（tech#173·对齐 '
            'call_expert.py O-20260924-1033·本件为结论存档·台账行='
            'expert-calls.md）\n\n%s\n'
            % (EXPERT_ID, ROLE_DEPT, stamp, model, material,
               (verdict or '').strip() or '-'))
        first_line = ((verdict or '').strip() or '-').splitlines()[0]
        note = '全文=expert-verdicts/%s ｜ %s' % (vname, first_line)
        note = note.replace('|', '/').replace('\n', ' ')[:160]
        row = '| %s | %s | %s | %s | 0 | %s |\n' % (
            stamp, EXPERT_ID, ROLE_DEPT, material, note)
        with io.open(os.path.join(root, 'docs', 'reviews',
                                  'expert-calls.md'), 'a',
                     encoding='utf-8') as fh:
            fh.write(row)
        print('LEDGER-ROW %s (tech#173 auto-ledger)' % EXPERT_ID,
              flush=True)
    except OSError as exc:
        print('WARN auto-ledger failed: %s (verdict kept)' % exc,
              flush=True)

def _auto_stage_result():
    # tech#174 auto-stage: the raw verdict json self-stages the
    # moment it lands. R2261 found the CPU-lane legs' raw
    # e4-result.json sitting untracked across 9 rounds while every
    # derived face (verdict archive + ledger row) landed same-window.
    # Symmetric with the archive above; best-effort -- an index
    # contention (parallel window holds index.lock) WARNs, verdict
    # and rc untouched (tech#173 contract).
    root = _repo_root()
    if root is None:
        return
    raw = os.path.join(HERE, 'e4-result.json')
    if not os.path.isfile(raw):
        return
    try:
        import subprocess
        proc = subprocess.run(
            ['git', 'add', '--', raw], cwd=root, timeout=30,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if proc.returncode == 0:
            print('STAGED-RESULT %s (tech#174 auto-stage)'
                  % os.path.relpath(raw, root), flush=True)
        else:
            print('WARN auto-stage failed rc=%d: %s (verdict kept)'
                  % (proc.returncode,
                     proc.stdout.decode('utf-8', 'replace').strip()),
                  flush=True)
    except Exception as exc:
        print('WARN auto-stage failed: %s (verdict kept)' % exc,
              flush=True)

_auto_ledger(result['verdict'], MATERIAL, MODEL)
_auto_stage_result()
'''

# E4 seat identity for the two card faces (the registry-seat face
# gets its identity from the CLI --expert id, resolved to registry
# role/dept AT FLIGHT TIME). These two constants are what keeps the
# rendered E4 output byte-identical to the pre-tech#172 literals.
E4_EXPERT_ID = 'E4-audience'
E4_ROLE_DEPT = u'E4 直觉观众参考仪（评审参考席（非部门编制））'

# Machinery template = verbatim v17/v18 lineage (R1536/R1938/R2001).
# Raw string keeps the strip-regex literals byte-identical.
TEMPLATE = r'''# -*- coding: utf-8 -*-
# E4 audience reference call - __LABEL__
# GENERATED by src/os/e4_launcher_gen.py (tech#113) -- do not hand-edit;
# regenerate from the body file instead. Machinery = v17/v18 lineage
# (R1536/R1938/R2001): UTF-8 stdin pipe + ANSI strip + braille strip
# (R189 U+2800 lesson) + e4-result.json next to this file.
# Pre-flight three-piece (tech#122/123 port, R2025 flight-3 burn):
# util-flip rc 4 / idle-resident relief / seat rate probe rc 7. The
# 7b wedge probe is deliberately absent -- the seat rate probe on the
# REAL seat model is its strict superset (R2025: 7b passed while the
# 14b seat burned; probe model != seat model).
# Staged launcher per tech#112: fire_consume.py dispatches THIS file
# the moment the fire card says fire.
# rc: 0 = verdict in e4-result.json | 4 = window-flip defer (NO result
# file) | 7 = slow-window bail (NO result file; re-dispatch next one).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = __MODEL__
TIMEOUT = __TIMEOUT__
MATERIAL = __LABEL_REPR__
prompt = __PROMPT_REPR__

RC_WINDOW_FLIP = 4
RC_SLOW_WINDOW = 7
UTIL_FLIP_PCT = 60          # preflight flip line (card gate is 80)
SEAT_PROBE_CAP_S = 240      # hard cap for the tiny seat generation
SEAT_PROBE_SLOW_S = 150     # elapsed above this = CPU-offload face
SEAT_PROBE_PROMPT = "Reply with exactly two chars: OK"


def _run(cmd, timeout, input_bytes=None):
    return subprocess.run(cmd, input=input_bytes, capture_output=True,
                          timeout=timeout)


def _gpu_headroom():
    """(util_pct, free_mb) or None - probe face, never raises."""
    try:
        p = _run(["nvidia-smi",
                  "--query-gpu=utilization.gpu,memory.free",
                  "--format=csv,noheader,nounits"], 15)
        first = p.stdout.decode("utf-8", "replace").strip().splitlines()[0]
        util_s, free_s = first.split(",")[:2]
        return int(util_s.strip()), int(free_s.strip())
    except Exception:
        return None


def preflight():
    """Relief + seat rate probe. Returns (ok, rc, evidence lines)."""
    ev = []
    h = _gpu_headroom()
    if h is None:
        ev.append("PREFLIGHT nvidia-smi unreadable - proceeding unguarded")
        return True, 0, ev
    util, free = h
    ev.append("PREFLIGHT util=%d%% free=%dMB" % (util, free))
    if util >= UTIL_FLIP_PCT:
        ev.append("DEFER window flipped after card (util %d%% >= %d%%)"
                 % (util, UTIL_FLIP_PCT))
        return False, RC_WINDOW_FLIP, ev
    # relief: stop idle ollama residents (safe - util just read < 60;
    # keep-warm self-heals, R2011 precedent: zero service debt)
    try:
        ps = _run(["ollama", "ps"], 15)
        names = [ln.split()[0] for ln in
                 ps.stdout.decode("utf-8", "replace").strip().splitlines()
                 if ln.strip() and not ln.lstrip().lower().startswith("name")]
        for name in names:
            _run(["ollama", "stop", name], 30)
            ev.append("RELIEF stopped idle resident %s" % name)
    except Exception as exc:
        ev.append("RELIEF skip (ollama ps/stop unavailable: %s)" % exc)
    h2 = _gpu_headroom()
    if h2:
        ev.append("RELIEF free now %dMB" % h2[1])
    # seat rate probe: tiny generation on the REAL seat model
    t0 = time.time()
    try:
        p = _run(["ollama", "run", MODEL], SEAT_PROBE_CAP_S,
                 input_bytes=SEAT_PROBE_PROMPT.encode("utf-8"))
    except subprocess.TimeoutExpired:
        ev.append("RATE-FAIL seat probe timed out (%ds cap, model %s) - "
                  "slow window; re-dispatch next fire window"
                  % (SEAT_PROBE_CAP_S, MODEL))
        return False, RC_SLOW_WINDOW, ev
    elapsed = time.time() - t0
    if p.returncode != 0:
        ev.append("RATE-FAIL seat probe exit %d (model %s) - server face"
                 % (p.returncode, MODEL))
        return False, RC_SLOW_WINDOW, ev
    if elapsed > SEAT_PROBE_SLOW_S:
        ev.append("RATE-FAIL seat probe %ds > %ds (model %s) - CPU-offload"
                 " face; do not burn %ds on a slow window"
                  % (int(elapsed), SEAT_PROBE_SLOW_S, MODEL, TIMEOUT))
        return False, RC_SLOW_WINDOW, ev
    ev.append("RATE-OK seat probe %ds (model %s, %ds cap) - GO"
              % (int(elapsed), MODEL, SEAT_PROBE_CAP_S))
    return True, 0, ev


_ok, _rc, _ev = preflight()
for _line in _ev:
    print(_line, flush=True)
if not _ok:
    print("PREFLIGHT-BAIL rc=%d (no e4-result.json written; "
          "re-dispatch next fire window)" % _rc, flush=True)
    raise SystemExit(_rc)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': MODEL, 'material': MATERIAL}
try:
    p = subprocess.run(['ollama', 'run', MODEL], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=TIMEOUT)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-%ds' % TIMEOUT
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding="utf-8").write(
    json.dumps(result, ensure_ascii=False, indent=2))
__AUTO_LEDGER_BLOCK__
print('DONE' if not result['verdict'].startswith('TIMEOUT') else 'TIMEOUT')
'''


# tech#169 CPU-lane variant template (wire v3 = tech#186): the CPU
# face is legal 24/7 (O-20260913-2215 CEO standing order -- the
# workday zero-dispatch rule's CPU portion was explicitly repealed).
# tech#186 reroute: the flight goes to the EXTERNAL brain lane
# (:8090 Qwen3.6-35B-A3B, OpenAI wire, BRAIN_URL/BRAIN_MODEL env at
# FLIGHT TIME, thinking off via chat_template_kwargs) instead of the
# local ollama API -- the dormant pathological qwen3.8:27b is no
# longer referenced by default. The old options pair
# (num_gpu/num_thread) is MOOT on this wire: threads/GPU pinning
# belong to the resident server, not the client payload. No GPU
# preflight lives here: the fire_consume --cpu-lane gate stays this
# launcher's preflight (its semantics re-cut = tech#186 leg 4).
CPU_TEMPLATE = r'''# -*- coding: utf-8 -*-
# E4 audience reference call (CPU LANE) - __LABEL__
# GENERATED by src/os/e4_launcher_gen.py --cpu-lane (tech#169, wire
# v3 = tech#186) -- do not hand-edit; regenerate from the body file
# instead. CPU lane face: O-20260913-2215 CPU face 24/7. Wire =
# external brain lane (BRAIN_URL env, OpenAI chat wire,
# enable_thinking:false -- canon qwen38-rollout-20261015.md v3);
# num_gpu/num_thread are MOOT (server-owned, tech#186). No GPU
# preflight: the fire_consume --cpu-lane gate is this launcher's
# preflight. Flight = POST non-stream (clean JSON verdict; no
# ANSI/braille strip needed on the API face).
# Staged launcher per tech#112: fire_consume.py --cpu-lane dispatches
# THIS file when the CPU-lane gate says fire.
# rc: 0 = verdict in e4-result.json (incl. TIMEOUT/EMPTY verdicts) |
# 3 = transport error, NO result file (re-dispatch next window).
import io, json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = __MODEL__
TIMEOUT = __TIMEOUT__
LANE = 'cpu'
GENERATE_URL = os.environ.get(
    'BRAIN_URL', 'http://127.0.0.1:8090/v1/chat/completions')
MATERIAL = __LABEL_REPR__
prompt = __PROMPT_REPR__

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': MODEL,
          'material': MATERIAL, 'lane': LANE}
payload = json.dumps({'model': MODEL, 'stream': False,
                      'messages': [{'role': 'user', 'content': prompt}],
                      'chat_template_kwargs': {'enable_thinking': False}}
                     ).encode('utf-8')
request = urllib.request.Request(GENERATE_URL, data=payload,
                                 headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(request, timeout=TIMEOUT) as resp:
        body = json.loads(resp.read().decode('utf-8', 'replace'))
    _choices = body.get('choices') or []
    _content = ''
    if _choices:
        _content = ((_choices[0].get('message') or {}).get('content')
                    or '')
    result['verdict'] = _content.strip() or 'EMPTY-RESPONSE'
except Exception as exc:
    text = '%s: %s' % (type(exc).__name__, exc)
    if 'timed out' in text.lower() or 'timeout' in text.lower():
        result['verdict'] = 'TIMEOUT-%ds' % TIMEOUT
    else:
        print('TRANSPORT-ERROR %s' % text, flush=True)
        raise SystemExit(3)
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
__AUTO_LEDGER_BLOCK__
print('DONE' if not result['verdict'].startswith('TIMEOUT') else 'TIMEOUT')
'''


# tech#172 registry-seat template (wire v3 = tech#186): the --expert
# face renders the R2257 hand-written s1_call_cpu.py lineage as a
# generated artifact. Differences vs the E4 card faces are exactly
# the two the family charter names -- the BODY (prompt comes from the
# registry prompt file, not a hand body) and the MATERIAL position
# (verbatim material under the 材料块) -- everything else is family
# law: CPU lane (O-20260913-2215 24/7 face; the old num_gpu/
# num_thread options pair is MOOT on the tech#186 wire -- threads
# belong to the external resident server), liveness <brain-base>/
# health 2s probe (rc 3 -- never burn the cap on a corpse), transport
# error rc 3, TIMEOUT verdict rc 0, tech#173 auto-ledger. Seat model
# + prompt file + role/dept are read from data/experts/registry.json
# AT FLIGHT TIME (never hardcoded, s1_call doctrine R2257); the
# fallback default when the registry carries no model is env
# BRAIN_MODEL (qwen3.6-35b) -- the registry top-level default swap
# is tech#186 leg 4 (registry 12-seat defaults). The repo root is
# walked from HERE (.git probe), so the launcher is
# position-independent (better than the hand-written parents[4] pin).
# Registry-seat face is CPU-LANE ONLY by adopted design (tech#169):
# the GPU S1 sibling s1_call.py stays hand-written per R2257.
EXPERT_TEMPLATE = r'''# -*- coding: utf-8 -*-
# __EXPERT__ seat call (CPU LANE) - __MATERIAL__
# GENERATED by src/os/e4_launcher_gen.py --expert (tech#172 registry-
# seat face, wire v3 = tech#186) -- do not hand-edit; regenerate
# instead. Family law: seat model + prompt file + role/dept read from
# data/experts/registry.json AT FLIGHT TIME (never hardcoded); prompt
# assembly = call_expert.build_prompt parity (材料块, material
# verbatim). CPU lane face: O-20260913-2215 CPU face 24/7. Wire =
# external brain lane (BRAIN_URL env, OpenAI chat wire,
# enable_thinking:false -- canon qwen38-rollout-20261015.md v3);
# num_gpu/num_thread are MOOT (server-owned, tech#186). Liveness =
# <brain-base>/health 2s probe (dead server -> rc 3, never burn the
# cap on a corpse). No GPU preflight: the fire_consume.py --cpu-lane
# gate is this launcher's preflight.
# tech#173 auto-ledger: the verdict self-logs its expert-calls row +
# archive at landing time.
# rc: 0 = result json written (incl TIMEOUT/EMPTY verdicts) | 3 =
# liveness/transport/input error, NO result file (re-dispatch next
# window).
import io, json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERT_ID = __EXPERT_ID__
MATERIAL_REL = __MATERIAL_REPR__
RESULT_NAME = __RESULT_REPR__
TIMEOUT = __TIMEOUT__
LANE = 'cpu'
GENERATE_URL = os.environ.get(
    'BRAIN_URL', 'http://127.0.0.1:8090/v1/chat/completions')
HEALTH_URL = (GENERATE_URL.split('/v1/')[0].rstrip('/') + '/health')


def _repo_root():
    d = HERE
    while d and d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, '.git')):
            return d
        d = os.path.dirname(d)
    return None


ROOT = _repo_root()
if ROOT is None:
    print('FAIL no repo root above %s' % HERE, flush=True)
    raise SystemExit(3)

# ---------- liveness (2s cap; dead server never burns the window) ----------
try:
    urllib.request.urlopen(HEALTH_URL, timeout=2).read()
except Exception as exc:
    print('LIVENESS-FAIL %s' % exc, flush=True)
    raise SystemExit(3)

# ---------- seat + prompt from registry (never hardcoded) ----------
reg = json.loads(io.open(os.path.join(ROOT, 'data', 'experts',
                                      'registry.json'),
                         encoding='utf-8-sig').read())
seat = str(reg.get('model', '')) or os.environ.get(
    'BRAIN_MODEL', 'qwen3.6-35b')
prompt_file = None
role_dept = EXPERT_ID
entries = reg.get('experts') or reg.get('roster') or []
for e in entries:
    if str(e.get('id', '')) == EXPERT_ID:
        if e.get('model'):
            seat = str(e['model'])
        prompt_file = str(e.get('prompt_file') or '') or None
        role_dept = '%s（%s）' % (e.get('role', EXPERT_ID),
                                  e.get('dept', ''))
        break
if not prompt_file:
    print('FAIL registry seat %s has no prompt_file' % EXPERT_ID,
          flush=True)
    raise SystemExit(3)
prompt_path = os.path.join(ROOT, prompt_file)
material_path = os.path.join(ROOT, MATERIAL_REL)
if not (os.path.isfile(prompt_path) and os.path.isfile(material_path)):
    print('FAIL input missing: prompt=%s material=%s'
          % (prompt_path, material_path), flush=True)
    raise SystemExit(3)

prompt_text = io.open(prompt_path, encoding='utf-8-sig').read()
material_text = io.open(material_path, encoding='utf-8-sig').read()
# call_expert.build_prompt parity: prompt + 材料块, material verbatim
prompt = (prompt_text.rstrip() + '\n\n===== 材料 =====\n' +
          material_text.strip() + '\n')

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': seat,
          'material': MATERIAL_REL, 'lane': LANE, 'expert': EXPERT_ID}
payload = json.dumps({'model': seat, 'stream': False,
                      'messages': [{'role': 'user', 'content': prompt}],
                      'chat_template_kwargs': {'enable_thinking': False}}
                     ).encode('utf-8')
request = urllib.request.Request(GENERATE_URL, data=payload,
                                 headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(request, timeout=TIMEOUT) as resp:
        body = json.loads(resp.read().decode('utf-8', 'replace'))
    _choices = body.get('choices') or []
    _content = ''
    if _choices:
        _content = ((_choices[0].get('message') or {}).get('content')
                    or '')
    result['verdict'] = _content.strip() or 'EMPTY-RESPONSE'
except Exception as exc:
    text = '%s: %s' % (type(exc).__name__, exc)
    if 'timed out' in text.lower() or 'timeout' in text.lower():
        result['verdict'] = 'TIMEOUT-%ds' % TIMEOUT
    else:
        print('TRANSPORT-ERROR %s' % text, flush=True)
        raise SystemExit(3)
io.open(os.path.join(HERE, RESULT_NAME), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
MATERIAL = MATERIAL_REL
MODEL = seat
__AUTO_LEDGER_BLOCK__
print('DONE' if not result['verdict'].startswith('TIMEOUT') else 'TIMEOUT')
'''


class UsageError(Exception):
    """Loud usage error before any file is written (rc 2)."""


def build_prompt(body, questions):
    """Pure: body + canonical question block, with double-append guard.

    >>> build_prompt('narrative.', 'Q')[:11]
    'narrative\\nQ'
    """
    if QUESTION_MARKER in body:
        raise UsageError(
            'body already contains the question block (marker '
            + repr(QUESTION_MARKER) + ') -- pass the narrative only')
    return body.rstrip() + '\n' + questions.rstrip()


def render_launcher(prompt, label, model, timeout, cpu_lane=False,
                    cpu_threads=4):
    """Pure: full turnkey launcher source (UTF-8 str).

    cpu_lane=True renders the tech#169 CPU variant (API flight with
    num_gpu=0/num_thread=4, no GPU preflight); both lane templates
    carry the tech#173 auto-ledger block (self-logging expert-calls
    row + verdict archive at landing time) with the E4 seat identity
    (tech#172 parametrization keeps the E4 output byte-identical)."""
    src = CPU_TEMPLATE if cpu_lane else TEMPLATE
    src = src.replace('__LABEL__', label.replace('\\', '\\\\'))
    src = src.replace('__MODEL__', repr(model))
    src = src.replace('__TIMEOUT__', str(int(timeout)))
    src = src.replace('__LABEL_REPR__', repr(label))
    src = src.replace('__PROMPT_REPR__', repr(prompt))
    src = src.replace('__THREADS__', str(int(cpu_threads)))
    src = src.replace('__AUTO_LEDGER_BLOCK__', AUTO_LEDGER_BLOCK)
    src = src.replace('__EXPERT_ID__', repr(E4_EXPERT_ID))
    src = src.replace('__ROLE_DEPT_EXPR__', repr(E4_ROLE_DEPT))
    return src


def render_expert_launcher(expert_id, material_rel, result_name, timeout,
                           cpu_threads=4):
    """Pure: turnkey registry-seat launcher source (UTF-8 str).

    tech#172 expert face: the R2257 hand-written s1_call_cpu.py
    lineage as a generated artifact. Seat identity is baked as the
    expert id; the seat model, prompt file, and role/dept text stay
    registry-owned (read at flight time -- `role_dept` is the
    variable the shared auto-ledger block references, so the ledger
    row's dept column tracks the registry, not this file)."""
    src = EXPERT_TEMPLATE
    src = src.replace('__EXPERT__', expert_id.replace('\\', '\\\\'))
    src = src.replace('__MATERIAL__', material_rel.replace('\\', '\\\\'))
    src = src.replace('__MATERIAL_REPR__', repr(material_rel))
    src = src.replace('__RESULT_REPR__', repr(result_name))
    src = src.replace('__TIMEOUT__', str(int(timeout)))
    src = src.replace('__THREADS__', str(int(cpu_threads)))
    src = src.replace('__AUTO_LEDGER_BLOCK__', AUTO_LEDGER_BLOCK)
    # seat-identity placeholders live INSIDE the block too -- both
    # replaces must run AFTER the block insertion (one global pass
    # covers the template constant line and the block's copy).
    src = src.replace('__EXPERT_ID__', repr(expert_id))
    src = src.replace('__ROLE_DEPT_EXPR__', 'role_dept')
    return src


def _read_text(path):
    with io.open(path, 'r', encoding='utf-8-sig') as fh:
        return fh.read()


def _repo_root():
    """Repo root walked up from THIS file (.git probe)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while d and d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, '.git')):
            return d
        d = os.path.dirname(d)
    return None


def _find_registry_seat(root, expert_id):
    """(seat dict or None, known id list) from the registry (pure read).

    Generation-time typo guard: the generated launcher re-reads the
    registry at flight time anyway (never hardcoded), so this check
    only catches unknown ids / empty prompt_file EARLY, before a
    staged fire card can die at flight time on a typo.
    """
    path = os.path.join(root, 'data', 'experts', 'registry.json')
    try:
        data = json.loads(io.open(path, encoding='utf-8-sig').read())
    except (OSError, ValueError) as exc:
        raise UsageError('registry unreadable: %s (%s)' % (path, exc))
    entries = data.get('experts') or data.get('roster') or []
    known = [str(e.get('id', '')) for e in entries]
    for e in entries:
        if str(e.get('id', '')) == expert_id:
            return e, known
    return None, known


def _validate_timeout(value):
    if value is None or int(value) <= 0:
        raise UsageError('--timeout must be a positive integer')


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='Launcher generator family (tech#113/#169/#172): '
                    'E4 card face (--body + --label -> e4_call.py / '
                    'e4_call_cpu.py) or registry-seat face (--expert + '
                    '--material -> <id>_call_cpu.py, the s1_call_cpu '
                    'lineage).')
    ap.add_argument('--body',
                    help='E4 card face: hand-written prompt body file '
                         '(role + card lines + background; WITHOUT the '
                         'question block)')
    ap.add_argument('--label',
                    help='E4 card face: material label for the result '
                         'JSON + launcher header')
    ap.add_argument('--out',
                    help='launcher output path (E4 default: <body dir>'
                         '/e4_call.py; expert default: <material dir>'
                         '/<id-lower>_call_cpu.py)')
    ap.add_argument('--model',
                    help='seat model name (default: BRAIN_MODEL env / '
                         'qwen3.6-35b on the CPU-lane faces, '
                         'qwen3.8:27b on the GPU face pending its '
                         'tech#185 retirement)')
    ap.add_argument('--timeout', type=int, default=1500)
    ap.add_argument('--questions-file',
                    help='override the canonical question block (whole file '
                         'verbatim; e.g. seat-form adaptation)')
    ap.add_argument('--cpu-lane', action='store_true',
                    help='E4 card face: render the tech#169 CPU-lane '
                         'variant (API flight with num_gpu=0/'
                         'num_thread=4, no GPU preflight; dispatch via '
                         'fire_consume.py --cpu-lane)')
    ap.add_argument('--expert',
                    help='registry-seat face (tech#172): registry seat id '
                         '(e.g. S1-script); renders the CPU-lane '
                         'registry-seat launcher (seat/prompt/role are '
                         'read from data/experts/registry.json at FLIGHT '
                         'time)')
    ap.add_argument('--material',
                    help='registry-seat face: material file path '
                         '(repo-relative in production; assembled '
                         'verbatim under the 材料块)')
    ap.add_argument('--result-name',
                    help='registry-seat face: result json file name '
                         '(default: <id-lower>-cpu-result.json)')
    args = ap.parse_args(argv)

    try:
        _validate_timeout(args.timeout)
        if args.expert or args.material:
            # ---------- registry-seat face (tech#172) ----------
            if args.body:
                raise UsageError('--expert face and --body face are '
                                 'exclusive (the registry owns the prompt; '
                                 'a body belongs to the E4 card face)')
            if args.label:
                raise UsageError('--expert face does not take --label '
                                 '(the ledger material column is the '
                                 'material path)')
            if args.questions_file:
                raise UsageError('--expert face does not take '
                                 '--questions-file (the registry '
                                 'prompt_file is the prompt)')
            if not (args.expert or '').strip():
                raise UsageError('--expert requires a registry seat id '
                                 '(e.g. S1-script)')
            if not (args.material or '').strip():
                raise UsageError('--expert face requires --material '
                                 '(repo-relative material path)')
            expert_id = args.expert.strip()
            material_rel = args.material.strip()
            root = _repo_root()
            if root is None:
                raise UsageError('no repo root above this generator -- '
                                 'cannot validate the registry seat')
            seat, known = _find_registry_seat(root, expert_id)
            if seat is None:
                raise UsageError('unknown expert id: %s (known: %s)'
                                 % (expert_id, ', '.join(known)))
            if not str(seat.get('prompt_file') or '').strip():
                raise UsageError('registry seat %s has no prompt_file'
                                 % expert_id)
            if not os.path.isfile(os.path.join(root, material_rel)):
                raise UsageError('material file not found (repo-relative '
                                 'or absolute): ' + material_rel)
            result_name = (args.result_name or '').strip() or (
                expert_id.lower() + '-cpu-result.json')
            out = args.out or os.path.join(
                root, os.path.dirname(material_rel),
                expert_id.lower() + '_call_cpu.py')
            if os.path.isdir(out):
                raise UsageError('--out points at an existing directory: '
                                 + out)
            src = render_expert_launcher(expert_id, material_rel,
                                         result_name, args.timeout)
            print('RESULT-FILE', result_name)
        else:
            # ---------- E4 card face (tech#113/#169) ----------
            if not args.body:
                raise UsageError('either --body (E4 card face) or --expert '
                                 '+ --material (registry-seat face) is '
                                 'required')
            if not args.label or not args.label.strip():
                raise UsageError('--label must be non-empty (E4 card '
                                 'face)')
            if not os.path.isfile(args.body):
                raise UsageError('body file not found: ' + args.body)
            body = _read_text(args.body)
            if not body.strip():
                raise UsageError('body file is empty: ' + args.body)
            if args.questions_file:
                if not os.path.isfile(args.questions_file):
                    raise UsageError('questions file not found: '
                                     + args.questions_file)
                questions = _read_text(args.questions_file)
                if not questions.strip():
                    raise UsageError('questions file is empty: '
                                     + args.questions_file)
            else:
                questions = CANONICAL_QUESTIONS
            prompt = build_prompt(body, questions)
            # tech#186 per-face default: the CPU face flies the brain
            # lane (env BRAIN_MODEL), the GPU face keeps its legacy
            # default until the tech#185 retirement ruling.
            model = args.model or (
                os.environ.get('BRAIN_MODEL', 'qwen3.6-35b')
                if args.cpu_lane else 'qwen3.8:27b')
            out = args.out or os.path.join(
                os.path.dirname(os.path.abspath(args.body)), 'e4_call.py')
            if os.path.isdir(out):
                raise UsageError('--out points at an existing directory: '
                                 + out)
            src = render_launcher(prompt, args.label, model,
                                   args.timeout, cpu_lane=args.cpu_lane)
    except UsageError as exc:
        print('USAGE-ERROR:', exc)
        return 2

    parent = os.path.dirname(os.path.abspath(out))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with io.open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(src)
    print('WROTE', os.path.abspath(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
