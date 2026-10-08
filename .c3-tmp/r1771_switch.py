# -*- coding: utf-8 -*-
import io, os, subprocess, time, shutil

BASE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
POC = os.path.join(BASE, r"data\assets\aihot-poc")
ENVF = os.path.join(POC, "AIHOT", ".env")
out = []
def w(s): out.append(str(s))
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, **kw)
    return r.stdout.decode("utf-8", errors="replace").strip(), r.stderr.decode("utf-8", errors="replace").strip(), r.returncode

w("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))

# 1. derive qwen2.5:14b-8k (layer-shared, no serve restart; R1769 pattern)
o, e, rc = run(["ollama", "create", "qwen2.5:14b-8k", "-f", "-"],
               input=b"FROM qwen2.5:14b\nPARAMETER num_ctx 8192\n")
w("ollama_create rc=%s out=%s err=%s" % (rc, o[:120], e[:120]))

# 2. rewrite .env LLM_MODEL (python rewrite, R1710 op-red rule)
txt = io.open(ENVF, encoding="utf-8").read()
lines = txt.splitlines()
changed = 0
for i, l in enumerate(lines):
    if l.startswith("LLM_MODEL="):
        lines[i] = "LLM_MODEL=qwen2.5:14b-8k"
        changed += 1
io.open(ENVF, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
w("env_llm_model_changed=%d" % changed)

# 3. kill worker 68636
o, e, rc = run(["taskkill", "/PID", "68636", "/F"])
w("taskkill rc=%s %s %s" % (rc, o[:80], e[:80]))

# 4. start new worker (python direct-start, DETACHED|CREATE_NEW_PROCESS_GROUP, worker2.log append)
node = shutil.which("node")
wlog = open(os.path.join(POC, "worker2.log"), "ab")
DETACHED = 0x00000008
NEWGROUP = 0x00000200
env = dict(os.environ)
env["NODE_ENV"] = "production"
p = subprocess.Popen([node, "--env-file-if-exists=../../.env", "src/main.ts"],
                     cwd=os.path.join(POC, "AIHOT", "apps", "worker"),
                     env=env, stdout=wlog, stderr=wlog,
                     creationflags=DETACHED | NEWGROUP, close_fds=True)
w("worker_new_pid=%s" % p.pid)

# 5. verify
time.sleep(18)
time.sleep(0)
alive = None
try:
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "(Get-Process -Id %d -ErrorAction SilentlyContinue) -ne $null" % p.pid],
                       capture_output=True)
    alive = r.stdout.decode("utf-8", errors="replace").strip()
except Exception as ex:
    alive = "check_err:%s" % str(ex)[:60]
w("worker_alive=%s" % alive)
tail = io.open(os.path.join(POC, "worker2.log"), "rb").read()[-900:].decode("utf-8", errors="replace")
w("worker2.log tail:\n%s" % tail)

io.open(os.path.join(BASE, r".c3-tmp\r1771_switch.txt"), "w", encoding="utf-8").write("\n".join(out))
print("switch done")
