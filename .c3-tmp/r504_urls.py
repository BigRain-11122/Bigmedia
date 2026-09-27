# r504_urls.py - extract in-register URLs from user-research §3.5 area (cut-4 reuse targets)
import io, re

t = io.open(r"research\user-research-v1.md", encoding="utf-8").read()
pat = re.compile(r"https?://[^\s)\uff09\u3011\uff1b\uff0c\"']+")
for m in pat.finditer(t):
    u = m.group(0)
    print(u[:160])
print("---- §3.5 heading slice ----")
i = t.find("## \u00a73.5")
if i < 0:
    i = t.find("3.5")
print(t[i:i+2400].encode("unicode_escape").decode()[:2700])
