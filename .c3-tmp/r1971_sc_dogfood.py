# -*- coding: utf-8 -*-
# R1971 dogfood: extract r1970 ad-hoc anchors/card-pairs, run canonical
# src/render/sc_beats_check.py against the real SC-005-05 piece, compare parity.
import ast, io, os, re, subprocess, sys, tempfile

BASE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
ADHOC = os.path.join(BASE, r'.c3-tmp\r1970_sc00505_check.py')
BEATS = os.path.join(BASE, r'data\storylines\audio\SC-005-05-v1.beats.txt')
MAT = os.path.join(BASE, r'data\storylines\audio\SC-005-05-v1-s1-material.md')
CARD = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\census\anchors\C-00015.md'
OUT = os.path.join(BASE, r'.c3-tmp\r1971_sc_check_evidence.txt')

src = io.open(ADHOC, encoding='utf-8').read()
tree = ast.parse(src)
anchors, card_forms = None, None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id == 'anchors':
            anchors = [e.value for e in node.value.elts if isinstance(e, ast.Constant)]
        if node.targets[0].id == 'card_forms':
            card_forms = []
            for e in node.value.elts:
                tup = ast.literal_eval(e)
                card_forms.append(tup)
leaks = re.search(r"for s in \((.*?)\) if s in beats", src).group(1)
leak_list = [x.strip().strip("'") for x in leaks.split(",") if x.strip()]

td = tempfile.mkdtemp()
af = os.path.join(td, 'anchors.txt')
io.open(af, 'w', encoding='utf-8', newline='\n').write('\n'.join(anchors) + '\n')
pf = os.path.join(td, 'card_pairs.txt')
plines = []
for beats_form, card_form in card_forms:
    if card_form is None:
        plines.append(beats_form)
    else:
        plines.append(beats_form + '||' + card_form)
io.open(pf, 'w', encoding='utf-8', newline='\n').write('\n'.join(plines) + '\n')
print('extracted: anchors=%d card_pairs=%d leaks=%d' % (len(anchors), len(card_forms), len(leak_list)))

cmd = [sys.executable, os.path.join(BASE, 'src', 'render', 'sc_beats_check.py'),
       '--beats', BEATS, '--material', MAT, '--anchors', af,
       '--card', CARD, '--card-anchors', pf, '--out', OUT]
for lk in leak_list:
    cmd += ['--leak', lk]
r = subprocess.run(cmd, capture_output=True)
sys.stdout.write(r.stdout.decode('utf-8', errors='replace'))
print('CLI_RC=%d' % r.returncode)
