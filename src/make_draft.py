# -*- coding: utf-8 -*-
"""BigStream draft scaffolder - M1/M3 station automation (production-chain.md).

Usage:
    python src/make_draft.py BS-002 mp                      # master (WeChat MP)
    python src/make_draft.py BS-002 shipinhao               # variant scaffold
    python src/make_draft.py BS-002 weibo --ver 2           # next version
    python src/make_draft.py BS-TEST-1 mp --out DIR          # test mode

Platform keys:
    mp          master (V2 full text, WeChat gongzhonghao)
    shipinhao douyin kuaishou tiktok     V1 voiceover 60s
    bilibili youtube                      V3 mid-video
    zhihu toutiao                         V2 same-source
    weibo xiaohongshu                     V4 social short

Laws enforced (CONSTITUTION / content-pipeline M1 / production-chain):
    naming : YYYYMMDD-<topic>-<platform label>-vN.md; an existing filename is
             refused (version law: open vN+1, never overwrite).
    gate   : state.json "production" == "paused" refuses scaffolding into
             data/drafts (CEO order O-20260923-1525-bm-a); the gate opens
             only by CEO order. Test mode (--out DIR) is always allowed.
    source : masters pre-fill their source list from the idea ledger row.
    lint   : generated skeletons are built to pass src/draft_lint.py
             (structure/gate/master-link/AIGC/sources checks).

Encoding rule: this source file is pure ASCII. All Chinese lives in UTF-8
data files (src/os/skeletons.md, docs/variant-templates.md, ideas ledger)
except the short platform-label escapes below.
"""
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DRAFTS = REPO / "data" / "drafts"
IDEAS = REPO / "data" / "ideas" / "ideas.md"
STATE = REPO / "src" / "os" / "state.json"
SKELETONS = REPO / "src" / "os" / "skeletons.md"
TEMPLATES = REPO / "docs" / "variant-templates.md"

# platform key -> (label, kind); labels as \uXXXX escapes (ASCII law)
PLATFORMS = {
    "mp": ("\u516c\u4f17\u53f7", "master"),
    "shipinhao": ("\u5fae\u4fe1\u89c6\u9891\u53f7", "v1"),
    "douyin": ("\u6296\u97f3", "v1"),
    "kuaishou": ("\u5feb\u624b", "v1"),
    "tiktok": ("TikTok", "v1"),
    "bilibili": ("B\u7ad9", "v3"),
    "youtube": ("YouTube", "v3"),
    "zhihu": ("\u77e5\u4e4e", "v2"),
    "toutiao": ("\u4eca\u65e5\u5934\u6761", "v2"),
    "weibo": ("\u65b0\u6d6a\u5fae\u535a", "v4"),
    "xiaohongshu": ("\u5c0f\u7ea2\u4e66", "v4"),
}


def read(p):
    return p.read_text(encoding="utf-8")


def die(msg, code=2):
    print("make_draft: %s" % msg)
    sys.exit(code)


def load_state():
    try:
        return json.loads(read(STATE))
    except Exception:
        return {}


def idea_row(topic):
    """Return (title, source) columns for a topic id from the ideas ledger."""
    for line in read(IDEAS).splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 7 and parts[1] == topic:
            return parts[4], parts[6]
    return None, None


def load_skeletons():
    """Parse named [block] sections from the skeleton data file."""
    out, cur = {}, None
    for line in read(SKELETONS).splitlines():
        m = re.match(r"^\[([a-z0-9-]+)\]\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() + "\n" for k, v in out.items()}


def spec_block(label):
    """Extract the platform spec block (S3) from docs/variant-templates.md."""
    lines = read(TEMPLATES).splitlines()
    out, hit = [], False
    for line in lines:
        if line.startswith("### "):
            if hit:
                break
            hit = line.find(label) >= 0
            if hit:
                out.append(line)
        elif hit:
            if line.startswith("## "):
                break
            out.append(line)
    return "\n".join(out).strip()


def main(argv):
    args, opts, i = [], {"ver": 1, "out": None}, 1
    while i < len(argv):
        a = argv[i]
        if a == "--ver":
            i += 1
            opts["ver"] = int(argv[i])
        elif a == "--out":
            i += 1
            opts["out"] = argv[i]
        else:
            args.append(a)
        i += 1
    if len(args) != 2:
        die("usage: make_draft.py TOPIC PLATFORM_KEY [--ver N] [--out DIR]")
    topic, key = args[0].upper(), args[1].lower()
    if key not in PLATFORMS:
        die("unknown platform key '%s' (known: %s)" % (key, " ".join(sorted(PLATFORMS))))
    label, kind = PLATFORMS[key]

    test = opts["out"] is not None
    state = load_state()
    if not test:
        if state.get("production") == "paused":
            die("production gate CLOSED (state.json production=paused, order "
                "O-20260923-1756-bm-a mode correction: no mass generation). "
                "Opening requires a CEO order. "
                "Test mode: add --out DIR.", 3)
        title, source = idea_row(topic)
        if not title:
            die("topic %s not found in the ideas ledger" % topic, 4)
        outdir = DRAFTS
    else:
        source = "(test placeholder)"
        outdir = Path(opts["out"])
        outdir.mkdir(parents=True, exist_ok=True)

    date = time.strftime("%Y%m%d")
    fname = "%s-%s-%s-v%d.md" % (date, topic, label, opts["ver"])
    path = outdir / fname
    if path.exists():
        die("refusing to overwrite %s (version law) - rerun with --ver %d"
            % (fname, opts["ver"] + 1), 5)

    sk = load_skeletons()
    if kind == "master":
        body = sk["master"]
    elif kind == "v1":
        body = sk["v1"]
    else:
        body = sk["v-generic"]
    master_ref = "%s-%s-%s-v1.md" % (date, topic, PLATFORMS["mp"][0])
    body = (body.replace("{DATE}", date).replace("{TOPIC}", topic)
                .replace("{PLATFORM}", label).replace("{VER}", str(opts["ver"]))
                .replace("{MASTER}", master_ref).replace("{SOURCE}", source or "(fill source)"))
    if kind != "master":
        spec = spec_block(label)
        body = body.replace("{SPEC_BLOCK}",
                            spec if spec else "(spec block not found in variant-templates.md)")
    path.write_text(body, encoding="utf-8")
    print("scaffold written: %s" % path)
    print("next: fill sections, then run src/draft_lint.py; GATE stays PENDING until M4.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
