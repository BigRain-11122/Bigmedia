# r512_edits4.py - amend this round's own log line (pre-commit) + station-reviews quote alignment
import io, json, os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"

def main():
    # 1. station-reviews quote alignment
    srp = os.path.join(ROOT, "docs", "reviews", "station-reviews.md")
    with io.open(srp, "r", encoding="utf-8") as fh:
        t = fh.read()
    old = "renders 行升「成品·#79 件1 D15 落位」"
    new = "renders 行升「成品·落位（#79 件1 D15）」"
    assert t.count(old) == 1, "station-reviews anchor %d" % t.count(old)
    t = t.replace(old, new)
    with io.open(srp, "w", encoding="utf-8") as fh:
        fh.write(t)

    # 2. state.json own log line amendments (2 replaces)
    stp = os.path.join(ROOT, "src", "os", "state.json")
    st = json.load(io.open(stp, encoding="utf-8"))
    ln = st["log"][-1]
    assert "R512: 生产轮·#79 件1 收口毕" in ln, "last log line is not R512"
    a = ln.count("renders 行升「成品·#79 件1 D15 落位」")
    ln = ln.replace("renders 行升「成品·#79 件1 D15 落位」", "renders 行升「成品·落位（#79 件1 D15）」")
    b = "readiness 3 阻塞皆外部 CEO 面+2 发现轮内双清复跑核实（render-unannot lc-001=升成品标清+render-stale=尾注修红清）"
    c = ("readiness 3 阻塞皆外部 CEO 面 0 发现（首跑 2 发现轮内双清三跑核实：render-unannot lc-001=**第五合法态注册**〔readiness PRODUCT_SLOT_MARK「成品·落位」新增+夹具+测例·R189 SUPERSEDED/R252 DISPOSED 同型·298 全回归绿〕+render-stale=尾注无扩展名写法修红〔R147 先例〕）")
    assert ln.count(b) == 1, "probe-segment anchor %d" % ln.count(b)
    ln = ln.replace(b, c)
    st["log"][-1] = ln
    with io.open(stp, "w", encoding="utf-8") as fh:
        json.dump(st, fh, ensure_ascii=False, indent=1)
    print("AMEND OK a=%d" % a)

if __name__ == "__main__":
    main()
