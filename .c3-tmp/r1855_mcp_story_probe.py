# r1855 explore#17 addendum: radar_get_story deep-read chain probe.
# Discovery: hot_topics output embeds "来龙去脉：radar_get_story，public_id=..."
# hooks -> story deep-read chain is the designed M0 deep-read path.
# Criterion: story call with a real public_id from hot_topics returns a
# readable story page with sources. ASCII-only per encoding law.
import json
import re
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:3101/api/mcp"
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


N = {"id": 30}
PID_RE = re.compile(r"public_id=([0-9a-f\-]{8,})")

# step 1: get hot topics to harvest a real public_id
post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-03-26", "capabilities": {},
    "clientInfo": {"name": "bigstream-explore17b", "version": "1.0"}}})
post({"jsonrpc": "2.0", "method": "notifications/initialized"})
hot = call_tool("radar_get_hot_topics", {})
pids = PID_RE.findall(hot["text"])
OUT["public_ids_found"] = pids
print("public_ids harvested:", pids[:3])

if pids:
    st = call_tool("radar_get_story", {"public_id": pids[0]})
    OUT["story"] = {"http_status": st["http_status"], "text_len": len(st["text"]),
                    "rpc_error": st["rpc_error"], "head": (st["text"] or "")[:500]}
    has_boundary = "\u4e0d\u53ef\u4fe1\u5916\u90e8\u8d44\u6599" in (st["text"] or "")
    OUT["story_trust_meta_boundary"] = has_boundary
    print("story ->", st["http_status"], "len", len(st["text"]), "boundary", has_boundary)
    print("story head:", OUT["story"]["head"][:300])
    OUT["verdict"] = "PASS" if (st["http_status"] == 200 and len(st["text"]) > 100) else "FAIL"
else:
    OUT["verdict"] = "SKIP_NO_PUBLIC_ID"

print("VERDICT:", OUT["verdict"])
with open(".c3-tmp/r1855_mcp_story_evidence.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1)
print("evidence written: .c3-tmp/r1855_mcp_story_evidence.json")
