import re
src = open(r"src/os/state.json", encoding="utf-8").read()
for m in re.finditer(r'"ts": ', src):
    print(m.start(), repr(src[m.start():m.start()+40]))
print("---task---")
for m in re.finditer(r'"task": ', src):
    print(m.start(), repr(src[m.start():m.start()+70]))
