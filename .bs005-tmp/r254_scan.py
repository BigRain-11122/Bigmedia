# R254 window scan (Biggame console watch) + ch.6/comic sign check
import io
import subprocess
import glob
import os

r = subprocess.run(
    ["powershell", "-NoProfile", "-Command",
     "Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object -ExpandProperty MainWindowTitle"],
    capture_output=True)
titles = []
if r.returncode == 0 and r.stdout:
    for line in r.stdout.decode("utf-16-le", errors="ignore").splitlines():
        t = line.strip().lstrip("\ufeff").strip()
        if t:
            titles.append(t)
    if not titles:
        for line in r.stdout.decode("gbk", errors="ignore").splitlines():
            t = line.strip()
            if t:
                titles.append(t)

big = [t for t in titles if ("Biggame" in t) or ("\u603b\u63a7" in t)]
out = ["WINDOWS_N: %d" % len(titles),
       "BIGGAME_CONSOLE: %r" % big,
       "ALL_TITLES: %s" % " | ".join(titles)]
io.open(r".bs005-tmp/windows-R254.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("WINDOWS_N:", len(titles))
print("BIGGAME:", big)
