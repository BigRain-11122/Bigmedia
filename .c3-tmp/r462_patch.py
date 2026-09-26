# r462_check.py (fixed copy of r461_check.py): only OUTP retargeted to r462_check.txt
# patch applied via utf-8-safe python edit, not PS roundtrip (encoding law)
import io

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
src = io.open(ROOT + r"\.c3-tmp\r461_check.py", encoding="utf-8").read()
patched = src.replace('r461_check.txt', 'r462_check.txt').replace('r461 fast-path', 'r462 fast-path')
assert 'r462_check.txt' in patched and 'OUTP' in patched
io.open(ROOT + r"\.c3-tmp\r462_check.py", "w", encoding="utf-8").write(patched)
print("PATCHED")
