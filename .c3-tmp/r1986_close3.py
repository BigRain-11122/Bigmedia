# -*- coding: utf-8 -*-
"""R1986 stage B close (broken-round successor body): finalize_state +
commit state.json with close scripts self-included (tech#81). Stage A
already landed manually (9e6e65a8) after the .c3-tmp/*.log gitignore
abort; fulltest.log cannot be committed (gitignored) so it is removed -
its 1012-green summary is carried by r1986_fire_diag.txt section [6]."""
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "src", "os")))

from close_commit import finalize_state, run_close_commit  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "r1986_close2", os.path.join(_HERE, "r1986_close2.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
LOG_LINE, FOCUS = mod.LOG_LINE, mod.FOCUS


def main():
    lg = ".c3-tmp/r1986_fulltest.log"
    if os.path.exists(lg):
        os.remove(lg)
        print("removed fulltest.log (gitignored; summary in fire_diag)")
    summary = finalize_state(log_line=LOG_LINE, focus=FOCUS)
    print("finalize tick=%s ts=%s wm_added=%s orders_wm_rows=%s log_len=%s"
          % (summary["tick"], summary["ts"], summary["wm_added"],
             summary["orders_wm_rows"], summary["log_len"]))
    rc_b, lines_b = run_close_commit(
        files=["src/os/state.json", ".c3-tmp/r1986_close2.py",
               ".c3-tmp/r1986_close3.py"],
        message=(
            "R1986 loop close: production round - fire GO 16:40:56 "
            "consumed, window slammed mid-flight (ComfyUI 100%/11.8GB, "
            "llama-server evicted, 8-token probe 92s timeout = GPU- "
            "starvation family, yield law correct side, no restart); "
            "SC-005-04 S1 four fired calls zero verdicts (not passed, "
            "next fire window relaunch with tech#106 liveness face "
            "first); SC-005-05/06 + DIGEST v18 GPU tails remain gated; "
            "fresh card 17:08:45 no-fire; probes board 0F / readiness 3 "
            "external blockers 0 findings / loop_health 2F adjudicated "
            "historical [via bm-a]"
        ),
    )
    for ln in lines_b:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage B rc=%s" % rc_b)
    return rc_b


if __name__ == "__main__":
    sys.exit(main())
