# r489_tail.py - extract exact state.json log-array boundary + ts/task lines (ASCII script, utf-8 out)
import io, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8").read()
OUTP = os.path.join(ROOT, ".c3-tmp", "r489_tail.txt")

L = []
i = SP.index('\n ],')
L.append("BOUNDARY-REPR=" + repr(SP[i - 120:i + 40]))
j = SP.index('"ts"')
L.append("TS-TASK-REPR=" + repr(SP[j - 10:j + 400]))
k = SP.index('"tick"')
L.append("TICK-REPR=" + repr(SP[k - 5:k + 20]))
f = SP.index('"focus"')
L.append("FOCUS-HEAD-REPR=" + repr(SP[f:f + 60]))
# focus tail: last 80 chars of the focus string value
q = SP.index('"', f)  # opening quote of focus value
e = q + 1
while SP[e] != '"':
    e += 1
L.append("FOCUS-TAIL-REPR=" + repr(SP[e - 80:e + 3]))

SE = io.open(os.path.join(ROOT, "docs", "status-export.json"), "r", encoding="utf-8").read()
m = SE.index('"export_ts"')
L.append("EXPORT-TS-REPR=" + repr(SE[m:m + 50]))

with io.open(OUTP, "w", encoding="utf-8") as fo:
    fo.write("\n".join(x for x in L if x))
print("written")
