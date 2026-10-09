# r1853 explore#15: MCP handshake + tool list + daily-report call probe
# Target: AIHOT radar /api/mcp (Streamable HTTP, anonymous, read-only, stateless)
# ASCII-only per encoding law.
import json
import sys
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:3101/api/mcp"
OUT = {}
session_id = None


def post(payload, timeout=20):
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
            sid = r.headers.get("Mcp-Session-Id")
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        status = e.code
        ctype = e.headers.get("Content-Type", "") if e.headers else ""
        sid = e.headers.get("Mcp-Session-Id") if e.headers else None
        body = e.read().decode("utf-8", "replace")
    except Exception as e:
        return {"http_error": repr(e)}
    if sid:
        session_id = sid
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
    return {"http_status": status, "content_type": ctype, "session_id": sid,
            "raw_len": len(body), "parsed": parsed}


def summarize(res, keys=("protocolVersion", "serverInfo", "instructions")):
    p = res.get("parsed") or {}
    if "error" in p:
        return {"jsonrpc_error": p["error"]}
    r = p.get("result", p)
    out = {}
    for k in keys:
        if k in r:
            out[k] = r[k]
    if "tools" in r:
        out["tools"] = [
            {"name": t.get("name"), "desc": (t.get("description") or "")[:120]}
            for t in r["tools"]
        ]
    return out or {"raw_excerpt": json.dumps(p, ensure_ascii=False)[:400]}


print("=== step 1 initialize ===")
init_payload = {
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "bigstream-explore15", "version": "1.0"},
    },
}
res1 = post(init_payload)
OUT["initialize"] = res1
print("http:", res1.get("http_status"), "ctype:", res1.get("content_type"),
      "session:", res1.get("session_id"))
print("result:", json.dumps(summarize(res1), ensure_ascii=False, indent=1)[:900])

print("=== step 2 notifications/initialized ===")
res2 = post({"jsonrpc": "2.0", "method": "notifications/initialized"})
OUT["initialized_notification"] = {k: res2.get(k) for k in ("http_status", "raw_len")}
print("http:", res2.get("http_status"), "raw_len:", res2.get("raw_len"))

print("=== step 3 tools/list ===")
res3 = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
OUT["tools_list"] = res3
tools = (res3.get("parsed") or {}).get("result", {}).get("tools", [])
print("tool_count:", len(tools))
for t in tools:
    print("-", t.get("name"), "|", (t.get("description") or "")[:110])

print("=== step 4 tools/call daily report ===")
lead_hit = None
daily_tool = None
for t in tools:
    n = (t.get("name") or "").lower()
    if "daily" in n or "report" in n:
        daily_tool = t.get("name")
        break
if not daily_tool and tools:
    daily_tool = tools[0].get("name")
OUT["chosen_tool"] = daily_tool
print("chosen tool:", daily_tool)
if daily_tool:
    args = {}
    schema = (t.get("inputSchema") or {}) if tools else {}
    res4 = post({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                 "params": {"name": daily_tool, "arguments": args}}, timeout=30)
    OUT["tools_call"] = {k: res4.get(k) for k in ("http_status", "content_type")}
    content = (res4.get("parsed") or {}).get("result", {}).get("content", [])
    text_all = "\n".join((c.get("text") or "") for c in content
                         if c.get("type") == "text")
    OUT["call_text_len"] = len(text_all)
    print("call http:", res4.get("http_status"), "text_len:", len(text_all))
    # judging criterion: read the daily report "lead" field through MCP
    lead = None
    try:
        obj = json.loads(text_all)
        rep = obj.get("report") or obj
        lead = rep.get("lead")
    except Exception:
        for line in text_all.splitlines():
            if '"lead"' in line:
                lead = line.strip()[:200]
                break
    OUT["lead_field"] = lead
    print("LEAD:", json.dumps(lead, ensure_ascii=False)[:300] if lead else "(not found)")
    print("TEXT_HEAD:", text_all[:500])

with open(".c3-tmp/r1853_mcp_evidence.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1)
print("=== evidence written: .c3-tmp/r1853_mcp_evidence.json ===")
verdict = "PASS" if OUT.get("lead_field") else "FAIL"
print("VERDICT:", verdict, "(criterion: daily report lead field read via MCP)")
