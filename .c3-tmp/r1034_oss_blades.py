import json, time, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "bigstream-oss-harvest",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        return {"ERROR": str(e)}

out = []
def blade(tag, url):
    d = get(url)
    out.append("== %s ==" % tag)
    if "ERROR" in d:
        out.append("ERROR " + d["ERROR"])
        return
    items = d.get("items", [])
    out.append("total_count=%s" % d.get("total_count"))
    for it in items[:6]:
        lic = (it.get("license") or {}).get("spdx_id")
        out.append("%s | lic=%s | stars=%s | push=%s | arch=%s | lang=%s | %s" % (
            it.get("full_name"), lic, it.get("stargazers_count"),
            it.get("pushed_at"), it.get("archived"), it.get("language"),
            (it.get("description") or "")[:110]))
    time.sleep(1)

blade("blade1 ffmpeg filtergraph python", "https://api.github.com/search/repositories?q=ffmpeg+filtergraph+python&sort=stars&per_page=6")
blade("blade2 mp4 faststart", "https://api.github.com/search/repositories?q=mp4+faststart&sort=stars&per_page=6")
blade("blade3 video quality control analysis", "https://api.github.com/search/repositories?q=video+quality+control+artifact+analysis&sort=stars&per_page=6")

# direct fetch of QC candidate for five-gate evaluation
d = get("https://api.github.com/repos/bavc/qctools")
out.append("== direct bavc/qctools ==")
if "ERROR" in d:
    out.append("ERROR " + d["ERROR"])
else:
    lic = (d.get("license") or {}).get("spdx_id")
    out.append("lic=%s stars=%s forks=%s push=%s arch=%s lang=%s desc=%s" % (
        lic, d.get("stargazers_count"), d.get("forks_count"),
        d.get("pushed_at"), d.get("archived"), d.get("language"),
        (d.get("description") or "")[:140]))

open("r1034_oss_blades.txt", "w", encoding="utf-8").write("\n".join(out))
print("done", len(out))
