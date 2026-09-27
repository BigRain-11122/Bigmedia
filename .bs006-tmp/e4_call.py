# E4 audience reference call - BS-006 draft-collection piece-1 (non-registry seat, direct Ollama;
# .lc001-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Shipinhao 60s soft-cut vertical per #79 piece-2 (release-schedule D18 slot) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs006-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司开业第一天的交底视频——'
    '账号 0、发布 0、粉丝 0，敢说一切落在代码库、每分钟能审计；立了四条规矩：说不清数据从哪来的稿子发不出去、标题承诺什么内容就交付什么、'
    'AI 生成依法打标识包括这条视频本身、数据只从平台后台导出每周跟发布记录对账，不发愿景数字。'
    '画面是终端日志窗口、审查台账表格和黑底字卡交替，右上角全程有「BigStream|BS-006 EP.06」系列角标，左下有系统状态行和轻微扫描线质感；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 57 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话、听不懂的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': vo_path}
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
