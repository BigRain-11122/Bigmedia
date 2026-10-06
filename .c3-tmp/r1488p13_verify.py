import json, io, subprocess

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
old = subprocess.run(["git", "-C", ROOT, "show", "HEAD:src/os/state.json"],
                    capture_output=True).stdout.decode("utf-8")
data_old = json.loads(old)
with io.open(ROOT + r"\src\os\state.json", encoding="utf-8") as f:
    data_new = json.load(f)

lo, ln = data_old["log"], data_new["log"]
print("old_len=%d new_len=%d" % (len(lo), len(ln)))
print("old_tail_repr=%r" % (lo[-1][-120:],))
print("new_tail_repr=%r" % (ln[-2][-120:],))
print("r1487_identical=%s" % (lo[-1] == ln[-2],))
print("r1488_new_tail=%r" % (ln[-1][-100:],))
print("keydiff=%s" % (set(data_old.keys()) ^ set(data_new.keys()),))
for k in data_old:
    if k not in ("log", "tick", "ts", "task") and data_old[k] != data_new.get(k):
        print("CHANGED_KEY=%s" % k)
print("wm_len_old=%d wm_len_new=%d" % (len(data_old["decisions_watermark"]["dnums"]),
                                        len(data_new["decisions_watermark"]["dnums"])))
