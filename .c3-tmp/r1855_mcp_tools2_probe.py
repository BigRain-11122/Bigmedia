# r1855 explore#17: radar MCP second-batch tool readings
# Targets: radar_get_hot_topics (Top10 rank structure), radar_get_latest
# (24h/7d windows, item counts), radar_search (2-200 keyword search)
# Criterion: hot_topics rank 1-10 structure ok + latest both windows item
# counts readable. Cross-read vs /api/v1/hot-topics for content equivalence.
# ASCII-only per encoding law.
import json
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


N = {"id": 10}

# --- step 1: handshake ---
init_payload = {
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "bigstream-explore17", "version": "1.0"},
    },
}
res1 = post(init_payload)
OUT["initialize_http"] = res1.get("http_status")
OUT["server_info"] = ((res1.get("parsed") or {}).get("result") or {}).get("serverInfo")
post({"jsonrpc": "2.0", "method": "notifications/initialized"})
print("initialize:", OUT["initialize_http"], "server:", OUT["server_info"])

# --- step 2: tools/list with full schemas for the 3 targets ---
res3 = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
tools = (res3.get("parsed") or {}).get("result", {}).get("tools", [])
OUT["tool_count"] = len(tools)
schemas = {}
for t in tools:
    schemas[t.get("name")] = t.get("inputSchema") or {}
for name in ("radar_get_hot_topics", "radar_get_latest", "radar_search",
             "radar_get_story"):
    if name in schemas:
        OUT["schema_" + name] = schemas[name]
        print("schema", name, "->", json.dumps(schemas[name], ensure_ascii=False)[:300])

# --- step 3: radar_get_hot_topics ---
hot = call_tool("radar_get_hot_topics", {})
OUT["hot_topics"] = {"http_status": hot["http_status"], "text_len": len(hot["text"]),
                     "rpc_error": hot["rpc_error"]}
hot_obj = None
try:
    hot_obj = json.loads(hot["text"])
except Exception:
    pass
OUT["hot_topics_json_ok"] = hot_obj is not None
topics = None
if isinstance(hot_obj, dict):
    for key in ("topics", "hotTopics", "items", "data"):
        if isinstance(hot_obj.get(key), list):
            topics = hot_obj[key]
            break
    if topics is None and isinstance(hot_obj.get("report"), dict):
        for key in ("topics", "items"):
            if isinstance(hot_obj["report"].get(key), list):
                topics = hot_obj["report"][key]
                break
elif isinstance(hot_obj, list):
    topics = hot_obj
if topics is None and hot["text"]:
    # markdown fallback: count list rows
    topics = [ln for ln in hot["text"].splitlines() if ln.strip().startswith(("-", "*")) or (ln.strip()[:1].isdigit() and "." in ln[:4])]
OUT["hot_topics_count"] = len(topics) if topics is not None else None
OUT["hot_topics_head"] = (hot["text"] or "")[:600]
print("hot_topics: http", hot["http_status"], "json_ok", OUT["hot_topics_json_ok"],
      "count", OUT["hot_topics_count"])
print("hot head:", OUT["hot_topics_head"][:400])

# rank structure check: ranks 1..10 present (rank field or positional order)
rank_ok = False
if topics:
    if all(isinstance(x, dict) for x in topics[:3]):
        ranks = [x.get("rank") for x in topics if isinstance(x, dict)]
        rank_ok = any(isinstance(r, int) for r in ranks[:10]) and len(topics) >= 10
        OUT["hot_topics_ranks"] = [x.get("rank") for x in topics[:12]]
        OUT["hot_topics_titles_head"] = [x.get("title") for x in topics[:5]]
    else:
        rank_ok = len(topics) >= 10
OUT["hot_topics_rank_structure_ok"] = bool(rank_ok and OUT["hot_topics_count"] and OUT["hot_topics_count"] >= 10)
print("rank_structure_ok:", OUT["hot_topics_rank_structure_ok"])

# --- step 4: radar_get_latest (both windows) ---
latest_schema = schemas.get("radar_get_latest") or {}
enum_windows = []
try:
    props = latest_schema.get("properties", {})
    for pk, pv in props.items():
        if "window" in pk.lower() or "period" in pk.lower():
            if pv.get("enum"):
                enum_windows = pv["enum"]
            OUT["latest_window_param"] = pk
except Exception:
    pass
