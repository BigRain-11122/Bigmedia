# r482_tail.py - dump state.json tail to utf-8 file for exact replace anchoring (ASCII-only script)
import io, datetime

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"
OUTP = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r482_tail.txt"
s = io.open(P, encoding="utf-8").read()
with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("now=" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    f.write("len=%d\n" % len(s))
    f.write("TAIL_BEGIN\n" + s[-500:] + "\nTAIL_END\n")
print("OK now=%s len=%d" % (datetime.datetime.now().strftime("%H:%M:%S"), len(s)))
