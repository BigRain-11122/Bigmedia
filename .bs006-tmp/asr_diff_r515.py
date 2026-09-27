# ASR final-track diff (R515) - BS-006 S2-seat evidence: difflib char-level.
# v2: script-variant normalization (whisper medium emitted traditional glyphs for
# this track; same words, same sounds -> normalize trad->simp before diffing,
# drift logged honestly as channel artifact, M6 note) + punctuation stripped on
# both sides (series methodology: 去标点 char basis) + digit-alive accepts
# Chinese-numeral form (0->零 = value alive, R512 形差分离 precedent).
# UTF-8 file output only (console CJK is GBK-blind, encoding law).
import difflib, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))

TRAD2SIMP = {
    '統': '统', '誌': '志', '開': '开', '業': '业', '賬': '账', '號': '号',
    '發': '发', '佈': '布', '這': '这', '麼': '么', '碼': '码', '庫': '库',
    '審': '审', '計': '计', '線': '线', '沒': '没', '測': '测', '說': '说',
    '數': '数', '據': '据', '來': '来', '標': '标', '題': '题', '諾': '诺',
    '內': '内', '條': '条', '視': '视', '頻': '频', '時': '时', '鐘': '钟',
    '絲': '丝', '後': '后', '檢': '检', '備': '备', '錄': '录', '檔': '档',
    '樣': '样', '態': '态', '應': '应', '該': '该', '讓': '让', '質': '质',
    '規': '规', '過': '过', '對': '对', '戶': '户', '約': '约', '記': '记',
    '導': '导', '種': '种', '識': '识', '續': '续', '轉': '转', '給': '给',
    '傷': '伤', '實': '实', '預': '预', '講': '讲', '輯': '辑', '點': '点',
    '黨': '党', '檯': '台', '廣': '广', '電': '电', '視': '视', '頻': '频',
    '歲': '岁', '萬': '万', '億': '亿', '關': '关', '門': '门', '們': '们',
    '機': '机', '構': '构',     '殺': '杀', '壓': '压', '滿': '满', '髮': '发', '從': '从', '遞': '递',
}

NUMERAL_EQUIV = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
                 '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}

PUNCT = set(map(chr, [
    0xFF0C, 0x3002, 0x3001, 0xFF1B, 0xFF1A, 0xFF1F, 0xFF01, 0x2014, 0x2026,
    0x201C, 0x201D, 0x2018, 0x2019, 0x22, 0x27, 0x28, 0x29, 0x2C, 0x2E,
    0x3A, 0x3B, 0x3F, 0x21, 0x2D, 0x20,
]))

def normalize(s, descriptify=False):
    out = []
    for ch in s:
        if ch.isspace() or ch in PUNCT:
            continue
        if descriptify:
            ch = TRAD2SIMP.get(ch, ch)
        out.append(ch)
    return ''.join(out)

def srt_text(p):
    txt = []
    for ln in io.open(p, encoding='utf-8-sig'):
        ln = ln.strip()
        if ln and not ln.isdigit() and '-->' not in ln:
            txt.append(ln)
    return ''.join(txt)

ref_raw = io.open(os.path.join(HERE, 'voiceover.txt'), encoding='utf-8').read()
hyp_raw = srt_text(os.path.join(HERE, 'asr-check.srt'))
ref_c = normalize(ref_raw)
hyp_c = normalize(hyp_raw, descriptify=True)

sm = difflib.SequenceMatcher(None, ref_c, hyp_c, autojunk=False)
sites = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        sites.append((ref_c[i1:i2], hyp_c[j1:j2]))
diff_chars = sum(len(a or b) for a, b in sites)

digit_lines = []
for d in re.findall(r'[0-9]+', ref_c):
    cands = [d] + [NUMERAL_EQUIV.get(c, c) for c in d]
    ok = any(c in hyp_c for c in (d, ''.join(NUMERAL_EQUIV.get(c, c) for c in d)))
    digit_lines.append("%s:%s" % (d, 'ALIVE' if ok else 'LOST'))

out = []
out.append("REF_CHARS=%d HYP_CHARS_RAW=%d HYP_CHARS_SIMP=%d" % (
    len(ref_c), len(normalize(hyp_raw)), len(hyp_c)))
out.append("SCRIPT_DRIFT=trad->simp normalized (whisper medium channel artifact, same words; logged honestly)")
out.append("RATIO=%.4f SITES=%d DIFFCHARS=%d PCT=%.1f%%" % (
    sm.ratio(), len(sites), diff_chars, 100.0 * diff_chars / max(1, len(ref_c))))
out.append("DIGITS=" + ("; ".join(digit_lines) if digit_lines else "none-in-ref"))
for a, b in sites:
    out.append("SITE|%s -> %s" % (a, b))
io.open(os.path.join(HERE, 'asr-diff-r515.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print("OK sites=%d pct=%.1f" % (len(sites), 100.0 * diff_chars / max(1, len(ref_c))))
