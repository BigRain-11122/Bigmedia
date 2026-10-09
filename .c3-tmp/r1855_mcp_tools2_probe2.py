# r1855 explore#17 v2: markdown-aware second-batch tool readings.
# v1 lesson: MCP tools return markdown renderings (same as R1853 daily);
# search param is `q` (2-200), not keyword/limit.
# Criterion: hot_topics ranked structure (rank 1..N, N<=10) succeeds +
# latest both windows return readable briefings + search returns results.
# Cross-check: hot_topics markdown titles vs /api/v1/hot-topics top titles.
# ASCII-only per encoding law.
import json
import re
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:3101/api/mcp"
V1_HOT = "http://127.0.0.1:3101/api/v1/hot-topics"
OUT = {}
session_id = None


def post(payload, timeout=30):
    global session_id
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status = r.status
            ctype = r.headers.get("Content-Type", "")
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        status = e.code
        ctype = e.headers.get("Content-Type", "") if e.headers else ""
        body = e.read().decode("utf-8", "replace")
    except Exception as e:
        return {"http_error": repr(e)}
    parsed = None
    if "text/event-stream" in ctype:
        for line in body.splitlines():
            ls = line.strip()
            if ls.startswith("data:"):
                try:
                    parsed = json.loads(ls[5:].strip())
                except Exception:
                    pass
    else:
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = None
    return {"http_status": status, "content_type": ctype, "parsed": parsed,
            "raw_len": len(body)}


def call_tool(name, args):
    res = post({"jsonrpc": "2.0", "id": N["id"], "method": "tools/call",
                "params": {"name": name, "arguments": args}})
    N["id"] += 1
    content = (res.get("parsed") or {}).get("result", {}).get("content", [])
    text_all = "\n".join((c.get("text") or "") for c in content
                         if c.get("type") == "text")
    err = (res.get("parsed") or {}).get("error")
    return {"http_status": res.get("http_status"), "text": text_all,
            "rpc_error": err}


N = {"id": 20}
RANK_RE = re.compile(r"^\u7b2c\s*(\d+)\s*\u540d\uff1a\s*\[([^\]]+)\]")


def parse_ranked_md(text):
    ranks = []
    for line in text.splitlines():
        m = RANK_RE.match(line.strip())
        if m:
            ranks.append((int(m.group(1)), m.group(2)))
    return ranks


def count_brief_rows(text):
    rows = 0
    for line in text.splitlines():
        ls = line.strip()
        if ls.startswith(("- ", "* ", "### ")) or RANK_RE.match(ls):
            rows += 1
    return rows


# --- step 1: handshake ---
init_payload = {
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "bigstream-explore17", "version": "1.1"},
    },
}
res1 = post(init_payload)
OUT["initialize_http"] = res1.get("http_status")
OUT["server_info"] = ((res1.get("parsed") or {}).get("result") or {}).get("serverInfo")
post({"jsonrpc": "2.0", "method": "notifications/initialized"})
print("initialize:", OUT["initialize_http"], "server:", OUT["server_info"])

# --- step 2: tools/list (count + names) ---
res3 = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
tools = (res3.get("parsed") or {}).get("result", {}).get("tools", [])
OUT["tool_count"] = len(tools)
OUT["tool_names"] = [t.get("name") for t in tools]
print("tools:", OUT["tool_names"])

# --- step 3: radar_get_hot_topics default (limit=10) ---
hot = call_tool("radar_get_hot_topics", {})
OUT["hot_topics"] = {"http_status": hot["http_status"], "text_len": len(hot["text"])}
ranks = parse_ranked_md(hot["text"])
OUT["hot_rank_list"] = ranks
OUT["hot_rank_count"] = len(ranks)
OUT["hot_ranks_sorted_ok"] = bool(ranks and [r for r, _ in ranks] == sorted(r for r, _ in ranks) and ranks[0][0] == 1)
print("hot_topics ranks:", [(r, t[:30]) for r, t in ranks])

