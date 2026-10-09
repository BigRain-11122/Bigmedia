# r1853b explore#15 criterion closure: cross-check MCP daily text vs v1 API lead field
# ASCII-only per encoding law.
import json
import re
import urllib.request

with open(".c3-tmp/r1853_mcp_evidence.json", encoding="utf-8") as f:
    ev = json.load(f)

mcp_text = None
# re-run the tools/call inside this script is not needed; evidence holds only meta.
# Rebuild the text by calling again (stateless server, cheap):
BASE = "http://127.0.0.1:3101/api/mcp"
H = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}


def post(payload, timeout=25):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE, data=data, headers=H, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read().decode("utf-8", "replace")
        if "text/event-stream" in (r.headers.get("Content-Type") or ""):
            parsed = None
            for line in body.splitlines():
                ls = line.strip()
                if ls.startswith("data:"):
                    try:
                        parsed = json.loads(ls[5:].strip())
                    except Exception:
                        pass
            return parsed
        return json.loads(body) if body.strip() else None


post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-03-26", "capabilities": {},
    "clientInfo": {"name": "bigstream-explore15b", "version": "1.0"}}})
post({"jsonrpc": "2.0", "method": "notifications/initialized"})
res = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": "radar_get_daily", "arguments": {}}})
content = (res or {}).get("result", {}).get("content", [])
mcp_text = "\n".join(c.get("text") or "" for c in content if c.get("type") == "text")

with urllib.request.urlopen("http://127.0.0.1:3101/api/v1/dailies/latest", timeout=15) as r:
    api = json.loads(r.read().decode("utf-8", "replace"))

report = api.get("report") or api
lead = report.get("lead")
print("API report.lead (JSON field):")
print(json.dumps(lead, ensure_ascii=False, indent=1))

# lead field per API schema = object with headline lines; extract plain strings
def strings_of(x):
    out = []
    if isinstance(x, str):
        out.append(x)
    elif isinstance(x, dict):
        for v in x.values():
            out.extend(strings_of(v))
    elif isinstance(x, list):
        for v in x:
            out.extend(strings_of(v))
    return out


lead_strs = [s for s in strings_of(lead) if s.strip()]
mcp_head = None
for line in mcp_text.splitlines():
    if "头条" in line:
        mcp_head = line.strip()
        break

hits = [(s, s.strip() in mcp_text) for s in lead_strs]
print("MCP daily text len:", len(mcp_text))
for s, ok in hits:
    print("lead-part-in-mcp:", ok, "|", s[:80])
print("MCP headline line:", mcp_head[:160] if mcp_head else "(none)")

criterion = all(ok for _, ok in hits) and len(lead_strs) > 0
verdict = {
    "criterion": "daily report lead field read via MCP (content-level)",
    "api_lead_field": lead,
    "mcp_text_len": len(mcp_text),
    "mcp_headline_line": mcp_head,
    "lead_parts_all_in_mcp_text": criterion,
    "verdict": "PASS" if criterion else "FAIL",
}
with open(".c3-tmp/r1853_mcp_criterion.json", "w", encoding="utf-8") as f:
    json.dump(verdict, f, ensure_ascii=False, indent=1)
print("CRITERION VERDICT:", verdict["verdict"])
