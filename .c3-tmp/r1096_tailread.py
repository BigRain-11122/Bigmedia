import io
t = io.open(r'src\os\state.json', encoding='utf-8').read()
i = t.rfind('"2026-10-03 12:59x R1095')
out = io.open(r'.c3-tmp\r1096_tail.txt', 'w', encoding='utf-8')
out.write('R1095 line start:\n' + t[i:i+200] + '\n\n')
out.write('=== tail 900 chars ===\n' + t[-900:] + '\n')
out.close()
print('written, R1095 at offset', i)