# --- step 3b: limit=3 probe (schema max 10, min 1) ---
hot3 = call_tool("radar_get_hot_topics", {"limit": 3})
ranks3 = parse_ranked_md(hot3["text"])
OUT["hot_limit3_count"] = len(ranks3)
print("hot limit=3 ranks:", len(ranks3))

# --- step 4: radar_get_latest both windows ---
latest = {}
for w in ("24h", "7d"):
    lr = call_tool("radar_get_latest", {"window": w})
    rows = count_brief_rows(lr["text"])
    latest[w] = {"http_status": lr["http_status"], "text_len": len(lr["text"]),
                 "row_count": rows, "head": (lr["text"] or "")[:200]}
    print("latest", w, "->", lr["http_status"], "len", len(lr["text"]), "rows", rows)
OUT["latest"] = latest
OUT["latest_windows_ok"] = bool(latest["24h"]["http_status"] == 200 and latest["7d"]["http_status"] == 200 and latest["24h"]["text_len"] > 0 and latest["7d"]["text_len"] > 0)

# --- step 5: radar_search with correct arg `q` ---
sr = call_tool("radar_search", {"q": "AI"})
OUT["search_default"] = {"http_status": sr["http_status"], "text_len": len(sr["text"]),
                         "rows": count_brief_rows(sr["text"]),
                         "head": (sr["text"] or "")[:250]}
print("search q=AI ->", sr["http_status"], "len", len(sr["text"]))
print("search head:", OUT["search_default"]["head"][:200])

# --- step 6: cross-read v1 hot-topics titles vs MCP markdown titles ---
v1_titles = []
try:
    with urllib.request.urlopen(V1_HOT, timeout=15) as r:
        OUT["v1_http"] = r.status
        v1 = json.loads(r.read().decode("utf-8", "replace"))
    src = v1 if isinstance(v1, list) else None
    if src is None and isinstance(v1, dict):
        for key in ("hotTopics", "topics", "items", "data"):
            if isinstance(v1.get(key), list):
                src = v1[key]
                break
    if src:
        for x in src[:10]:
            if isinstance(x, dict) and x.get("title"):
                v1_titles.append(x["title"])
except Exception as e:
    OUT["v1_http"] = repr(e)
OUT["v1_top_titles"] = v1_titles
mcp_titles = [t for _, t in ranks]
overlap = sum(1 for t in v1_titles[:5] if t in mcp_titles)
OUT["cross_overlap_top5"] = overlap
OUT["cross_v1_count"] = len(v1_titles)
print("v1 titles:", len(v1_titles), "| mcp titles:", len(mcp_titles), "| overlap top5:", overlap)

# --- verdict ---
c1 = bool(ranks and ranks[0][0] == 1 and OUT["hot_rank_count"] >= 1
          and OUT["hot_ranks_sorted_ok"])
c2 = OUT["latest_windows_ok"]
c3 = bool(sr["http_status"] == 200 and len(sr["text"]) > 0)
OUT["verdict_detail"] = {
    "c1_hot_topics_ranked_structure": c1,
    "hot_rank_count_today": OUT["hot_rank_count"],
    "hot_limit3_count": OUT["hot_limit3_count"],
    "c2_latest_both_windows_readable": c2,
    "c3_search_readable": c3,
    "cross_overlap_top5": overlap,
    "supply_note": "today coalesced N=9 topics (schema cap 10) - supply-side, not tool-side",
}
OUT["verdict"] = "PASS" if (c1 and c2 and c3) else "FAIL"
print("VERDICT:", OUT["verdict"], json.dumps(OUT["verdict_detail"], ensure_ascii=False))

with open(".c3-tmp/r1855_mcp_tools2_criterion.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1)
print("criterion written: .c3-tmp/r1855_mcp_tools2_criterion.json")
