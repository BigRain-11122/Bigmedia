# R301 em-budget pre-check for MC-20260925-CENSUS-v11 (C-00020 Su Zihan) using renderer's own _em_cost.
# ASCII-only console output (encoding law). Machine truth = render_card_video._em_cost.
import importlib.util

spec = importlib.util.spec_from_file_location("rcv", r"src\render\render_card_video.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

BUDGET_PX = 1080 - 160  # side margins 80+80 (R293/R294 convention)

lines = {
    "h1": (84, "城市图鉴 011"),
    "f1": (40, "C-00020 · 苏梓涵"),
    "f2": (40, "碳基市民 · 原生代 · 女 · 24 岁"),
    "f3": (40, "GAME 城 · 游戏楼街区 · 关卡建筑师"),
    "f4": (40, "信条：「每个转角都该藏一个惊喜。」"),
    "f5": (40, "点子多 · 会折腾 · 记性好"),
    "f6": (40, "全城唯一给「夜班人员」留专属彩蛋的关卡建筑师"),
    "subs": (38, "基于硅基城市居民户籍卡档案（展示锚 C-00020）"),
}
for k, (size, s) in lines.items():
    em = sum(m._em_cost(c) for c in s)
    budget = BUDGET_PX / size
    ok = "OK" if em <= budget else "FAIL"
    # full-width glyph count for the log convention
    fw = sum(1 for c in s if ord(c) >= 0x2E80)
    print("%s size=%d em=%.2f budget=%.2f margin=%.2f fw_glyphs=%d %s" % (k, size, em, budget, budget - em, fw, ok))
# h2_size 44 exclusion test for binding line (hook line drives size choice)
hook = lines["f6"][1]
em44 = sum(m._em_cost(c) for c in hook)
print("h2_size44 hook em=%.2f budget=%.2f excl=%s" % (em44, BUDGET_PX / 44, "YES" if em44 > BUDGET_PX / 44 else "no"))
