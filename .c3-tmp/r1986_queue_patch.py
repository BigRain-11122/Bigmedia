# r1986: append tech#106 seed + main.md row 17 progress note
# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

TECH_SEED = u"106. [R1986 补货·本轮 fire 卡真发现] MV 文件面静默×硬件忙长尾态的火窗解锁判读面评估（缺口锚=R1986 实锚：fire 卡 16:35:51 读数=mv-probe quiet 154.6min〔文件面已静 2.5h+〕×gate util worst-case 100>80 仍占〔ComfyUI python 在渲〕×VRAM 面已翻 GO〔free 4983 过 2048·credit effective_free 9859〕=三面读数互相分叉态——现行「mv-active=CEO 优先线在执」归因对 quiet>120min 长尾窗渐失解释力〔文件面静默只证 git 可见域无新落·不证渲染波结束〕且无「渲染波 wedged 卡死」对极判据〔10-10 ollama wedged 槽位同型风险：波若真死·fire 窗将被无限占而不自知〕）——候选=mv_sprint_probe 或 fire 卡归因面增 ComfyUI 侧活度读数〔8188 /queue 长度+output 目录 newest mtime age+python 进程 CPU 时间增量三选一或组合·跨仓只读·零写接触〕：波真在渲=活度读数新鲜维持让路·波 wedged=读数陈旧触发「stale-render」注记〔判断位注记面·零闸·tech#79 归因族同型〕；判据=下个 fire 窗前后双读数对照〔活度读数与 gate util 翻 GO 时序一致=面成立·分叉=wedged 候查入账〕+hermetic 零动存量调用面·判负留痕合法）——按认领制随轮领做（CPU 面·判断位注记级零闸）"

MAIN_NOTE_OLD = u"——余腿 gated GPU fire 窗：M4.5 七席（Ollama）+E4 参考仪（e4-material 件=fire 窗前 CPU 顺手步预载·R1875 范式）+F-179 登记"
MAIN_NOTE_NEW = u"——余腿 gated GPU fire 窗：M4.5 七席（Ollama）+E4 参考仪（**[R1986 e4-material 预载毕 2026-10-11]**：四段式材料件 e4-material.md 落 tmp〔v17 同型·平台形态/完整描述/世界背景/本卡内容〕·机检 7/7 verbatim+AIGC 角标+底部声明行全在位〔r1986_e4mat_check.py〕·「六项整改」口径修正=第六项即剧本四律重写防 5+1 误读）+F-179 登记"

def main():
    # tech.md append (anchor = tail line is #105, append after it)
    p = 'state/queue/tech.md'
    t = io.open(p, encoding='utf-8').read()
    assert t.rstrip('\n').splitlines()[-1].startswith('105.'), 'tech.md tail anchor drift'
    assert '106.' not in t.splitlines()[-1], 'seed already appended'
    t = t.rstrip('\n') + '\n' + TECH_SEED + '\n'
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    print('tech.md: seed 106 appended, len=', len(t))

    # main.md row 17 progress note
    p2 = 'state/queue/main.md'
    t2 = io.open(p2, encoding='utf-8').read()
    assert MAIN_NOTE_OLD in t2, 'main.md row-17 anchor drift'
    assert MAIN_NOTE_NEW not in t2, 'main.md note already applied'
    t2 = t2.replace(MAIN_NOTE_OLD, MAIN_NOTE_NEW, 1)
    io.open(p2, 'w', encoding='utf-8', newline='').write(t2)
    print('main.md: row 17 note applied, len=', len(t2))

if __name__ == '__main__':
    main()
