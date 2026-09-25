# E4 audience reference call - MC-20260925-CENSUS-v9 static census card (non-registry seat,
# direct Ollama; MC-20260925-CENSUS-v8-tmp/e4_call.py pattern R298: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 009》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 009」；下面六行居民档案：'
    '「C-00018 · 罗大壮」「碳基市民 · 新市民派 · 男 · 45 岁」「GAME 城 · 像素匠人巷 · 像素画匠」'
    '「信条：「像素越小，心眼越大。」」「耐心 · 手痒 · 护短」'
    '「全城唯一坚持给老城门每月画一张「门脸像」的人」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00018）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万多名虚构居民；'
    '罗大壮是 GAME 城像素匠人巷的一位 45 岁像素画匠，碳基市民·新市民派，坐着数字迁移潮第一班车从东北老家迁来，'
    '落脚那天行李只有一个包袱和一卷自学的画稿；他画像素二十年，最烦「远看挺好近看不忍细看」的活儿，'
    '他说像素讲究的就是「放大八倍还是画」，做人是同一个理——这是他爹送他的话「干活别糊弄，糊弄等于糊弄自己」；'
    '每幅交活前他必放大八倍自检一遍；他的第一幅作品被选进城市里程碑光碑，他在碑前站了一刻钟，'
    '回家给爹打了个电话，俩人谁都没说话；现在他在匠人巷开了间小画室带学徒，供着一块「初版像素调色板」；'
    '他每月去老城门画一张「门脸像」，五十七张连起来就是一部门禁链的编年史——城里再没别人这么干；'
    '他性格耐心（能为一片瓦的投影磨一整天）、手痒（看见新工具手就痒，不拆不快）、护短（自家街区的人只能自己说，外人不行）；'
    '他的信条「像素越小，心眼越大。」这句也出现在同系列的「城市语录 004」卡上——那张按署名规矩不指名居民，'
    '这张登记的正是实名居民本人；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00018），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第九张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v9 static card (cards.json + render output)'}
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
