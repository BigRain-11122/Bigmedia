# R2010 tech#117: consumption scan - match pool lines against 15 REACT cards' cards.json verbatim
import json, io, sys, os, glob, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
POOL = r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json'
CARD_ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\storylines\cards'
d = json.load(open(POOL, encoding='utf-8'))
axes, buckets = d['axes'], d['sprite'].keys() if isinstance(d['sprite'], dict) else []
BUCKETS = ['morning','dusk','night','weekend','rain','typhoon','heatwave','coldsnap','market_open','market_close','ceo_order','festival']

# sample one cards.json to learn schema
c1 = json.load(open(os.path.join(CARD_ROOT, 'MC-20260926-REACT-v1', 'cards.json'), encoding='utf-8'))
print('=== cards.json schema (v1) ===')
print(json.dumps(c1, ensure_ascii=False, indent=1)[:1500])
