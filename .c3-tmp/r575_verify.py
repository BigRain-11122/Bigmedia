import io, json

st = json.load(io.open(r"src\os\state.json", encoding="utf-8"))
log_r575 = [l for l in st["log"] if l.find("R575:") >= 0 and l.find("R575: ") >= 0 and "R575" in l[:30]]
with io.open(r".c3-tmp\r575_verify.txt", "w", encoding="utf-8") as f:
    f.write("TICK %s\nTS %s\nTASK %s\nR575_LOG_COUNT %d\n" % (st["tick"], st["ts"], st["task"], len(log_r575)))
    f.write("LASTLOG_HEAD " + st["log"][-1][:80] + "\n")
print("OK")
