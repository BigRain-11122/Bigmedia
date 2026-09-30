# -*- coding: utf-8 -*-
"""R659 addendum: append honest-correction log line (reading fix + op-red), refresh ts/task."""
import io, os, json, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
now = datetime.datetime.now()

ADDENDUM = (
    "2026-09-29 " + now.strftime("%H:%M") + " R659 轮末补记（读数更正+操作红如实入账·追加制原行不改写·R585/R651 补记先例）——"
    "①bm-a codex 批位相更正=主行「README staged+3」沿 R651 补记旧读数·轮末双 plumbing 复核定谳 git diff --cached=空"
    "（零 staged 件）+git diff worktree=README +3/city-humanities +14=**批实为 worktree 未暂存态**（R651 补记「staged 且 "
    "worktree==index」读数系伪·git status --short 控制台首列空格被吃显示层伪差在案）——让位判定不变（批未闭=+3/+14 同内容 "
    "04:06 mtime 未动·HEAD b8344d0 后零 commit）·下轮解除判据同；"
    "②操作红+根修（R585 三犯律同族·轮末 diff --stat 复核咬住）=r659_close.py 首版导出件重写犯两伤：results 历史误截 22→8 行"
    "（删 14 行 tick 史·自设 trim 假设无先例依据——历轮导出皆全量 append 零 trim）+indent=2 重排（HEAD 原格式=indent=1）"
    "→596 行伪 diff 揭伤·r659_fix.py 从 HEAD 重建：23 行全量历史恢复+原格式直写·终态 diff=10 行（export_ts+results 追加+"
    "OS 行三面即最小面）——**导出件重写律=add-only+格式随 HEAD**（state.json indent=2 与导出件 indent=1 各随其 HEAD 原格式·"
    "禁自设 trim/indent）；③r659_verify2 indent 检查项自身行序 bug（line[1]=export_ts 非 do）=检查器红非数据红·9/10 实质 "
    "PASS+diff --stat 终态实证为准。"
)

sp = os.path.join("src", "os", "state.json")
d = json.load(io.open(sp, encoding="utf-8"))
assert d["tick"] == 659
assert "R659:" in d["log"][-1][:40]
d["log"].append(ADDENDUM)
d["ts"] = now.strftime("%Y-%m-%d %H:%M:%S")
# task stays = main R659 line first 60 chars (addendum is append-only annotation)
io.open(sp, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))

# verify
d2 = json.load(io.open(sp, encoding="utf-8"))
e2 = json.load(io.open("docs/status-export.json", encoding="utf-8"))
ok = (
    d2["tick"] == 659
    and "轮末补记" in d2["log"][-1]
    and d2["log"][-2].startswith("2026-09-29") and "R659:" in d2["log"][-2][:40]
    and d2["task"].startswith("R659: declared-idle")
    and len(e2["results"]) == 23
)
out = io.open(os.path.join(".c3-tmp", "r659_verify3.txt"), "w", encoding="utf-8")
out.write("addendum_ok %s\nresults_n %d\nALL_PASS %s\n" % (ok, len(e2["results"]), ok))
out.close()
print("addendum_ok", ok)
sys.exit(0 if ok else 1)
