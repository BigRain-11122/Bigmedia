# -*- coding: utf-8 -*-
"""R2257 close: orders origin-delta 9-row consumption ack + F-180 S1 CPU-lane dispatch accounting
+ finalize_state + explicit-file close commit + canonical export. UTF-8 (encoding law)."""
import os, sys, time, json, io, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src', 'os'))
import close_commit as cc

NOW = time.strftime('%Y-%m-%d %H:%M:%S')
hm = time.strftime('%H:%M')[:4] + u'x'

# --- face 0: disk-only evidence capture of the 9 origin-only rows (R2083 precedent; .c3-tmp gitignored) ---
GIT = r'C:\Program Files\Git\cmd\git.exe'
try:
    b = subprocess.run([GIT, '-C', ROOT[:ROOT.find('media')].rstrip('\\') if 'media' in ROOT else ROOT,
                        'show', 'origin/main:docs/orders.md'], capture_output=True).stdout
    txt = b.decode('utf-8', 'replace')
    lines = txt.split('\n')
    idx = None
    for i, l in enumerate(lines):
        if 'C-20261014-01' in l and l.strip().startswith('|'):
            idx = i
    if idx is not None:
        rows = [l for l in lines[idx + 1:] if l.strip()]
        with io.open(os.path.join(ROOT, '.c3-tmp', 'r2257_orders_origin_tail.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(rows) + '\n')
        print('EVIDENCE rows=%d captured' % len(rows))
except Exception as exc:
    print('EVIDENCE-SKIP %s' % exc)

# --- face 1: tech queue seed (R2257 genuine seed; queue re-stock step) ---
TQ = os.path.join(ROOT, 'state', 'queue', 'tech.md')
tqt = io.open(TQ, encoding='utf-8').read()
if '172. [R2257' not in tqt:
    assert '171.' in tqt, 'tech.md tail anchor drift (expected item 171)'
    seed = (
        u"\n172. [R2257 \u79cd\u5b50\u00b7tech#169 S1 \u817f\u843d\u5730\u6d3e\u751f] **S1 CPU \u822a\u9053 launcher \u751f\u6210\u5668\u65cf\u7edf\u4e00\u4f4d**"
        u"\uff08\u7f3a\u53e3\u951a=R2257 \u5b9e\u951a\uff1aE4 \u817f=e4_launcher_gen.py --cpu-lane \u751f\u6210\u4ef6\u5728\u5f79\uff3btech#169 \u91c7\u7eb3\uff3d"
        u"\u800c S1 \u817f R2257 \u624b\u5199 s1_call_cpu.py=\u540c\u65cf\u5de5\u827a\u672a\u6c89\u6dc0\u2014\u2014\u4e24\u817f\u5171\u4eab CPU \u8f66\u9053\u5f8b\uff3bnum_gpu=0 \u65ad\u8a00\u5373\u98de\u884c"
        u"/num_thread=4 CEO \u4f59\u91cf/liveness rc3/build_prompt parity\uff3d\u4ec5 body \u4e0e\u6750\u6599\u4f4d\u5f02\u2014\u2014"
        u"\u5019\u9009=\u751f\u6210\u5668\u65cf\u6cdb\u5316\uff3bs1_launcher_gen.py \u6216 e4_launcher_gen \u901a\u7528\u5316 --expert \u9762\uff3d"
        u"\u00b7\u5224\u636e=R2257 S1 CPU \u8bfb\u6570\u843d\u5730\u540e\u8bc4\uff3b\u8fc7\u95e8/\u8d85\u65f6/\u4f20\u8f93\u4e09\u6001\u7686\u5165\uff3d\u00b7tech#81 \u81ea\u542b\u5f8b=launcher \u5165\u5e93\u5df2\u6267\u00b7\u751f\u6210\u5668\u4f4d=\u4e0b\u7a97\u9886\uff09\n"
    )
    with io.open(TQ, 'a', encoding='utf-8') as f:
        f.write(seed)
    print('TECH-SEED appended (item 172)')
else:
    print('TECH-SEED skip (idempotent)')

# --- face 2: helper cleanup (round-debris hook; evidence file kept disk-only) ---
removed = 0
for fn in ['r2257_origin_rows.py', 'r2257_probe2.py', 'r2257_hot_supply.py', 'r2257_v19_template.py',
           'r2257b_read_v19.py', 'r2257_queues.py', 'r2257_f180_preflight.py', 'r2257b_s1_infra.py']:
    p = os.path.join(ROOT, '.c3-tmp', fn)
    if os.path.isfile(p):
        os.remove(p)
        removed += 1
print('HELPERS-REMOVED %d' % removed)

LOG = (
    u"2026-10-14 " + hm + u" R2257: \u8f6c\u529e\u6d88\u8d39\u8f6e+fire \u961f\u5934\u6d88\u8d39\u8f6e\u00b7orders origin-delta 9 \u884c\u6d88\u8d39+F-180 SC-005-07 S1 \u62e6\u622a\u5e2d CPU \u822a\u9053\u817f\u843d\u5730+\u70b9\u706b"
    u"\uff08R2256 \u4e0b\u8f6e\u6307\u9488\u5151\u73b0\uff1aF-180 \u62e6\u622a\u5e2d+\u5b88\u671b\u7eed+REACT-v20 \u5019\u9009\u5224\u8bfb\uff09"
    u"\u2014\u2014\u2460\u8f6e\u9996\u4e94\u67e5\uff1aorigin_gap QUIET ahead0 behind0+group_scan \u516d\u9762\uff1aDECISIONS truly_new=0 \u6c34\u4f4d 164\u00b7LEDGER @BigStream 5 \u884c=\u503c\u5b88\u951a\u96f6\u65b0\u8f6c\u529e"
    u"\u00b7ORDERS worktree quiet 403\u00b7**ORDERS-ORIGIN-DELTA WARN delta=9=rows 404-412 \u7834\u9759**\u2192git show origin/main \u9010\u884c\u6d88\u8d39\uff08tech#165 \u951a\u884c\u5f15\u7528\u00b7D-13 SLA \u5e26\u5185\u00b7\u8bc1\u636e\u4ef6\u76d8\u4e0a\u7559\u6863\uff09\uff1a"
    u"404=O-20261014-1215 \u4fee\u6cd5\u5305 v1\uff08executed \u77e5\u6089\uff1a\u5426\u51b3\u7a97\u5168\u94fe\u5e9f\u6b62/CEO-PROXY \u56db\u4ef6\u63a5\u7ebf/\u6392\u4ea7\u5e8f\u5165\u6b63\u5178/\u7248\u672c\u6cd5\u5178\u5730\u56fe/\u89c2\u5bdf\u671f\u51bb\u7ed3\u89e3\u9664\uff09"
    u"405=O-1245 \u5de1\u73ed\u67b6\u6784\u8c03\u7814\u843d\u5730\uff08ROUND v3 \u56db\u5347\u7ea7\u00b7\u77e5\u6089\uff09406=O-1315 \u4ee3\u7406\u5e2d\u81ea\u8fed\u4ee3\u4ee4\uff08\u6b659 \u95ed\u73af\u5165 ROUND\u00b7\u77e5\u6089\uff09"
    u"407=@bm-c V3 \u6ce21 \u516d\u955c\u56de\u4f20+\u6ce22 \u70b9\u706b\uff08MV \u88c5\u914d\u7ad9\u57df\u00b7\u672c\u5faa\u73af\u67e5\u770b\u4f4d\u96f6\u63a5\u89e6\u00b7R2247 \u6d88\u8d39\u4f4d\u627f\u7ee7\uff09"
    u"408=O-1705 \u673a\u5236\u5168\u94fe\u6761\u5ba1\u67e5\uff085 \u7f3a\u53e3\u4fee\u590d\u540c\u7a97\u6536\u53e3\u00b7\u77e5\u6089\uff09409=O-1745 \u4e3bAGENT \u5341\u4e09\u5e2d\u4e24\u6ce2\u7fa4\u5ba1\uff08executed\u00b7\u672c\u53f8\u96f6\u70b9\u540d\u4efd\u989d\uff09"
    u"410=**O-20261014-1855 \u5168\u9762\u5f00\u5de5\u591c\u4ee4**\uff08MV \u6700\u9ad8\u4f18\u5148+10-15 \u6668 08:43 \u6210\u54c1\u6b7b\u7ebf=\u672c\u5faa\u73af\u6267\u6cd5\u9762\uff1a\u5168\u901f\u751f\u4ea7+MV GPU \u8ba9\u8def+CPU \u9762 24/7 \u5408\u6cd5\u8f66\u9053\uff09"
    u"411=Phase 1-\u03b1 \u901f\u6548\u4ef6\u90e8\u7f72\uff08executed\u00b7\u77e5\u6089\uff09412=**MV V3 wave2 39/39 \u6536\u5272\u4ea4\u4ed8\u9762**\uff0822:3x \u843d\u00b7\u88c5\u914d\u7ad9\u53ef\u5f00\u00b7bm-a \u88c5\u914d\u7a97\u6d88\u8d39\u9762\u00b7\u672c\u5faa\u73af\u67e5\u770b\u4f4d\uff09"
    u"\u2014\u2014ack=\u672c\u884c+commit\uff08P-51 \u4e09\u8981\u7d20\uff09\uff1b"
    u"\u2461P1 \u677f\u5e8f\u53d6\u6d3b\uff1abacklog \u9876\u884c\u5168 gated\uff08#111 \u67e5\u770b\u4f4d\u65cf/#112 tech#92 \u5224\u636e\u7a97 10-15 08:00/#110 LEG-3 VRAM \u95e8 free 3.9G/#106 gated/#59 REACT \u7a97\uff09"
    u"\u2192**REACT-v20 \u6309\u65e5\u70ed\u70b9\u7a97\u4f9b\u7ed9\u5224\u8bfb=\u4eca\u65e5\u8017\u5c3d gated \u5982\u5b9e\u6ce8\u8bb0**\uff08v17/v18/v19 \u5df2\u6d88\u8d39 zhihu #4/#5/#2\u00b7\u4f59\u9898\u6750\u5168\u7b5b\u9664\uff1a#1 462 \u4e07\u672a\u7ed3\u6848\u6267\u6cd5\u9762\u56de\u907f\u5f8b/#3 190 \u4e07\u66b4\u529b\u4f24\u4ea1\u9762"
    u"/#6+#7 \u5177\u540d\u5267\u96c6\u89d2\u8272+\u827a\u4eba\u5916\u8c8c\u9762/#8-#10 \u5177\u540d IP \u6620\u5c04\u5f31+bilibili 10 \u6761=\u5177\u540d UP \u4e3b\u4f53\u88c1\u9762\u96f6\u76f4\u914d\u884c\uff3bv14/v19 \u5224\u4f8b\u590d\u7528\uff3d"
    u"\u00b7bilibili #1 63 \u5c0f\u65f6\u9762\u5305\u8f66=\u540c\u5224\u65cf\u4e0d\u5165\u699c\u3014\u5224\u4f8b\u6267\u6cd5\u975e\u7ffb\u6848\u3015\uff09\u2192\u660e\u6668\u65e5\u62a5\u7a97\u518d\u5224\uff1b"
    u"\u2462**F-180 SC-005-07 S1 \u62e6\u622a\u5e2d CPU \u822a\u9053\u817f\u843d\u5730+\u70b9\u706b**=fire \u961f\u5934 tech#105 \u6d88\u8d39\u5e8f\u5151\u73b0\u2014\u2014tech#169 \u91c7\u7eb3\u8bbe\u8ba1\u7684 S1 \u672a\u843d\u817f\uff08E4 \u817f e4_call_cpu.py \u5df2\u5728\u5f79\u00b7S1 \u817f\u672c\u8f6e\u8865\u9f50\uff09\uff1a"
    u"s1_call_cpu.py \u4ea4\u4ed8\uff08launcher-local \u6559\u4e49\uff3btech#122 \u5148\u4f8b\uff3d\u00b7liveness /api/tags 2s \u63a2\u9488 rc3\u00b7registry \u5e2d\u4f4d\u96f6\u786c\u7f16\u7801"
    u"\u00b7build_prompt parity=====\u6750\u6599===== \u88c5\u914d\u00b7num_gpu=0 \u65ad\u8a00\u5373\u98de\u884c=\u96f6 VRAM \u96f6 MV \u51b2\u7a81"
    u"\uff3bGPU \u822a\u9053\u6162\u7a97\u4e09\u70e7\u8bfb\u6570\uff1aflight-3 1500s \u8d85\u65f6+rc7 \u5ea7\u5e2d\u63a2\u9488 240s \u8d85\u65f6=GPU \u822a\u9053\u7ed3\u6784\u6027\u6162\u7a97\u00b7CPU \u5916\u63a8 110-180s\u226a1500s=tech#169 \u590d\u6d4b\uff3d"
    u"\u00b7num_thread=4=CEO 10% CPU \u4f59\u91cf\u5f8b\uff3bO-20261013-2215 CPU \u9762 24/7 \u5408\u6cd5\u8f66\u9053\uff3d\uff09\u00b7\u70b9\u706b PID 64508 detached+\u53cc redirect\u00b7.out/.err \u53cc\u7a7a=\u6d3b\u6027\u8fc7\u8fdb\u751f\u6210\u6bb5"
    u"\u2014\u2014\u7ed3\u679c s1-cpu-result.json \u8f6e\u95f4\u843d\u5730\u00b7\u4e0b\u8f6e\u9996\u8bfb\uff1a\u22659 \u8fc7\u95e8\u2192TTS light \u817f/<9 \u5b9e\u8d28\u65d7\u6574\u6539\uff3b\u8fd4\u5de5 \u22642 \u8f6e\u5347\u88c1\uff3d/TIMEOUT\u2192\u91cd\u53d1"
    u"\u00b7\u5224\u8bcd\u6863\u6848+expert-calls \u884c=\u8bfb\u56de\u8f6e call_expert \u5355\u5199\u8005\u8865\u8d26\uff1b"
    u"\u2463MV \u5b88\u671b\uff1arelease/ \u4ecd 10-08 \u65e7\u6837\u7247\u533a\uff08V3.5 \u9884\u89c8\u526a/\u7ec8\u526a\u4eca\u665a bm-a \u88c5\u914d\u7a97\u5728\u6267\u00b7GPU 4%/8.3G\u00b7\u88c5\u914d ffmpeg \u9762=CPU \u5408\u6cd5\u5171\u5b58\uff09"
    u"\u00b7wave2 39/39 CDN \u4fee\u590d\u9762\u5df2\u843d\uff08row 412\uff09\uff1b"
    u"\u2464\u4f8b\u884c\u4ef6\uff1a10-14 \u65e5\u62a5\u5728\u6848\u4e0d\u91cd\u8dd1\uff08O-2304 \u94c1\u5f8b\uff09\u00b7W42 \u5468\u5ba1\u5728\u6848\u00b7GB \u00a74 \u4e0b\u671f 10-15 \u8df3\u8fc7"
    u"\u00b7HQ-FEEDBACK \u4e0d\u5199\uff08\u96f6\u96c6\u56e2\u5c42\u65b0 open \u95ee\u9898\uff09\u00b7T1 \u50ac\u529e\u65e0\u8d85\u7ebf\u9879\u00b7tokens:local=0\uff08S1 CPU \u5728\u98de=\u843d\u5730\u8f6e\u8bb0\u8d26\u00b7P-54\u2464\uff09"
    u"\u00b7\u4e34\u65f6\u4ef6\u6e05\u7406\u94a9=r2257 \u52a9\u624b\u4ef6\u5220\u51c0\uff08origin rows \u8bc1\u636e\u4ef6\u76d8\u4e0a\u7559\u6863\uff09"
    u"\u00b7\u961f\u5217\u8865\u8d27\u6b65=tech \u65b0\u79cd\u5b50 1 \u6761\uff08tech#172 S1 CPU launcher \u751f\u6210\u5668\u65cf\u7edf\u4e00\u4f4d\uff09"
    u"\u2014\u2014\u4e0b\u8f6e=\u2460S1 CPU \u8bfb\u6570\uff08\u95e8\u5224\u5b9a+\u6863\u6848\u8865\u8d26\uff09\u246110-15 08:00 tech#92 \u951a\u4f8b\u91cd\u5224\u7a97\uff08zhihu \u5934\u90e8 \u22653 \u226560=PASS/fallback T1 60\u219255\u00b7tech#159 \u5de5\u5177\uff09"
    u"\u2462MV V3 \u6210\u7247\u5b88\u671b\uff0808:43 \u73ed\u5448 CEO\uff09\u2463REACT-v20 \u660e\u6668\u65e5\u62a5\u7a97\u2464F-180 \u8fc7\u95e8\u5219 SC-005-07 TTS light \u817f"
)

FOCUS = (
    u"R2257 consumed 9 origin-only orders rows 404-412 (tech#165 anchors: O-1215/1245/1315/1705/1745 executed-side "
    u"ack, rows 407/412 MV-lane view-only, O-1855 full-speed night order = MV yield + CPU 24/7 legal face), gated "
    u"REACT-v20 (today's hot supply exhausted per screening precedents), and landed the missing S1 leg of the "
    u"adopted CPU-lane dispatch design: s1_call_cpu.py dispatched (F-180 fire-head consumption, tech#169/tech#166 "
    u"seat revived, num_gpu=0 zero VRAM vs MV window, PID 64508 in flight). NEXT: S1 CPU readback gate ruling + "
    u"10-15 08:00 tech#92 anchor re-judge window + MV V3 08:43 deadline watch + REACT-v20 morning window + TTS leg."
)

DO = (
    u"R2257: consumed origin orders rows 404-412 (MV night order acked, MV-lane rows view-only); REACT-v20 "
    u"supply-gated today; F-180 S1 gate dispatched on CPU lane (s1_call_cpu.py in flight, zero VRAM); next: "
    u"S1 CPU readback gate ruling + 10-15 08:00 tech#92 window + MV V3 08:43 watch"
)

cc.finalize_state(LOG, ts=NOW, focus=FOCUS)

FILES = [
    u"src/os/state.json",
    u"state/queue/tech.md",
    u"data/storylines/audio/sc005-07-v1-tmp/s1_call_cpu.py",
    u"data/storylines/audio/sc005-07-v1-tmp/close_state_r2257.py",
]
MSG = ("R2257 [via bm-a]: consume origin-only orders rows 404-412 (tech#165 anchors; O-1215/1245/1315/1705/1745 "
       "executed-side ack, rows 407/412 MV-lane view-only, O-1855 MV-night-order ack; next: S1 CPU readback + "
       "tech#92 10-15 08:00 window); dispatch F-180 SC-005-07 S1 gate on CPU lane (s1_call_cpu.py, tech#169 S1 "
       "leg, tech#166 seat revived, num_gpu=0 zero VRAM vs MV window); REACT-v20 supply-gated (v17/18/19 consumed, "
       "rest screened per v14/v19 precedent); tech seed: S1 CPU launcher generator unification")
rc, lines = cc.run_close_commit(FILES, MSG, export_do=DO, expect_tick=2257)
for ln in lines:
    print(ln.encode('ascii', 'replace').decode('ascii'))
print('CLOSE RC=%d' % rc)
