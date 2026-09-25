# R254 window scan v2: write via Out-File utf8 then read utf-8-sig (R248 precedent)
import io
import subprocess

ps = ("Get-Process | Where-Object {$_.MainWindowTitle} | "
      "Select-Object -ExpandProperty MainWindowTitle | "
      "Out-File -Encoding utf8 .bs005-tmp\\windows-R254.txt")
subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)
lines = io.open(r".bs005-tmp/windows-R254.txt", encoding="utf-8-sig").read().splitlines()
titles = [l.strip() for l in lines if l.strip()]
big = [t for t in titles if ("Biggame" in t) or ("\u603b\u63a7" in t)]
taujie = [t for t in titles if ("Tuanjie" in t) or ("Unity" in t)]
print("WINDOWS_N:", len(titles))
print("BIGGAME_CONSOLE:", big)
print("TAUJIE_UNITY:", taujie)
