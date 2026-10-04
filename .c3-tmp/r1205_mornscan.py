import io, json, re
st = json.load(io.open(r'src\os\state.json', encoding='utf-8'))
logs = st.get('log', [])
e1124 = [e for e in logs if re.match(r'^\S+ \S+ R1124:', e)][0]
io.open(r'.c3-tmp\r1205_adj.txt', 'w', encoding='utf-8').write(e1124[-2800:])
ms = []
for e in logs:
    m = re.match(r'^\S+ \S+ R(\d{4}):', e)
    if m and int(m.group(1)) >= 1125:
        hit = re.search(r'morning|晨间|晨窗', e)
        if hit:
            ms.append(e[:150])
io.open(r'.c3-tmp\r1205_morn.txt', 'w', encoding='utf-8').write('\n'.join(ms) if ms else 'NO_MENTION_R1125_PLUS')
print('morn hits:', len(ms))
