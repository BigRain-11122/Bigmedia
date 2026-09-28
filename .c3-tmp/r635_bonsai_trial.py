# R635 BigStream CPU-tier content trial vs in-service llama-server :8077
# Spec: cph4/research/R-20260928-bonsai-fleet-trial.md (P-2026-09-28-07)
# Rule: thinking-chain tasks MUST pass chat_template_kwargs.enable_thinking=false (spec sec.3 lesson)
import io, json, time, urllib.request

URL = "http://127.0.0.1:8077"
OUT = r".c3-tmp\r635_bonsai_samples.txt"

def post(path, payload, timeout=600):
    req = urllib.request.Request(
        URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data, time.time() - t0

def chat(system, user, max_tokens=120):
    payload = {
        "model": "bonsai",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    data, wall = post("/v1/chat/completions", payload)
    msg = data["choices"][0]["message"]
    finish = data["choices"][0].get("finish_reason", "?")
    usage = data.get("usage", {})
    return msg.get("content", ""), finish, usage, wall

out = io.open(OUT, "w", encoding="utf-8")

def log(s):
    out.write(s + "\n")

log("# R635 bonsai BigStream content-domain samples (enable_thinking=false)")
log("# server: labbench/bonsai2 llama-server -ngl 0 :8077 (same-machine in-service instance)")

SYS = "你是硅基城市官方媒体的文案作者，只输出要求的句子本身，不要解释，不要引号，用简体中文。"

SAMPLES = [
    (
        "S1-copy-short: city quote candidate line",
        "给虚构的硅基城市写一句居民口吻的短句，主题是「早市」，要求：30 字以内，口语自然，带一点未来都市的生活气息，只输出这一句。",
    ),
    (
        "S2-content-draft: hot-topic reaction line (canteen cook persona)",
        "热点：「全国牛肉批发均价涨至一公斤 71 元」。以硅基城市一位食堂大厨的口吻，写一句对此的反应，40 字以内，口语，符合食堂从业者身份，只输出这一句。",
    ),
    (
        "S3-hook-draft: short-video opening hook line",
        "为一条讲「AI 公司凌晨自动开会做决策」的短视频，写一句 15 字以内的开头钩子文案，要求口语、有悬念、不夸大、不标题党，只输出这一句。",
    ),
]

results = []
for name, prompt in SAMPLES:
    content, finish, usage, wall = chat(SYS, prompt)
    comp = usage.get("completion_tokens", -1)
    log("")
    log("=== " + name + " ===")
    log("PROMPT: " + prompt)
    log("OUTPUT: " + content.strip())
    log("META: finish=%s completion_tokens=%s wall=%.1fs tps_approx=%.2f" % (
        finish, comp, wall, (comp / wall) if (comp and comp > 0 and wall > 0) else -1))
    results.append((name, finish, comp, wall))
    print("%s finish=%s ctok=%s wall=%.1fs" % (name, finish, comp, wall))

# tg128 speed leg: native /completion returns timings.predicted_per_second
try:
    payload = {"prompt": "一句话介绍硅基城市：", "n_predict": 128, "stream": False, "temperature": 0.7}
    data, wall = post("/completion", payload)
    timings = data.get("timings", {})
    content = data.get("content", "")
    log("")
    log("=== tg128 (/completion native timings) ===")
    log("OUTPUT: " + content.strip()[:400])
    log("TIMINGS: " + json.dumps(timings, ensure_ascii=False))
    log("WALL: %.1fs" % wall)
    print("tg128 timings=" + json.dumps(timings))
except Exception as e:
    log("tg128 native failed: %r" % e)
    # fallback: chat call with max_tokens=128, wall-clock approximation
    try:
        content, finish, usage, wall = chat(SYS, "写一段 128 字左右的硅基城市清晨街景描写。", max_tokens=128)
        comp = usage.get("completion_tokens", -1)
        log("")
        log("=== tg128 fallback (chat wall-clock) ===")
        log("OUTPUT: " + content.strip()[:400])
        log("META: completion_tokens=%s wall=%.1fs tps_wall=%.2f" % (comp, wall, comp / wall if comp > 0 else -1))
        print("tg128 fallback ctok=%s wall=%.1fs" % (comp, wall))
    except Exception as e2:
        log("tg128 fallback failed: %r" % e2)
        print("tg128 FAILED")

out.close()
print("done")
