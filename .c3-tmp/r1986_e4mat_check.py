# r1986: e4-material verbatim check vs cards.json lines (v18)
import io, json, sys
sys.stdout.reconfigure(encoding='utf-8')
base = 'data/storylines/cards/MC-20261011-DIGEST-v18'
cj = json.load(io.open(base + '/cards.json', encoding='utf-8'))
lines = cj['cards'][0]['lines']
mat = io.open(base + '-tmp/e4-material.md', encoding='utf-8').read()
quote = 'mv的评审要分层级，' + lines[3]
ok = 0; miss = []
for ln in lines:
    if ln == lines[2] or ln == lines[3]:
        continue  # quote handled joined below
    if ln in mat:
        ok += 1
    else:
        miss.append(ln)
if quote in mat:
    ok += 1
else:
    miss.append('JOINED-QUOTE:' + quote)
checks = len(lines) - 2 + 1  # two quote lines joined into one
print('VERBATIM_OK=', ok, '/', checks)
for m in miss:
    print('MISS:', m)
print('AIGC:', cj['aigc_notice'] in mat)
print('DECLARATION:', '基于硅基城市真实事件（全曲冲刺日令批台账档案）' in mat)
