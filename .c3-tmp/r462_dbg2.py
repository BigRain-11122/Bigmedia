# r462 debug2: reproduce edits in memory, show context around json error position
import io, json, importlib.util, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = ROOT + r"\src\os\state.json"

# load logline/focus/task from account script without executing its edits:
src = io.open(ROOT + r"\.c3-tmp\r462_account.py", encoding="utf-8").read()
ns = {}
# execute only the top part (imports + logline + focus_new definitions) up to the state.json marker
head = src.split("# ---------- state.json surgical edits ----------")[0]
exec(head, ns)
logline = ns["logline"]
focus_new = ns["focus_new"]
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

raw = io.open(SP, encoding="utf-8").read()

def sub1(text, old, new):
    n = text.count(old)
    assert n == 1, "anchor count=%d" % n
    return text.replace(old, new, 1)

raw = sub1(raw, '"tick": 461,', '"tick": 462,')

old_focus_prefix = '"focus": "R461: #59 REACT 09-28 热点窗届日领（M0 拋优→全链'[:20]
i = raw.index('"focus": "R461: #59 REACT 09-28')
j = raw.index('",', i)
raw = raw[:i] + '"focus": "' + focus_new + '",' + raw[j + 2:]

tail_anchor = '\n ],\n "ts": "2026-09-27 03:59:22",'
new_tail = ',\n  "' + logline + '",\n ],\n "ts": "' + ts + '",'
raw = sub1(raw, tail_anchor, new_tail)

old_task = '"task": "生产轮·#67 DIGEST 续件第五件《城市盘点 006·深夜决策批数字盘点》全链走门毕（R460 指针序首位领·cl"'
raw = sub1(raw, old_task, '"task": "x"')

out = io.open(ROOT + r"\.c3-tmp\r462_dbg2.txt", "w", encoding="utf-8")
try:
    json.loads(raw)
    out.write("VALID JSON\n")
except json.JSONDecodeError as e:
    out.write("ERR %s\n" % e)
    pos = e.pos
    out.write("CTX: ...%s...\n" % raw[pos - 120:pos + 120])
    # also quote-scan the logline
    out.write("dq_in_logline=%d\n" % logline.count('"'))
    out.write("bracket_comma_in_logline=%d\n" % logline.count("],"))
    out.write("logline_len=%d\n" % len(logline))
out.close()
print("done")
