# r486_tail.py - dump exact tail chars of state.json for safe replace anchor (utf-8, new OUTP)
import io, os
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
OUTP = os.path.join(ROOT, ".c3-tmp", "r486_tail.txt")
with io.open(os.path.join(ROOT, "src", "os", "state.json"), "r", encoding="utf-8") as f:
    txt = f.read()
with io.open(OUTP, "w", encoding="utf-8") as f:
    f.write("LEN=%d\n" % len(txt))
    f.write("TAIL300>>>%s<<<\n" % txt[-300:])
print("written LEN=%d" % len(txt))
