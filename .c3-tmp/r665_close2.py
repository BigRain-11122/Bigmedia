# -*- coding: utf-8 -*-
# R665 close part 2 (SE-only): outs[0] is a 2-element row [title, text] - OS row text is index 1, not 2
import io, json, datetime, collections

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
SE = ROOT + r'\docs\status-export.json'
now = datetime.datetime.now()

se = json.load(io.open(SE, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
se['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
se['outs'][0][1] = (u"tick 665\uff1aR665 declared-idle \u7a7a\u8f6e\u5224\u5b9a\uff08\u4e94\u9759+\u63a2\u9488\u7eff+\u53ef\u9886\u5e8f\u5c3d\u00b7\u65b0\u7a97 1/6=R665-R670 \u672c\u7a97\u4e0d commit\uff09\uff1abm-a codex \u6279\u672a\u95ed\u8ba9\u4f4d\u7ef4\u6301\uff08README+3/city-humanities+14 worktree \u672a\u6682\u5b58\u6001=git diff --cached \u7a7a\u590d\u6838\u5b9a\u8c27\u00b7mtime 04:06 \u672a\u52a8\uff09\u00b7\u4e94\u67e5\u951a\u9759\uff08orders O-1910/ledger 34 rowdiff NEW=0 GONE=0=r665_probe \u516d\u6a21\u5f0f\u5b9e\u8dd1/decisions 68\uff09\u00b7\u53ef\u9886\u9879\u9010\u4ef6\u6838\u8fc7\u5168 gated\uff08#86 \u56db\u817f\uff1aa \u6e90\u95ed/b \u951a\u6b62 C-00029 anchors \u590d\u6838 20 \u5361 C-00030 False/c+d \u8ba9\u4f4d\u533a\u00b7#70 21:40 \u672a\u5230\u00b7#67 \u96f6\u89e6\u53d1\u00b7#63 \u540c\u951a\u00b7#59 v6 \u6302 09-30\u00b7queue \u9876\u9879 gated\u00b7W40 \u63d0\u6848 P-1 \u5df2\u4ea4\uff09\u00b7\u4e09\u63a2\u9488 board 0F/readiness 3 \u7686\u5916\u90e8 0 \u53d1\u73b0/loop 3F+43W \u5728\u6848\u7c7b\uff08account-lag tick665 \u6536\u8d26\u81ea\u5e73\u00b7\u65b0 1 WARN=07:12\u219207:34 22min \u7a97\u754c gap \u5408\u6cd5\uff09\u00b7\u4f8b\u884c\u4ef6\u65e5\u62a5 09-29+W40 \u5468\u5ba1\u5728\u6848\u4e0d\u91cd\u8dd1\u00b7tokens:local=0\u2014\u2014\u4e0b\u8f6e R666 \u53ef\u9886\u5e8f=\u2460#86\uff08bm-a \u6279\u95ed\u5224\u636e\uff09\u2461#70 \u5207\u7247 2\uff0821:40 \u540e\uff09\u2462#67 \u89e6\u53d1\u5f8b\u2463REACT v6=09-30 \u7a97")
res_row = [
    u"665",
    (u"R665 declared-idle \u7a7a\u8f6e\u5224\u5b9a\uff08\u4e94\u9759+\u63a2\u9488\u7eff+\u53ef\u9886\u5e8f\u5c3d\u00b7\u65b0\u7a97 1/6=R665-R670\uff09\uff1a\u4e94\u67e5\u951a\u9759\uff08orders O-1910/ledger 34 rowdiff NEW=0 GONE=0\uff3br665_probe \u516d\u6a21\u5f0f\u5b9e\u8dd1\uff3d/decisions 68\uff09\u00b7bm-a codex \u6279\u672a\u95ed\u8ba9\u4f4d\u7ef4\u6301\uff08README+3/city-humanities+14 worktree \u6001\u00b7git diff --cached \u7a7a\u590d\u6838\u00b7mtime 04:06 \u672a\u52a8\u00b7HEAD ad4a501 \u96f6\u65b0 commit\uff09\u00b7\u53ef\u9886\u5e8f\u5c3d\uff08#86 \u56db\u817f gated\uff1aa \u6e90\u95ed/b \u951a\u6b62 C-00029 anchors \u590d\u6838 20 \u5361 C-00030 False/c+d \u8ba9\u4f4d\u533a\u00b7#70 21:40 \u672a\u5230\u00b7#67 \u96f6\u65b0\u4e8b\u4ef6\u00b7#63 \u540c\u951a\u00b7#59 v6 \u6302 09-30/#31 \u7a3f\u672a\u843d/#78 \u7d20\u6750\u95e8/queue \u9876 gated/W40 \u63d0\u6848 P-1 \u5df2\u4ea4\uff09=\u4fdd\u62a4\u6001\u8c41\u514d\u9762\u5728\u6848\u00b7\u4e09\u63a2\u9488 board 0F/readiness 3 \u5916\u90e8 0 \u53d1\u73b0/loop 3F+43W \u5728\u6848\u7c7b\uff08account-lag tick665 \u6536\u8d26\u81ea\u5e73\u00b7\u65b0 1 WARN=07:12\u219207:34 22min \u7a97\u754c gap \u5408\u6cd5\uff09\u00b7\u4f8b\u884c\u4ef6\u65e5\u62a5 09-29+W40 \u5468\u5ba1\u5728\u6848\u4e0d\u91cd\u8dd1\u00b7tokens:local=0\u00b7\u4e0b\u8f6e\u53ef\u9886\u5e8f\u4e0d\u53d8\uff08#86 \u8ba9\u4f4d\u5224\u636e/#70 21:40/#67 \u89e6\u53d1\u5f8b\uff09")
]
if not any(r[0] == '665' for r in se['results']):
    se['results'].append(res_row)
io.open(SE, 'w', encoding='utf-8').write(json.dumps(se, indent=1, ensure_ascii=False) + '\n')
print('se done: export_ts=' + se['export_ts'] + ' results_len=' + str(len(se['results'])))
