# -*- coding: utf-8 -*-
# r873 fix: insert missing comma after former-last log entry (R872) before R873 entry.
import sys

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
data = open(p, "rb").read()
marker = '  "2026-10-01 17:44 R873:'.encode("utf-8")
i = data.find(marker)
if i < 0:
    print("MARKER-NOT-FOUND")
    sys.exit(1)
j = i
while data[j - 1 : j] in (b"\r", b"\n"):
    j -= 1
prev_end = data[:j]
if prev_end.endswith(b'",'):
    print("ALREADY-COMMA no-op")
elif prev_end.endswith(b'"'):
    fixed = prev_end + b"," + data[j:]
    open(p, "wb").write(fixed)
    print("COMMA-INSERTED at byte %d" % (j - 1))
else:
    print("UNEXPECTED-ENDING tail=%r" % prev_end[-8:])
    sys.exit(1)
