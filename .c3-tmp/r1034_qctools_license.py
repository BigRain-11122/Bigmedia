import re, urllib.request
req = urllib.request.Request("https://raw.githubusercontent.com/bavc/qctools/master/License.html", headers={"User-Agent": "bs"})
t = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
text = re.sub(r"<[^>]+>", " ", t)
text = re.sub(r"\s+", " ", text)
hits = re.findall(r"(?i)(?:GPL|General Public|BSD|MIT|Apache|MPL|LGPL|Version [\d.]+)[^<]{0,90}", text)
out = ["HEAD: " + text[:300], "---HITS---"] + hits[:12]
open("r1034_qctools_license.txt", "w", encoding="utf-8").write("\n".join(out))
print("ok")
