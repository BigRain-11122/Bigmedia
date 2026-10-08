import subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
platform = "B\u7ad9"  # B站, CJK name law (playbook single source of truth)
r = subprocess.run([sys.executable, "src/platform_spec_check.py",
                    "--video", "output/renders/md-0001-v1-bilibili-16x9.mp4",
                    "--platform", platform],
                   capture_output=True)
print(r.stdout.decode('utf-8', errors='replace'))
print('RC', r.returncode)
