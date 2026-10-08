# -*- coding: utf-8 -*-
import json, io, os, subprocess, urllib.request, urllib.parse, http.cookiejar, time

BASE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
POC = os.path.join(BASE, r"data\assets\aihot-poc")
PSQL = os.path.join(POC, r"pg17\pgsql\bin\psql.exe")
ENV = {}
for line in io.open(os.path.join(POC, "AIHOT", ".env"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); ENV[k] = v

out = []
def w(s): out.append(str(s))
def sql(q):
    r = subprocess.run([PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-c", q], capture_output=True)
    o = r.stdout.decode("utf-8", errors="replace")
    e = r.stderr.decode("utf-8", errors="replace").strip()
    return o + (("ERR:" + e) if e else "")

w("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
# confirm model error signature of the 21:49 batch (evidence for the op-red log)
w(sql("SELECT left(coalesce(error,''),90) err, count(*) FROM receipts WHERE created_at > timestamptz '2026-10-08 21:48:30+08' GROUP BY 1 ORDER BY 2 DESC LIMIT 3;"))

try:
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    data = urllib.parse.urlencode({"password": ENV["ADMIN_PASSWORD"], "return": "/api/admin/me"}).encode()
    req = urllib.request.Request("http://127.0.0.1:3101/api/auth/password", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        opener.open(req, timeout=15)
    except urllib.error.HTTPError as e:
        w("login_follow=%s (tolerated)" % e.code)
    me = json.load(opener.open("http://127.0.0.1:3101/api/admin/me", timeout=15))
    req = urllib.request.Request("http://127.0.0.1:3101/api/admin/processing/requeue",
        data=json.dumps({"group": None, "reason": "R1771 re-requeue after model-not-found batch (worker started before qwen2.5:14b-8k creation; model now in place)"}).encode(),
        headers={"Content-Type": "application/json", "x-csrf-token": me.get("csrf") or ""})
    resp = opener.open(req, timeout=120)
    w("requeue=%s" % resp.read().decode("utf-8", errors="replace")[:300])
except Exception as e:
    w("requeue_error=%s" % str(e)[:200])

io.open(os.path.join(BASE, r".c3-tmp\r1771_requeue3.txt"), "w", encoding="utf-8").write("\n".join(out))
print("requeue3 done")
