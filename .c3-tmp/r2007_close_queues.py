# r2007 close helper: mark main#18 done + append main#19 + tech#116 replenishment
import io, sys

MAIN = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\state\queue\main.md'
TECH = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\state\queue\tech.md'

def rw(path, transform):
    with io.open(path, 'r', encoding='utf-8') as f:
        t = f.read()
    t2 = transform(t)
    if t2 is None:
        print('ANCHOR-NOT-FOUND:', path)
        sys.exit(1)
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(t2)
    print('OK:', path)

def main_xform(t):
    old = '——可即领（CPU 面·无 GPU 依赖·10-12 窗三件〔tech#92 权威窗/W42 周审/REACT-v15〕后位候选）'
    if old not in t:
        return None
    done_note = ('\n——**[done 2026-10-11 R2007]** 升格回评执行毕（B 池两锚逐锚复跑·尾带基锚 8.0x5→6.0→7.0 诚实并读）：'
                 'C-00012 沈佩兰升 A（选型件 §7 v1.2·题眼级信条「队形不能乱，人心更不能散」+口令/沪语声音原生+烟火 register=8.0 performer 族同带）'
                 '→SC-005-07 三件套预置毕（41 锚 GREEN rc0+inclusion 13/13+leak 零命中+M1 0F9W·fire-ready 结转·F-180 预指·生产链行=main#19）；'
                 'C-00023 潘志明维持 B 判负留痕（制度 register=尾带弱读数族风险面·场强次一档·重开条件=SC-005-07 E4 ≥8.0 或新跨卡资产·判据预注册 sources 件）')
    t = t.replace(old, old + done_note, 1)
    # replenishment: main#19 production line row
    if not t.endswith('\n'):
        t += '\n'
    t += ('\n19. [R2007 补货] SC-005-07《城市口述史·选段七·晨操领队沈佩兰》生产链（main#18 升 A 定谳件·二季首件·F-180 预指）——'
          '拍稿三件套 fire-ready 结转（beats 41 锚 GREEN+sources+s1-material 在 git·R1968/R1970/R1972 预置范式）→'
          'gated GPU fire 窗消费（tech#112 fire_consume 原子通道·S1 预置发射器=消费轮顺手步）：S1 门→TTS light→same_text→ai_feel→ASR 终轨（--asr-diff 正典面）→E4→E8 七席→M4→F-180 登记——'
          '**材料轴检验位（预注册）**：E4 ≥8.0=材料轴假设增强/潘志明重开条件半面达成·E4 ≤7.0=烟火 register 亦不保带值→系列续供重议（二季止于单件候选）——gated fire 窗（MV sprint 让路照旧）\n')
    return t

def tech_xform(t):
    if not t.endswith('\n'):
        t += '\n'
    t += ('\n116. [R2007 补货·真发现种子] SC-005-07 ASR 字位观察位（tech#97/#102 同型第三案·随件收官轮并读·观察位不占产线）——'
          '缺口锚=本件沪语四词（结棍/灵光/帮帮忙/侬说啥物事）+口令族（对齐——起步——）+数字族（十九年/七人/四十三人/三分贝/三块糖）'
          '=陆海峰 15.0% 沪语密度带同型偏高位预判；判据=SC-005-07 ASR 字位 ≥16% 且 S2 ≤7.5 双触=whisper QC 通道 noise-dict 扩充腿评估'
          '（仅 QC 通道非发布面·字幕轨=edge-tts 直出零损兜底不变）；全 ≤16%=零动作维持 M6 真人校准线注记位——判负留痕合法\n')
    return t

rw(MAIN, main_xform)
rw(TECH, tech_xform)
print('DONE')
