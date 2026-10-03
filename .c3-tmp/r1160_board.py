import io, re
t = io.open(r'C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md', encoding='utf-8').read()
lines = t.splitlines()
# board rows: table rows starting with | D- or | C- (dispatch board format)
board = [l for l in lines if re.match(r'^\|\s*[DC]-\d{8}-\d{2}', l)]
bs = [l for l in board if re.search(r'BigStream|七线全司|全司|六司|八线全量', l)]
out = ['board_rows_total=%d' % len(board), 'bs_involving=%d' % len(bs)]
for l in bs: out.append('BS| ' + l[:200])
io.open(r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1160_board.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
