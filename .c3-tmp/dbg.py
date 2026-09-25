import subprocess
cmd = ["ffmpeg", "-i", ".c3-tmp/a2_pitch_p12.mp3",
       "-af", "aspectralstats=measure=centroid,ametadata=print:file=-",
       "-f", "null", "-"]
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc=", r.returncode)
print("--- stdout tail ---")
print(r.stdout[-800:] if r.stdout else "(empty)")
print("--- stderr tail ---")
print(r.stderr[-400:] if r.stderr else "(empty)")
