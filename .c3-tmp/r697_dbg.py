# -*- coding: utf-8 -*-
import io, re
ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
s = io.open(ROOT + r"\output\renders\README.md", encoding="utf-8").read()
src = io.open(ROOT + r"\.c3-tmp\r697_close.py", encoding="utf-8").read()
m = re.search(r'old2 = u"([^"]+)"', src)
raw = m.group(1)
old2 = raw.encode("utf-8", "backslashreplace").decode("unicode_escape") if "\\u" in raw else raw
# more robust: let python parse the literal
old2_parsed = eval('u"' + raw + '"')
out = io.open(ROOT + r"\.c3-tmp\r697_dbg.txt", "w", encoding="utf-8")
out.write("old2 (parsed) in s: %s\n" % (old2_parsed in s))
out.write("old2 repr: %r\n" % old2_parsed)
i = s.find("s1-review-material-v1.md")
j = s.find("\n", i)
out.write("file seg: %r\n" % s[i:j+1])
for pos in range(len(old2_parsed)):
    if s.find(old2_parsed[:pos+1]) < 0:
        prev = s.find(old2_parsed[:pos])
        out.write("first break at pos %d: expected %r (U+%04X); file context: %r\n" % (pos, old2_parsed[pos], ord(old2_parsed[pos]), s[max(0,prev-5):prev+10]))
        break
out.close()
print("dbg written")
