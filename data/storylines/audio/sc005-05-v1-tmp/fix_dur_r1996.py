import io

p = r"data\storylines\audio\sc005-05-v1-tmp\e4-material.md"
s = io.open(p, encoding="utf-8").read()
old = "时长约 3 分 11 秒"
new = "时长约 3 分 34 秒"
if old in s:
    s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("changed")
else:
    print("old-string-not-found")
