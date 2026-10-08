"""MD-0001 script+storyboard generation driver v2 (native API).

v1 lesson: /v1 chat completions ignored think:false for qwen3.5:9b-16k,
all 4096 completion tokens burned in reasoning (finish=length, content
empty). v2 uses ollama native /api/generate with think:false which is
the documented switch for reasoning models.
"""
import json
import re
import sys
import time
import urllib.request

BASE = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b-16k"
PROMPT_FILE = "data/storylines/drama/md0001/prompt-script-v1.txt"
RAW_FILE = "data/storylines/drama/md0001/script-raw-v2.txt"
CONTENT_FILE = "data/storylines/drama/md0001/script-content-v2.json"
REPORT_FILE = "data/storylines/drama/md0001/script-validate-v2.txt"

SCENES = {"open", "lamp", "tower", "cat", "close"}


def validate(doc):
    problems = []
    for key in ("title", "logline", "total_seconds", "characters", "shots"):
        if key not in doc:
            problems.append("missing top key: " + key)
    shots = doc.get("shots", [])
    ids = {c.get("id") for c in doc.get("characters", [])}
    invalid = 0
    for i, sh in enumerate(shots):
        bad = []
        for f in ("id", "scene", "seconds", "visual", "camera", "speaker", "line"):
            if f not in sh or sh[f] in ("", None):
                bad.append(f)
        if sh.get("scene") not in SCENES:
            bad.append("scene-value")
        if sh.get("speaker") not in ids:
            bad.append("speaker-value")
        s = sh.get("seconds")
        if not isinstance(s, (int, float)) or not (3 <= s <= 12):
            bad.append("seconds-range")
        if len(str(sh.get("line", ""))) > 44:
            bad.append("line-length")
        if bad:
            invalid += 1
            problems.append("shot %s bad fields: %s" % (sh.get("id", i), ",".join(bad)))
    n = len(shots)
    if not (10 <= n <= 14):
        problems.append("shot count out of range: %s" % n)
    total = sum(sh.get("seconds", 0) for sh in shots if isinstance(sh.get("seconds"), (int, float)))
    if not (60 <= total <= 90):
        problems.append("total seconds out of 60-90: %s" % total)
    if doc.get("total_seconds") and doc["total_seconds"] != total:
        problems.append("declared total != sum: %s vs %s" % (doc.get("total_seconds"), total))
    rate = (invalid / n * 100.0) if n else 100.0
    return problems, n, invalid, rate, total


def extract_json(text):
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return json.loads(text[start:end + 1])


def main():
    with open(PROMPT_FILE, encoding="utf-8") as f:
        prompt = f.read()
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "think": False,
        "stream": False,
        "options": {"temperature": 0.8, "num_predict": 4096},
    }
    print("POST %s model=%s think=false prompt_chars=%d" % (BASE, MODEL, len(prompt)), flush=True)
    t0 = time.time()
    req = urllib.request.Request(
        BASE,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        print("CALL FAIL: %r" % exc, flush=True)
        sys.exit(1)
    dt = time.time() - t0
    content = data.get("response", "")
    print("CALL done in %.1fs done=%s eval_count=%s" % (dt, data.get("done"), data.get("eval_count")), flush=True)
    with open(RAW_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    with open(CONTENT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    try:
        doc = extract_json(content)
    except Exception as exc:
        print("JSON PARSE FAIL: %r" % exc, flush=True)
        doc = None
    if doc is None:
        print("VALIDATION FAIL: no parsable JSON object", flush=True)
        sys.exit(2)
    problems, n, invalid, rate, total = validate(doc)
    lines = [
        "shot_count=%d invalid=%d invalid_rate=%.1f%% total_seconds=%s elapsed=%.1fs"
        % (n, invalid, rate, total, dt),
    ]
    lines.extend("PROBLEM: " + p for p in problems)
    print("\n".join(lines), flush=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    ok = not problems and rate <= 5.0
    print("VALIDATION " + ("PASS" if ok else "FAIL"), flush=True)
    sys.exit(0 if ok else 3)


if __name__ == "__main__":
    main()
