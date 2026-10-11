# -*- coding: utf-8 -*-
# r1986 (broken-round successor body): tech#106 double-confirmation note +
# main.md row-16 S1 consumption outcome + fire diagnosis evidence file.
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

TECH_ANCHOR = u"判据=下个 fire 窗前后双读数对照〔活度读数与 gate util 翻 GO 时序一致=面成立·分叉=wedged 候查入账〕+hermetic 零动存量调用面·判负留痕合法）——按认领制随轮领做（CPU 面·判断位注记级零闸）"
TECH_APPEND = TECH_ANCHOR + u" **[R1986 双证注记·断轮承接 body 17:0x]**：判据已被第二轮火窗实弹双证——①GO 后窗中翻脸面：fire GO 16:40:56（B-eviction-credit·util_max 32）消费即发 SC-005-04 S1 后 ComfyUI 复燃（17:0x nvidia-smi 100%/11832MiB·compute-apps 唯一占主=ComfyUI python 58200〔MV 会话域〕·llama-server 被逐出零 VRAM）→S1 四发全 ollama timeout（300s/1500s/600s 三窗型·判词零落）+8-token 最小探针 92s 超时=纯 GPU 饿死族定性（非 wedged 槽位族·让路律正确侧）；②17:08:45 复查卡 no-fire（util-face worst-case 99>80 正确拦停=活度读数面已在卡内生效）——消费面新律：GO 消费前必先跑本项 ComfyUI 侧活度读数·窗中翻脸时在飞判词一律作废重发"

MAIN_ANCHOR = u"〔evictable 4888〕·readings-age gate 28s）→三件 fire-ready 维持结转=下个 fire 窗 S1 连发照旧；轮内=tech#97 观察位判读收口（缪一 15.0%<16%+S2 8.0>7.5=不触发·零动作留痕）+tech#102 二批同型观察位入队。"
MAIN_APPEND = MAIN_ANCHOR + u" **[R1986 断轮承接·S1 首程消费结局]**：fire GO 16:40:56 消费即发 SC-005-04 S1（后台 79000·14b 冷载 ~16:47 全 VRAM）→窗中翻脸=ComfyUI 复燃 100%/11.8GB 饿死 ollama（四发 timeout：15:52 300s/15:56 1500s retry 环/16:42 600s·判词零落 expert-verdicts 无新档=**S1 未过门·零假绿灯**）→GPU 腿全族 hard-blocked（M4.5/E4/ASR 终轨同堵）·**三件 fire-ready 维持结转**（04 先发→05→06·F-176/177/178 预指不变）——下个 fire 窗重发 S1 前置=tech#106 活度读数面判据（GO 消费前 ComfyUI 侧 188 /queue+output mtime+CPU 增量三选一）+标准 1500s 窗照旧"

DIAG = u"""# r1986 fire-window S1 consumption diagnosis trail (successor body)
# All ASCII. Evidence for zero-false-green S1 adjudication.

[1] S1 attempts for SC-005-04 (data/storylines/audio/sc005-04-v1-tmp/):
  s1-run.out  15:57:57  GPU-OK util=31% free=9820MB -> ollama timeout (300s) rc=3
  s1-run2.out 15:59:54  DEFER gpu util 93% > 80% (occupied window)
               (gpu-guard-defer-ledger.jsonl +1 row: S1-script defer 15:59:54)
  s1-retry.out 16:26:58 attempt 1/24 non-defer rc=3
               GPU-OK util=28% free=4716MB -> ollama timeout (1500s) rc=3
  .c3-tmp/r1986_s1_00504.out 16:4x-16:5x (prior body, PID 79000)
               GPU-OK util=19% free=4639MB -> ollama timeout (600s) rc=3
  => 4 fired calls, ZERO verdicts landed; expert-verdicts has no new file.
  => S1 NOT passed. Zero false-green. Chain stays at the gate.

[2] Fire window timeline:
  16:34:37 / 16:35:51 cards: no-fire (util worst 100>80)
  16:40:56 card: FIRE verdict (path=B-eviction-credit, gate go=True
           free_min=4942 util_max=32, mv quiet 159.7min, TTL 120s)
  16:42 prior body launches S1 background 79000; 14b cold load ~16:47
  17:0x successor body: nvidia-smi = 100% util, 11832/12282 MiB used
  17:08:45 fresh card: no-fire (util-face worst-case 99% > gate 80)

[3] Root cause (this round's adjudication):
  ComfyUI python PID 58200 (comfyui-krea portable, MV sprint session
  domain = CEO priority line) is the ONLY compute app holding the GPU,
  ~11.8GB. llama-server is evicted (no VRAM in compute-apps list), so
  even an 8-token minimal probe to qwen2.5:14b times out at 92s (needs
  ~9GB reload into ~450MB free). Pure GPU-starvation family, NOT the
  10-10 ollama-wedged-slot family. Yield law correctly applied: no
  restart action taken (restart would not create VRAM).

[4] Ollama service health: /api/tags OK (10 models) - server alive;
  generation path blocked by VRAM starvation only.

[5] Meme V1 deliverable check (CPU view-point): zero mp4 under
  cph4/fleet matching zunjie/brake/meme/shortvideo - still not landed
  (bm-a session domain in flight, zero contact).

[6] tech#26 R1835 stranded backfill recovered this round:
  src/render/whisper_to_srt.py (v3 dict + expect fingerprint gate)
  tests/test_noise_dict.py 34 tests OK
  full suite: Ran 1012 tests in 107.364s OK
  data/pipeline/asr-noise-dict-v3.json + whisper-ledger.jsonl new files
  (stranded since ~10-09 = lingering-hook violation fixed by commit)
"""


def main():
    p = "state/queue/tech.md"
    t = io.open(p, encoding="utf-8").read()
    assert TECH_ANCHOR in t, "tech#106 anchor drift"
    assert TECH_APPEND not in t, "tech#106 note already applied"
    t = t.replace(TECH_ANCHOR, TECH_APPEND, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print("tech.md: #106 double-confirmation note applied")

    p2 = "state/queue/main.md"
    t2 = io.open(p2, encoding="utf-8").read()
    assert MAIN_ANCHOR in t2, "main row16 anchor drift"
    assert MAIN_APPEND not in t2, "main row16 note already applied"
    t2 = t2.replace(MAIN_ANCHOR, MAIN_APPEND, 1)
    io.open(p2, "w", encoding="utf-8", newline="").write(t2)
    print("main.md: row 16 R1986 outcome note applied")

    io.open(".c3-tmp/r1986_fire_diag.txt", "w", encoding="utf-8",
            newline="").write(DIAG)
    print("r1986_fire_diag.txt written")


if __name__ == "__main__":
    main()
