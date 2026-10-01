# -*- coding: utf-8 -*-
# r873 fix 2: remove trailing comma after the (new) last log entry R873.
import sys

p = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
data = open(p, "rb").read()
pairs = [(b'",\n ],', b'"\n ],'), (b'",\r\n ],', b'"\r\n ],')]
done = False
for bad, good in pairs:
    n = data.count(bad)
    if n == 1:
        data = data.replace(bad, good)
        open(p, "wb").write(data)
        print("TRAILING-COMMA-REMOVED pattern=%r" % bad)
        done = True
        break
    elif n > 1:
        print("AMBIGUOUS count=%d pattern=%r" % (n, bad))
        sys.exit(1)
if not done:
    print("PATTERN-NOT-FOUND")
    sys.exit(1)