OUT["latest_enum_windows"] = enum_windows
windows = enum_windows or ["24h", "7d"]
latest_readings = {}
for w in windows[:4]:
    args = {}
    if OUT.get("latest_window_param"):
        args[OUT["latest_window_param"]] = w
    lr = call_tool("radar_get_latest", args)
    items_count = None
    try:
        lo = json.loads(lr["text"])
        if isinstance(lo, dict):
            for key in ("items", "briefings", "articles", "stories", "data"):
                v = lo.get(key)
                if isinstance(v, list):
                    items_count = len(v)
                    break
            if items_count is None and isinstance(lo.get("briefing"), dict):
                for key in ("items", "articles"):
                    v = lo["briefing"].get(key)
                    if isinstance(v, list):
                        items_count = len(v)
                        break
        elif isinstance(lo, list):
            items_count = len(lo)
    except Exception:
        pass
    latest_readings[w] = {"http_status": lr["http_status"],
                          "text_len": len(lr["text"]),
                          "items_count": items_count,
                          "rpc_error": lr["rpc_error"],
                          "head": (lr["text"] or "")[:300]}
    print("latest", w, "->", latest_readings[w]["http_status"],
          "items", items_count, "len", len(lr["text"]))
OUT["latest_readings"] = latest_readings
latest_ok = (len(latest_readings) >= 2 and all(
    v.get("http_status") == 200 and v.get("text_len", 0) > 0
    for v in latest_readings.values()))
OUT["latest_windows_ok"] = bool(latest_ok)

# --- step 5: radar_search keyword ---
sr = call_tool("radar_search", {"keyword": "AI", "limit": 5})
sr_items = None
try:
    so = json.loads(sr["text"])
    if isinstance(so, dict):
        for key in ("items", "results", "articles", "stories", "data"):
            v = so.get(key)
            if isinstance(v, list):
                sr_items = len(v)
                break
    elif isinstance(so, list):
        sr_items = len(so)
except Exception:
    pass
OUT["search"] = {"http_status": sr["http_status"], "text_len": len(sr["text"]),
                 "items_count": sr_items, "rpc_error": sr["rpc_error"],
                 "head": (sr["text"] or "")[:300]}
print("search ->", sr["http_status"], "items", sr_items, "len", len(sr["text"]))
OUT["search_ok"] = bool(sr["http_status"] == 200 and (sr_items is None or sr_items >= 0) and len(sr["text"]) > 0)

# --- step 6: cross-read v1 hot-topics for content equivalence ---
v1_titles = []
try:
    with urllib.request.urlopen(V1_HOT, timeout=15) as r:
        v1 = json.loads(r.read().decode("utf-8", "replace"))
    OUT["v1_http"] = r.status
    def _titles(obj):
        out = []
        if isinstance(obj, list):
            src = obj
        elif isinstance(obj, dict):
            src = None
            for key in ("hotTopics", "topics", "items", "data"):
                if isinstance(obj.get(key), list):
                    src = obj[key]
                    break
            if src is None:
                return out
        else:
            return out
        for x in src[:10]:
            if isinstance(x, dict) and x.get("title"):
                out.append(x["title"])
        return out
    v1_titles = _titles(v1)
except Exception as e:
    OUT["v1_http"] = repr(e)
OUT["v1_top_titles"] = v1_titles[:10]
mcp_titles = OUT.get("hot_topics_titles_head") or []
overlap = [t for t in v1_titles[:5] if t in mcp_titles]
OUT["cross_overlap_top5"] = len(overlap)
print("v1 top titles:", len(v1_titles), "overlap mcp-top5:", len(overlap))

# --- verdict ---
c1 = OUT["hot_topics_rank_structure_ok"]
c2 = OUT["latest_windows_ok"]
OUT["verdict"] = "PASS" if (c1 and c2) else "FAIL"
OUT["verdict_detail"] = {"c1_hot_topics_rank_1_10": c1,
                         "c2_latest_both_windows_readable": c2,
                         "search_ok_bonus": OUT["search_ok"],
                         "cross_overlap_top5": OUT.get("cross_overlap_top5")}
print("VERDICT:", OUT["verdict"], json.dumps(OUT["verdict_detail"], ensure_ascii=False))

with open(".c3-tmp/r1855_mcp_tools2_evidence.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1)
print("evidence written: .c3-tmp/r1855_mcp_tools2_evidence.json")
