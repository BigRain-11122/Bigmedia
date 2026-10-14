# -*- coding: utf-8 -*-
# r2251: tech#164 CPU-lane three-question retest (main#33 step2+step3).
# Seat qwen2.5:14b restored via R2250 pull. Mirror e4_call.py model/prompt
# style with API num_gpu=0 + num_thread=4 (CEO 10% CPU margin law).
# Q1: CPU lane serves a valid E4-format verdict (HTTP 200 + score line).
# Q2: GPU zero-touch (nvidia-smi used-mem identical before/after).
# Q3: latency viable for the async E4 window (1500s wrapper budget).
import subprocess, sys, time, json, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace") if sys.stdout else None

MODEL = "qwen2.5:14b"
URL = "http://localhost:11434/api/generate"
HARD_CAP_S = 420.0

PROMPT = (
    "你是一名刷信息流的普通读者，看到一张静态盘点卡《城市速报 017·AI 能力认知漏斗之问》"
    "（1080x1080 方图，黑底，左上角[AIGC·AI 生成内容]，标题「城市速报 017」）。"
    "卡上写着：「AI 圈有个认知漏斗」——大模型越强，普通人越看不懂它到底能干什么；"
    "「会用的人拿它赚钱，不会用的人只拿它聊天」——这是当天的原话；"
    "「漏斗三层 · 看得见 · 用得上 · 赚得到」——三层递进，一层比一层人少。"
    "底部声明行「基于硅基城市真实事件（知乎热榜台账档案）」。"
    "背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。"
    "「城市速报」系列是集团旗下媒体公司把城市当天热议话题原样速报出来的卡片。"
    "请回答三个问题，每题一段，直说不委婉：\n"
    "1) 刷到这张卡你会停下来看吗？会保存或转发吗？打几分（0-10）？为什么？\n"
    "2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原文？\n"
    "3) 最弱的一项是什么？"
)


def gpu_state():
    p = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.free",
         "--format=csv,noheader,nounits"], capture_output=True, timeout=15)
    line = p.stdout.decode("utf-8", "replace").strip().splitlines()[0]
    parts = [x.strip() for x in line.split(",")]
    return tuple(int(x) for x in parts)


def main():
    print("R2251 cpu-probe start", flush=True)
    util0, used0, free0 = gpu_state()
    print("GPU-BEFORE util=%d used=%dMB free=%dMB" % (util0, used0, free0), flush=True)

    body = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": True,
        "options": {"num_gpu": 0, "num_thread": 4, "temperature": 0.7,
                    "num_predict": 500},
    }
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    print("POST %s model=%s num_gpu=0 num_thread=4 (stream)" % (URL, MODEL), flush=True)
    t0 = time.time()
    text_parts = []
    done_reason = None
    try:
        with urllib.request.urlopen(req, timeout=HARD_CAP_S) as resp:
            print("HTTP %d" % resp.status, flush=True)
            for raw in resp:
                if time.time() - t0 > HARD_CAP_S:
                    done_reason = "hard-cap"
                    break
                try:
                    chunk = json.loads(raw.decode("utf-8", "replace"))
                except Exception:
                    continue
                if chunk.get("response"):
                    text_parts.append(chunk["response"])
                if chunk.get("done"):
                    done_reason = "done"
                    break
                if len(text_parts) % 60 == 0 and text_parts:
                    print("  t=%.1fs chars=%d" % (time.time() - t0,
                        sum(len(x) for x in text_parts)), flush=True)
    except Exception as e:
        print("CALL-FAIL %.1fs %r" % (time.time() - t0, e), flush=True)
        return 2

    elapsed = time.time() - t0
    text = "".join(text_parts)
    util1, used1, free1 = gpu_state()
    print("GPU-AFTER  util=%d used=%dMB free=%dMB" % (util1, used1, free1), flush=True)
    print("ELAPSED %.1fs done=%s chars=%d" % (elapsed, done_reason, len(text)), flush=True)

    q1 = done_reason == "done" and len(text) > 80 and any(c.isdigit() for c in text)
    q2 = used1 == used0
    q3 = elapsed <= 1500.0
    print("Q1-cpu-lane-verdict-valid: %s" % ("PASS" if q1 else "FAIL"), flush=True)
    print("Q2-gpu-zero-touch: %s (delta=%dMB)" % ("PASS" if q2 else "FAIL", used1 - used0), flush=True)
    print("Q3-latency-viable-1500s-window: %s (%.1fs)" % ("PASS" if q3 else "FAIL", elapsed), flush=True)
    print("---VERDICT-TEXT-HEAD---", flush=True)
    print(text[:900], flush=True)
    print("---VERDICT-TEXT-END---", flush=True)
    print("RESULT q1=%s q2=%s q3=%s elapsed=%.1f" % (q1, q2, q3, elapsed), flush=True)
    return 0 if (q1 and q2 and q3) else 1


if __name__ == "__main__":
    raise SystemExit(main())
