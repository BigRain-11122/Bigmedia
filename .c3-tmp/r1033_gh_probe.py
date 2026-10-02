# -*- coding: utf-8 -*-
# R1033 OSS slice-2 external probes (GitHub API, A-level, read-only).
import json, urllib.request

def gh(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "bigstream-oss-harvest", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

out = []
# Knife 1: adopted candidate upstream health/license read
try:
    d = gh("https://api.github.com/repos/fonttools/fonttools")
    out.append("K1 fonttools/fonttools: license=%s stars=%s forks=%s open_issues=%s pushed_at=%s archived=%s lang=%s desc=%r" % (
        (d.get("license") or {}).get("spdx_id"), d.get("stargazers_count"),
        d.get("forks_count"), d.get("open_issues_count"), d.get("pushed_at"),
        d.get("archived"), d.get("language"), (d.get("description") or "")[:100]))
except Exception as e:
    out.append("K1 fonttools/fonttools: ERROR %r" % e)

# Knife 2: purpose-built glyph-coverage / tofu-detection tools search
try:
    s = gh("https://api.github.com/search/repositories?q=font+glyph+coverage+check&sort=stars&order=desc&per_page=5")
    out.append("K2 search 'font glyph coverage check': total=%s" % s.get("total_count"))
    for it in s.get("items", [])[:5]:
        out.append("  - %s | %s | stars=%s | push=%s | %r" % (
            it["full_name"], (it.get("license") or {}).get("spdx_id"),
            it["stargazers_count"], it.get("pushed_at"),
            (it.get("description") or "")[:90]))
except Exception as e:
    out.append("K2 search: ERROR %r" % e)

# Knife 2b: subtitle tofu face search (closest domain tool)
try:
    s = gh("https://api.github.com/search/repositories?q=subtitle+missing+glyph+tofu&sort=stars&order=desc&per_page=5")
    out.append("K2b search 'subtitle missing glyph tofu': total=%s" % s.get("total_count"))
    for it in s.get("items", [])[:5]:
        out.append("  - %s | %s | stars=%s | push=%s | %r" % (
            it["full_name"], (it.get("license") or {}).get("spdx_id"),
            it["stargazers_count"], it.get("pushed_at"),
            (it.get("description") or "")[:90]))
except Exception as e:
    out.append("K2b search: ERROR %r" % e)

open(r".c3-tmp\r1033_gh_probes.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
