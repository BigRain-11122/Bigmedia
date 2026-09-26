# -*- coding: utf-8 -*-
"""R443 smoke: wording gate on real production beats (BS-004 v6).

Writes findings to .c3-tmp/r443_plc_smoke.txt in UTF-8 (console capture
is unreliable on the GBK console - evidence must land in a file first).
"""
import contextlib
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

import plain_language_check as plc  # noqa: E402

beats = REPO / "data" / "sources" / "bs004" / "voiceover-v6.beats.txt"
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = plc.main(["--beats", str(beats)])
out = buf.getvalue()
(REPO / ".c3-tmp" / "r443_plc_smoke.txt").write_text(out, encoding="utf-8")
print("smoke rc=%d bytes=%d" % (rc, len(out.encode("utf-8"))))
