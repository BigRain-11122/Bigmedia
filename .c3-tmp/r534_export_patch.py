# -*- coding: utf-8 -*-
# R534 status-export patch: export_ts + engineering-dept "s" field (ASCII-only payloads, binary-safe, zero newline translation)
import json, re, time, sys

P = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\docs\status-export.json"
raw = open(P, "rb").read()
now = time.strftime("%Y-%m-%dT%H:%M:%S+08:00").encode("ascii")

# 1. export_ts refresh (P-61 freshness gate)
raw2 = re.sub(rb'"export_ts": "[^"]*"', b'"export_ts": "' + now + b'"', raw, count=1)
assert raw2 != raw, "export_ts patch failed"

# 2. engineering dept machine-readable tick face: R532 -> R534
new_s = (
    "R534: full task-book anomaly round - R533 interrupted-attempt double-record fix "
    "(17:04 firing exited clean 17:06:50 with zero state write; done-beat 533 vs tick 532 = account hole; "
    "tick 532->534 with R533+R534 log entries per R155/R425 precedent) + ledger five-mode anchor correction 22->31: "
    "r531_check.py/r532_check.py had five-mode Chinese tag literals corrupted to '?' strings at write time "
    "(PS5.1 GBK file-layer corruption), their count 22 = @BigStream-ASCII-only artifact; ledger mtime 15:15:21 "
    "unchanged across R530->R533 proves group never rewrote it, overturning R531 'group R2-wave re-anchor to 22' "
    "determination; r533_lednew.txt 31-row dump = all historical (newest transfer P-2026-09-27-07 received R515) "
    "= zero new transfers; corrective law: probe five-mode tag matching must use unicode escapes (r533_all.py canon); "
    "five checks otherwise quiet (orders 35 files anchor mtime 13:53:11 unchanged, decisions 56=anchor, production=open, "
    "no bm-a activity: storylines tails 12:49/09-25); backlog top not claimable (#78 FluxVerse footage blocked, "
    "#63 C-00030/31 supply-gated, #59 REACT due 09-28, #70 OSS 09-29, W40 weekly audit opens 09-28 + monthly stats note <=09-30); "
    "probes inherited from R533 17:04:49 run (board 0 FAIL / readiness 3 external blockers 0 findings / loop_health 2F+24W all in-case); "
    "anomaly-trigger window-close commit R531-R534 (state.json + status-export + .c3-tmp r531/r532/r533 evidence, .sc003 tmp untouched), "
    "push, window reset R535-R540; daily 09-27 in place, benchmarks day3 skip, tokens:local=0, publish lock unchanged (not live = not measured)"
).encode("ascii")

pat = re.compile(rb'"s": "R532: idle-fast[^"]*"')
assert pat.search(raw2), "s-field anchor not found"
raw3 = pat.sub(b'"s": ' + b'"' + new_s + b'"', raw2, count=1)

open(P, "wb").write(raw3)
json.load(open(P, encoding="utf-8"))
print("PATCH_OK export_ts=" + now.decode("ascii"))
