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

# HTTP health (R1752 pre-flight guard)
def get(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.status, resp.read(300)
    except Exception as e:
        return None, str(e)[:120]
st, body = get("http://127.0.0.1:3101/api/health")
w("api_health=%s %s" % (st, body))
st, body = get("http://127.0.0.1:3100/")
w("web=%s" % st)

w("=== articles by processing_state ===")
w(sql("SELECT processing_state, count(*) FROM articles GROUP BY 1 ORDER BY 2 DESC;"))
w("=== publications distribution (all) ===")
w(sql("SELECT count(*) total, count(score) scored, round(avg(score)::numeric,1) avg, min(score), max(score), count(*) FILTER (WHERE score>=60) ge60, count(*) FILTER (WHERE score>=65) ge65, count(*) FILTER (WHERE score>=76) ge76, count(*) FILTER (WHERE selected) sel FROM publications;"))
w("=== publications 16k era (updated_at > 21:25) ===")
w(sql("SELECT count(*) total, count(score) scored, round(avg(score)::numeric,1) avg, min(score), max(score), count(*) FILTER (WHERE score>=60) ge60, count(*) FILTER (WHERE score>=65) ge65, count(*) FILTER (WHERE score>=76) ge76, count(*) FILTER (WHERE selected) sel FROM publications WHERE updated_at > timestamptz '2026-10-08 21:25:00+08';"))
w("=== receipts since 21:28 by model/status ===")
w(sql("SELECT model, status, count(*), round(avg(extract(epoch from completed_at-created_at))::numeric,0) avg_s FROM receipts WHERE created_at > timestamptz '2026-10-08 21:28:00+08' GROUP BY 1,2 ORDER BY 3 DESC;"))
w("=== reports recent ===")
w(sql("SELECT id, kind, key, model, generated_at, length(content::text) len FROM reports ORDER BY created_at DESC LIMIT 5;"))
w("=== job_runs recent ===")
w(sql("SELECT * FROM job_runs ORDER BY id DESC LIMIT 2;"))
w("=== selected count ===")
w(sql("SELECT count(*) FROM publications WHERE selected;"))

io.open(os.path.join(BASE, r".c3-tmp\r1771_aihot.txt"), "w", encoding="utf-8").write("\n".join(out))
print("phase-A done")

# Phase B: requeue residual failed via admin API (audit-facing, R1770 path)
out2 = []
def w2(s): out2.append(str(s))
try:
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    data = urllib.parse.urlencode({"password": ENV["ADMIN_PASSWORD"], "return": "/admin"}).encode()
    req = urllib.request.Request("http://127.0.0.1:3101/api/auth/password", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    opener.open(req, timeout=15)
    me = json.load(opener.open("http://127.0.0.1:3101/api/admin/me", timeout=15))
    csrf = me.get("csrf")
    w2("login=ok csrf=%s" % ("" if not csrf else "present"))
    req = urllib.request.Request("http://127.0.0.1:3101/api/admin/processing/requeue",
        data=json.dumps({"group": None, "reason": "R1771 clean sweep of residual failed articles in 16k model era"}).encode(),
        headers={"Content-Type": "application/json", "x-csrf-token": csrf or ""})
    resp = opener.open(req, timeout=60)
    w2("requeue=%s" % resp.read().decode("utf-8", errors="replace")[:600])
except Exception as e:
    w2("requeue_error=%s" % str(e)[:300])

io.open(os.path.join(BASE, r".c3-tmp\r1771_requeue.txt"), "w", encoding="utf-8").write("\n".join(out2))
print("phase-B done")
