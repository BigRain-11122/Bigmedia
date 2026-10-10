import os, time
root = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\fleet\meme-daily-v1\outbound"
print("=== meme outbound newest 8 ===")
entries = []
for cur, dirs, files in os.walk(root):
    for f in files:
        p = os.path.join(cur, f)
        entries.append((os.path.getmtime(p), os.path.relpath(p, root)))
entries.sort(reverse=True)
for t, rel in entries[:8]:
    print(time.strftime("%H:%M:%S", time.localtime(t)), rel)
