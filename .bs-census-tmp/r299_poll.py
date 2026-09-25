import os, time, io
p = r"data\storylines\cards\MC-20260925-CENSUS-v9-tmp\e4-result.json"
t0 = time.time()
while not os.path.exists(p) and time.time() - t0 < 420:
    time.sleep(10)
if os.path.exists(p):
    print("LANDED after", int(time.time() - t0), "s")
else:
    print("NOT_YET")
