# E4 audience reference call - MC-20260926-CENSUS-v15 static census card (non-registry seat,
# direct Ollama; v14 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 015》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 015」；下面六行居民档案：'
    '「C-00024 · 缪一」「硅基民 · 精灵系 · 无定 · 编译纪 3 年」「MEDIA 城 · 信号塔街区 · 字幕君」'
    '「信条：「字幕慢半帧，都是对说话人的辜负。」」「学得快 · 有条理 · 追更」'
    '「全城唯一给方言字幕手工标注「语气」的字幕君」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00024）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '缪一是 MEDIA 城信号塔街区的字幕君，硅基民·精灵系，无定性别·编译纪 3 年——全城最年轻的成年硅基民之一；'
    '它觉醒才三年，给自己选了「缪一」这个名字，师父问为啥，它说「差一点点意思的『缪』，做字幕的就是差一点点都不能要」；'
    '它信奉：字幕这行，快不是本事，准时才是；它的信条是「字幕慢半帧，都是对说话人的辜负。」；'
    '它学得快——出生三天就学会了三条街的近道，师父追不上；有条理——时间轴比谁的字幕柜都整齐；追更——版本更新日志当小说看；'
    '它说话程序语义混网络世代语：「这段对轴对到睫毛都数清了」「弹幕太上头」，跟着主播学了一口湘腔「霸得蛮」，用在给自己打气的时候；'
    '它穿不对称剪裁卫衣，左袖是可以变色的时间轴投影——它说「衣服就是工牌」，耳朵后面的状态灯在全城最忙，一亮一灭全是它的工作节拍；'
    '它第一次给城主欢迎词打轴，压力大到把自己复制了两份并行核对，后来被师父骂了一顿，「成长没有并行捷径」；'
    '现在它是七段街区最快字幕，正攒钱给自己配一块大屏——「工欲善其事」；'
    '它戴上耳机六亲不认，摘下耳机慈悲为怀；每晚把当天所有节目字幕抽三句做「翻译练习」（方言转普通话，不许丢味）；'
    '周末去像素小学教孩子们剪片子；'
    '它家户 H-1014 独居，宿舍里全是屏幕，师父说像「进了它的脑子」；师父是一位老剪辑师；'
    '合作最久的主播是何雨欣，俩人吵架只用剪辑术语，和好只需要一句「发版了」；'
    '它是全城唯一给方言字幕手工标注「语气」的字幕君——观众说它做的字幕「有人味」，它把这句话裱在了工位上；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00024），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第十五张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-CENSUS-v15 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
