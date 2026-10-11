# -*- coding: utf-8 -*-
# R1978 format restore: state.json back to the repo's indent=1 convention
# (R1978 close wrote indent=2 -> full-file diff noise; restore so the next
# round's close script (copied from history) produces a minimal diff again).
import json
from pathlib import Path

state_path = Path('src/os/state.json')
with open(str(state_path), 'r', encoding='utf-8') as fh:
    state = json.load(fh)
with open(str(state_path), 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(state, fh, ensure_ascii=False, indent=1)
    fh.write('\n')
print('state.json rewritten with indent=1; tick=%s' % state['tick'])
