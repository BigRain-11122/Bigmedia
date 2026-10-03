import io, re
t = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
m = re.search(r"派工通告板(.*?)(?:\n#{1,3} |\Z)", t, re.S)
board = m.group(1) if m else ""
rows = [ln.strip() for ln in board.splitlines() if ln.strip().startswith('|') and not re.match(r'^\|[\s\-|]+$', ln.strip())]
bsrows = [ln for ln in rows if re.search(r"BigStream|七司", ln)]
out = ['board_total_rows=%d (wm baseline 46+2 new D-20261004-02 rows expected 48)' % len(rows),
       'bs_qixian_rows=%d (baseline 8)' % len(bsrows)]
for ln in bsrows: out.append('BS| ' + ln[:160])
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1160_board2.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('rows=%d bs=%d' % (len(rows), len(bsrows)))
