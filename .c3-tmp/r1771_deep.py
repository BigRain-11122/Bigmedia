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

w("=== receipts 21:28+ status/purpose ===")
w(sql("SELECT status, purpose, count(*), to_char(min(created_at),'HH24:MI:SS') first, to_char(max(created_at),'HH24:MI:SS') last FROM receipts WHERE created_at > timestamptz '2026-10-08 21:28:00+08' GROUP BY 1,2 ORDER BY 3 DESC;"))

w("=== receipts 21:28+ error signatures ===")
w(sql("SELECT status, left(coalesce(error,''),110) err, count(*) FROM receipts WHERE created_at > timestamptz '2026-10-08 21:28:00+08' AND status IN ('unknown','failed') GROUP BY 1,2 ORDER BY 3 DESC LIMIT 12;"))

w("=== chain counts ===")
w(sql("SELECT (SELECT count(*) FROM analyses) analyses, (SELECT count(*) FROM embeddings) emb, (SELECT count(*) FROM stories) stories, (SELECT count(*) FROM articles WHERE processing_state='analyzed' AND grouping_status='pending') grp_pending;"))

w("=== job names since 20:00 ===")
w(sql("SELECT job, status, count(*), to_char(max(finished_at),'HH24:MI:SS') last FROM job_runs WHERE started_at > timestamptz '2026-10-08 20:00:00+08' GROUP BY 1,2 ORDER BY 3 DESC LIMIT 20;"))

w("=== usage sample of a received 16k receipt ===")
w(sql("SELECT purpose, usage FROM receipts WHERE created_at > timestamptz '2026-10-08 21:28:00+08' AND status='received' LIMIT 2;"))

io.open(os.path.join(BASE, r".c3-tmp\r1771_deep.txt"), "w", encoding="utf-8").write("\n".join(out))
print("deep done")

# requeue with tolerant login (404 on /admin redirect tolerated)
out2 = []
def w2(s): out2.append(str(s))
try:
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    data = urllib.parse.urlencode({"password": ENV["ADMIN_PASSWORD"], "return": "/api/admin/me"}).encode()
    req = urllib.request.Request("http://127.0.0.1:3101/api/auth/password", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        opener.open(req, timeout=15)
    except urllib.error.HTTPError as e:
        w2("login_follow=%s (cookiejar=%d)" % (e.code, len(cj)))
    names = [c.name for c in cj]
    w2("cookies=%s" % names)
    me = json.load(opener.open("http://127.0.0.1:3101/api/admin/me", timeout=15))
    csrf = me.get("csrf")
    w2("me=ok csrf=%s" % ("present" if csrf else "MISSING"))
    req = urllib.request.Request("http://127.0.0.1:3101/api/admin/processing/requeue",
        data=json.dumps({"group": None, "reason": "R1771 clean sweep of residual failed articles in 16k model era"}).encode(),
        headers={"Content-Type": "application/json", "x-csrf-token": csrf or ""})
    resp = opener.open(req, timeout=120)
    w2("requeue=%s" % resp.read().decode("utf-8", errors="replace")[:600])
except Exception as e:
    w2("requeue_error=%s" % str(e)[:300])
io.open(os.path.join(BASE, r".c3-tmp\r1771_requeue2.txt"), "w", encoding="utf-8").write("\n".join(out2))
print("requeue2 done")
