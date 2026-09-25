# -*- coding: utf-8 -*-
"""R271 collect: inspect state.json tail, then update tick/focus/log/ts/task."""
import io, sys

sys.stdout.reconfigure(encoding="utf-8")
P = r"src\os\state.json"
t = io.open(P, encoding="utf-8").read()

i = t.find("R270: idle-fast")
print(repr(t[i - 40 : i + 100]))
print("---")
j = t.rfind('"ts"')
print(repr(t[j - 100 : j + 420]))
print("LEN", len(t))
