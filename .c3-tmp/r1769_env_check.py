from pathlib import Path

t = Path("data/assets/aihot-poc/AIHOT/.env").read_text(encoding="utf-8")
for ln in t.splitlines():
    if "LLM" in ln or "EXTRA" in ln or "COLLECT" in ln:
        print(repr(ln))
