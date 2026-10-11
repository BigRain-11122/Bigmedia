# -*- coding: utf-8 -*-
"""R2004 tech#113 dogfood: regenerate the v18 hand-written launcher from
its extracted body and diff against the proven v17/v18 lineage."""
import difflib
import io
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src', 'os'))
import e4_launcher_gen as gen  # noqa: E402

V18 = os.path.join(ROOT, 'data', 'storylines', 'cards',
                   'MC-20261011-DIGEST-v18-tmp', 'e4_call.py')
OUTDIR = os.path.join(ROOT, '.c3-tmp', 'r2004_e4gen_parity')

src18 = io.open(V18, encoding='utf-8').read()
cut = src18.index("result = {'ts'")
ns = {'__file__': V18}
exec(compile(src18[:cut], 'v18_head', 'exec'), ns)  # imports+HERE+prompt only
prompt18 = ns['prompt']

body = prompt18[:prompt18.index(gen.QUESTION_MARKER)].rstrip()
regen_prompt = gen.build_prompt(body, gen.CANONICAL_QUESTIONS)
machinery18 = src18[cut:]
regen_src = gen.render_launcher(
    regen_prompt, 'MC-20261011-DIGEST-v18 static card (parity regen)',
    'qwen2.5:14b', 1500)
regen_machinery = regen_src[regen_src.index("result = {'ts'"):]

os.makedirs(OUTDIR, exist_ok=True)
body_path = os.path.join(OUTDIR, 'body.txt')
io.open(body_path, 'w', encoding='utf-8').write(body)
io.open(os.path.join(OUTDIR, 'e4_call.py'), 'w', encoding='utf-8').write(regen_src)

print('BODY_CHARS', len(body))
print('--- PROMPT DELTAS (hand v18 -> generated) ---')
out = ['BODY_CHARS %d' % len(body),
       '--- PROMPT DELTAS (hand v18 -> generated) ---']
for ln in difflib.unified_diff(
        prompt18.splitlines(), regen_prompt.splitlines(), lineterm='', n=0):
    if ln.startswith(('---', '+++', '@@')):
        continue
    print(ln)
    out.append(ln)
print('--- MACHINERY DELTAS (hand v18 -> generated) ---')
out.append('--- MACHINERY DELTAS (hand v18 -> generated) ---')
for ln in difflib.unified_diff(
        machinery18.splitlines(), regen_machinery.splitlines(), lineterm='', n=0):
    if ln.startswith(('---', '+++', '@@')):
        continue
    print(ln)
    out.append(ln)
print('PARITY-OUT', OUTDIR)
out.append('PARITY-OUT ' + OUTDIR)
io.open(os.path.join(OUTDIR, 'r2004_parity_out.txt'), 'w',
        encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
