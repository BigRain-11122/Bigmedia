# -*- coding: utf-8 -*-
import json, io
d = json.load(io.open(r'C:\Users\sjs20\Desktop\FluxGroup\life\BigLife\cognition\pools.json', encoding='utf-8'))
tot = [0]
def walk(o):
    if isinstance(o, dict):
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
    elif isinstance(o, str):
        tot[0] += 1
walk(d)
print('pools quote strings total:', tot[0])
