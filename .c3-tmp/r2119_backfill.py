# -*- coding: utf-8 -*-
"""R2119 queue done-marker backfill + supply-gate evidence + tech#42 gate-met note.
ASCII code; Chinese only in appended data strings. Fail-fast on every claim."""
import io, os, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
TECH = os.path.join(ROOT, 'state', 'queue', 'tech.md')
EV = os.path.join(ROOT, '.c3-tmp', 'r2119_supply_check.txt')

# --- evidence file: this round's supply-gate readouts ---
with io.open(EV, 'w', encoding='utf-8') as f:
    f.write('R2119 supply-gate recheck evidence (2026-10-13 06:5x)\n')
    f.write('1) BigLife tai-ci pool unlock gate (R1848 one-command recheck, first since 10-10 R1848):\n')
    f.write('   worktree unique strings = 1440 ; HEAD:cognition/pools.json unique = 1440 ; new-vs-HEAD = 0\n')
    f.write('   gate (unique>1440 OR row-diff non-empty) = LOCKED (main#12 gated stance holds)\n')
    f.write('   next recheck >= 2026-10-17 or on BigLife-side increment report\n')
    f.write('2) QUOTE supply (BigLife docs/CODEX.md sec.8 six-axis creed table):\n')
    f.write('   table rows = 6 (yan-huo/zhi-xu/qiu-xin/huai-jiu/xia-qi/xiao-yao) ; consumed by QUOTE-v1..v6 = F-013..F-018\n')
    f.write('   new rows vs consumed = 0 -> QUOTE supply EXHAUSTED, zero-action honest note\n')
    f.write('3) queue done-marker verification probes spent this round before backfill: ~6 tool calls (the repeat-scan tax this backfill removes)\n')

def probe(label, cond):
    if not cond:
        print('VERIFY-FAIL:', label)
        sys.exit(1)
    print('VERIFY-OK:', label)

p26 = os.path.join(ROOT, 'data', 'pipeline', 'asr-noise-dict-v3.json')
p31 = os.path.join(ROOT, 'src', 'os', 'loop_health.py')
p84 = os.path.join(ROOT, 'src', 'os', 'mv_sprint_probe.py')
p129 = os.path.join(ROOT, 'src', 'os', 'group_scan.py')

probe('tech#26 v3 dict exists', os.path.exists(p26))
with io.open(p26, encoding='utf-8') as f:
    probe('tech#26 law cites tech#26', 'tech#26' in f.read())
lh = io.open(p31, encoding='utf-8').read()
probe('tech#31 check_stale_dirty', 'def check_stale_dirty' in lh)
probe('tech#114 check_audio_tmp_residue', 'def check_audio_tmp_residue' in lh)
probe('tech#84 mv_sprint_probe file', os.path.exists(p84))
gs = io.open(p129, encoding='utf-8').read()
probe('tech#129 DIGEST-SUPPLY face', ('DIGEST-SUPPLY' in gs) or ('DIGEST_SUPPLY' in gs))
fc = os.path.join(ROOT, 'src', 'os', 'fire_consume.py')
probe('tech#135 throughput probe in fire_consume', 'throughput' in io.open(fc, encoding='utf-8').read())
exp = io.open(os.path.join(ROOT, 'state', 'queue', 'explore.md'), encoding='utf-8').read()
probe('tech#42 gate-met: explore#24 done R1956', 'done 2026-10-11 R1956' in exp)

MARK = ' ——**[backfill-done 2026-10-13 R2119]**：交付证机核在盘（{ev}）·原交付轮散见历轮台账·done 标回填防重扫税'
NOTE42 = ' ——**[gate-met 2026-10-13 R2119]**：前置 explore#24 已 done R1956（118 号视频文件实践指南 PDF 全文直采=字段级参数技术输入在案）→ 本项转可领（CPU 面·ffmpeg -metadata/XMP 自愿嵌入评估·下窗候选）'
BACKFILL = {
    26: 'asr-noise-dict-v3.json law=tech#26',
    31: 'loop_health.check_stale_dirty 面在役',
    84: 'src/os/mv_sprint_probe.py 在役（fire 卡 mv-active 判据面·tech#86 --ledger 承接）',
    114: 'loop_health.check_audio_tmp_residue 面在役（domain_prefix 参数化=tech#115 观察位承接）',
    129: 'group_scan DIGEST-SUPPLY advisory face 在役（R2117/R2118 每轮读数）',
    135: 'R2116 交付（P-7 pilot 腿·fire-consume-ledger throughput_probe 字段在役）',
}

with io.open(TECH, encoding='utf-8') as f:
    lines = f.read().splitlines(True)

out, hits = [], []
for ln in lines:
    s = ln.lstrip()
    matched = False
    for n, ev in BACKFILL.items():
        pref = '%d. ' % n
        pref2 = '%d.[' % n
        if (s.startswith(pref) or s.startswith(pref2)) and not matched:
            if ('[backfill-done' in ln) or ('[done' in ln):
                matched = True  # already marked, skip
                break
            ln = ln.rstrip('\r\n') + MARK.format(ev=ev) + '\n'
            hits.append(n)
            matched = True
            break
    if (not matched) and s.startswith('42. ') and ('gate-met' not in ln) and ('[done' not in ln):
        ln = ln.rstrip('\r\n') + NOTE42 + '\n'
        hits.append(42)
    out.append(ln)

missing = [n for n in list(BACKFILL) + [42] if n not in hits]
if missing:
    print('ANCHOR-MISS for:', missing)
    sys.exit(1)

with io.open(TECH, 'w', encoding='utf-8', newline='') as f:
    f.writelines(out)
print('TECH backfill written: markers =', sorted(hits))
print('evidence file:', EV)
