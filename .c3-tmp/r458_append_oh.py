# R458: append slice-2 section (from UTF-8 data file) to the OH window ledger.
import io

OH = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\oss-harvest\OH-20260926-bigstream.md'
SRC = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r458_oh_slice2.md'

body = io.open(OH, encoding='utf-8').read()
add = io.open(SRC, encoding='utf-8').read()

# idempotence guard: skip if slice-2 marker already present
if 'R458' in body and 'slice 2' in body.lower():
    print('already-appended')
else:
    if not body.endswith('\n'):
        body += '\n'
    body += add
    io.open(OH, 'w', encoding='utf-8', newline='\n').write(body)
    print('appended ok, new-len', len(body))
