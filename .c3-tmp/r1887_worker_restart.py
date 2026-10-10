"""R1887: restart AIHOT worker to reload cached prompt texts.

Finding: prompts.ts caches pack files in a module-level Map and analyze.ts
computes PREFILTER_SYSTEM/SCORE_SYSTEM at import time, so the R1886
prefilter-city swap AND this round's selection-score-city swap both stay
inert until the worker process restarts. Worker restart is our own PoC
domain (R1764/R1770/R1771 precedent). Mode matches the running stack
(release:dev, no NODE_ENV) - minimal change, prompt cache reload only.
"""
import subprocess
import os

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\assets\aihot-poc\AIHOT\apps\worker"
LOG = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\assets\aihot-poc\worker-r1887.log"
ERR = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\data\assets\aihot-poc\worker-r1887-err.log"

# Pre-open logs with append so the detached child never inherits our shell pipes.
out = open(LOG, "ab")
err = open(ERR, "ab")
env = dict(os.environ)  # no NODE_ENV -> matches running stack (release:dev)
p = subprocess.Popen(
    ["node", "--env-file-if-exists=../../.env", "src/main.ts"],
    cwd=ROOT,
    env=env,
    stdout=out,
    stderr=err,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    close_fds=True,
)
print("WORKER-START pid=%d log=%s" % (p.pid, LOG))
