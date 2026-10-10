"""R1887: requeue failed AIHOT articles via admin API (R1836 craft).

Login (NoRedirect to keep the 303's Set-Cookie session) -> GET /api/admin/me
for CSRF -> POST /api/admin/processing/requeue {group: null, reason}.
group=null = all failure groups from the last 30 days, which includes the
34 city-source failed items (R1876 count). Retries now run under the NEW
city wordings (worker restarted this round).
"""
import json
import re
import urllib.request

BASE = "http://127.0.0.1:3101"
ENV = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\assets\aihot-poc\AIHOT\.env"

with open(ENV, encoding="utf-8") as f:
    password = next(line.split("=", 1)[1].strip() for line in f if line.startswith("ADMIN_PASSWORD="))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = urllib.request.build_opener(NoRedirect)

# 1) password login -> 303 + Set-Cookie session (returnTo /api/admin/me per R1770 fix)
body = ("password=" + urllib.parse.quote(password) + "&return=/api/admin/me").encode()
req = urllib.request.Request(BASE + "/api/auth/password", data=body,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    resp = opener.open(req, timeout=15)
except urllib.error.HTTPError as e:
    if e.code not in (302, 303, 307):
        raise
    resp = e  # the 303 carries Set-Cookie
set_cookie = resp.headers.get("Set-Cookie", "")
session = set_cookie.split(";")[0]
print("LOGIN-OK status=%s cookie=%s..." % (resp.status if hasattr(resp, "status") else resp.code, session[:20]))

# 2) CSRF token
req = urllib.request.Request(BASE + "/api/admin/me", headers={"Cookie": session})
me = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
csrf = me["csrf"]
print("CSRF-OK admin=%s" % me["name"])

# 3) requeue all failed groups
payload = json.dumps({"group": None,
                       "reason": "R1887 requeue under city criterion: worker restarted with prefilter-city + selection-score-city; city failed pool 34 + others retry under new wording"}).encode()
req = urllib.request.Request(BASE + "/api/admin/processing/requeue", data=payload,
                             headers={"Cookie": session, "X-CSRF-Token": csrf,
                                      "Content-Type": "application/json"})
result = urllib.request.urlopen(req, timeout=30).read().decode()
print("REQUEUE-RESULT:", result)
