import io, re
e = io.open(r"src/render/emotive_tts.py", encoding="utf-8").read()
m = re.search(r"def parse_beats\(.*?\n(?=\ndef )", e, re.S)
print(m.group(0) if m else "nf")
