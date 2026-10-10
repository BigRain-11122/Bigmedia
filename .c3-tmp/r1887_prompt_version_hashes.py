"""R1887: compute promptVersion hashes exactly as prompts.ts does.

prompts.ts: promptVersion(name) -> sha256(f"{n}\n{raw(n)}\n" for used files sorted).hex[:10]
Used files = the file itself plus any {{> include}} files. City prefilter and
city selection-score have no includes; industry versions need a check.
"""
import hashlib
import re
import os

DIR = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\assets\aihot-poc\AIHOT\industry\prompts"
INCLUDE = re.compile(r"\{\{>\s*([A-Za-z][\w.-]*)\s*\}\}")


def raw_text(name):
    with open(os.path.join(DIR, name + ".md"), encoding="utf-8") as f:
        return f.read()


def used_files(name, seen=None):
    seen = seen or []
    if name in seen:
        raise ValueError("cycle")
    text = raw_text(name)
    out = [name]
    for m in INCLUDE.finditer(text):
        out.extend(used_files(m.group(1), seen + [name]))
    return out


def version_hash(*names):
    used = sorted(set(n for nm in names for n in used_files(nm)))
    h = hashlib.sha256()
    for n in used:
        h.update(f"{n}\n{raw_text(n)}\n".encode("utf-8"))
    return h.hexdigest()[:10], used


for name in ["prefilter", "selection-score", "prefilter-city", "prefilter-industry-bak-r1886",
             "selection-score-city", "selection-score-industry-bak-r1887"]:
    vh, used = version_hash(name)
    print(f"{name:40s} -> {name}@{vh}  used={used}")
