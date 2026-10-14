# -*- coding: utf-8 -*-
# E4 audience reference call (CPU LANE) - SC-005-07 audio piece.
# Adapted from the tech#169 generated pattern (MC-20261014-REACT-v18
# e4_call_cpu.py); audio-line series predates the card generator, prompt
# body = sc005-07-v1-tmp/e4-material.md verbatim + standard E4 audio
# questions (call_expert E4-audience registry question block).
# CPU lane laws: O-20260913-2215 CPU 24/7 + CEO 10% margin (num_thread=4)
# + zero GPU touch (num_gpu=0 -- the assertion IS the flight).
# rc: 0 = verdict in e4-result.json | 3 = transport error.
import io, json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = 'qwen2.5:14b'
TIMEOUT = 1500
CPU_THREADS = 4
GENERATE_URL = 'http://localhost:11434/api/generate'
MATERIAL = 'SC-005-07-v1'

material = io.open(os.path.join(HERE, 'e4-material.md'),
                   encoding='utf-8').read().strip()
questions = (
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这条音频帖你会点开听吗？会听完吗？会保存或转发给朋友吗？'
    '打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？')
prompt = material + '\n\n' + questions

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': MODEL,
          'material': MATERIAL, 'lane': 'cpu'}
payload = json.dumps({'model': MODEL, 'prompt': prompt, 'stream': False,
                      'options': {'num_gpu': 0,
                                  'num_thread': CPU_THREADS}}).encode('utf-8')
request = urllib.request.Request(GENERATE_URL, data=payload,
                                 headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(request, timeout=TIMEOUT) as resp:
        body = json.loads(resp.read().decode('utf-8', 'replace'))
    result['verdict'] = (body.get('response') or '').strip() or \
        'EMPTY-RESPONSE'
except Exception as exc:
    text = '%s: %s' % (type(exc).__name__, exc)
    if 'timed out' in text.lower() or 'timeout' in text.lower():
        result['verdict'] = 'TIMEOUT-%ds' % TIMEOUT
    else:
        print('TRANSPORT-ERROR %s' % text, flush=True)
        raise SystemExit(3)
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if not result['verdict'].startswith('TIMEOUT') else 'TIMEOUT')
