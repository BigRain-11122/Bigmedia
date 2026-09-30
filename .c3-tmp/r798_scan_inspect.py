import io, re

t = io.open(r'.c3-tmp\r798_scan_out.txt', encoding='utf-8', errors='replace').read()
t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', t)
o = io.open(r'.c3-tmp\r798_scan_lines.txt', 'w', encoding='ascii', errors='backslashreplace')
o.write(t)
o.close()
print('written', len(t))
