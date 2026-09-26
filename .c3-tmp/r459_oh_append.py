# R459 slice-3 idempotent append to cph4 OH ledger (CEO-order exception, single file)
import io

OH = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20260926-bigstream.md'
SLICE = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r459_oh_slice3.md'
GUARD = '## 切片 3（R459'

with io.open(OH, encoding='utf-8') as f:
    body = f.read()
if GUARD in body:
    print('ALREADY_PRESENT skip')
else:
    with io.open(SLICE, encoding='utf-8') as f:
        piece = f.read().strip('\n')
    if not body.endswith('\n'):
        body += '\n'
    body += '\n' + piece + '\n'
    with io.open(OH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(body)
    print('APPENDED', len(piece), 'chars')
