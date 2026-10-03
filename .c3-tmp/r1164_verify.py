# -*- coding: utf-8 -*-
# R1164 ledger recheck with correct UTF-8 regex (r1164_all.py PS round-trip suspected mojibake)
import io, re, os, hashlib, datetime
ledger = r'C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md'
raw = io.open(ledger, encoding='utf-8', errors='replace').read()
pat = re.compile(r'@(BigStream|\u4e03\u7ebf\u5168\u53f8|\u5168\u53f8|\u516d\u53f8|\u516b\u7ebf\u5168\u91cf)')
cnt = sum(1 for line in raw.splitlines() if pat.search(line))
bs = sum(1 for line in raw.splitlines() if '@BigStream' in line)
print('now=%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print('ledger_sha256=%s' % hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16])
print('LEDGER_ALL_PAT=%d  @BigStream_only=%d  mtime=%s' % (cnt, bs, datetime.datetime.fromtimestamp(os.path.getmtime(ledger)).strftime('%m-%d %H:%M')))
# also check whether r1164_all.py regex got corrupted: compare with r1163_all.py bytes
a = io.open(r'.c3-tmp\r1163_all.py', 'rb').read()
b = io.open(r'.c3-tmp\r1164_all.py', 'rb').read()
print('r1163_all.py bytes=%d  r1164_all.py bytes=%d  bom_r1164=%s' % (len(a), len(b), b[:3] == b'\xef\xbb\xbf'))
try:
    ta = io.open(r'.c3-tmp\r1163_all.py', encoding='utf-8').read()
    tb = io.open(r'.c3-tmp\r1164_all.py', encoding='utf-8-sig').read()
    print('regex_r1163=%r' % re.search(r"pat = re.compile\((.+)\)", ta).group(1))
    print('regex_r1164=%r' % re.search(r"pat = re.compile\((.+)\)", tb).group(1))
except Exception as e:
    print('cmp_err=%r' % e)
