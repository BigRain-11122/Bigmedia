#!/usr/bin/env python3
"""MV sprint active-window static probe (tech#84).

Gap anchor (tech#82 yield-discipline follow-up): the eviction-aware
opt-in faces on ollama_probe (--eviction-aware) and gpu_window_gate
(--eviction-aware-mb) are passed only when the lanes owning the
resident models are judged non-active -- but that "MV sprint active?"
judgment was episodic executor intuition re-derived by hand every round
from scattered mtimes (the tech#82 help text says so verbatim: "the
judgment position passes the flag ONLY when the lanes owning the
resident models are judged non-active"). This probe mechanizes that
judgment as a write-silence reading:

  faces (any one fresh => active; the MV session writes no busy marker
  by contract -- activity is derived from file writes only, so renders
  / lookboards / frames landing on disk ARE the busy signal):
    repo-mv-dirty  git-dirty/untracked files whose path mentions an MV
                   domain token (mv0001 / mv001), newest mtime
    mv-outbound    newest mtime under the mv0001-handover outbound root
                   (krea2/, 30s-reel-v1/, ...)
    h3-outbound    newest mtime under the h3-local-test outbound root
                   (the mv0001 H3 video lane)

  Verdict: newest readable face age < --threshold-min => active, else
  quiet. Default threshold 90 min: the MV full-track sprint's known
  natural silence ceiling is the bm-c receipt monitor cadence (cron
  7-57 min poll + 60-min poke), so 90 min of silence on ALL faces means
  no scheduled receipt-wait is in flight either.

  rc contract (consumers gate on rc, not on parsing):
    0 = quiet  (MV lanes non-active; eviction credit admissible)
    1 = active (yield discipline: keep skips, no eviction credit)
    2 = error  (no readable face, or any unreadable face -- fail-closed:
                a missing reading must never read as quiet)

  Shared-infra files written by the sprint (whisper-ledger.jsonl, ASR
  noise dicts) carry no MV token and never count as lane activity:
  those surfaces are written by any lane, so crediting them would make
  every lane look like MV. Kinship: loop_health._parse_porcelain_z
  (tech#31) -- the 12-line NUL parser is kept local so the probe family
  stays standalone (each probe owns its own locked seams).
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FLUXGROUP_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_THRESHOLD_MIN = 90
MV_DOMAIN_TOKENS = ("mv0001", "mv001")
MV_OUTBOUND_ROOT = FLUXGROUP_ROOT / "cph4" / "fleet" / "mv0001-handover" / "outbound"
H3_OUTBOUND_ROOT = FLUXGROUP_ROOT / "cph4" / "fleet" / "h3-local-test" / "outbound"
GIT_TIMEOUT_S = 20

RC_QUIET = 0
RC_ACTIVE = 1
RC_ERROR = 2


def parse_porcelain_z_paths(data):
    """`git status --porcelain -z` stdout bytes -> [relpath]. -z records
    are NUL-separated with no path quoting (raw UTF-8 bytes); a
    rename/copy record is followed by a second NUL field holding the
    old path, which is skipped. Short/garbled chunks never crash."""
    paths, skip_next = [], False
    for chunk in data.split(b"\0"):
        if not chunk:
            continue
        if skip_next:
            skip_next = False
            continue
        if len(chunk) < 4:
            continue
        xy = chunk[:2]
        if b"R" in xy or b"C" in xy:
            skip_next = True
        paths.append(chunk[3:].decode("utf-8", "replace"))
    return paths


def filter_mv_domain(paths, tokens=MV_DOMAIN_TOKENS):
    """[relpath] -> [relpath] mentioning an MV domain token. Substring
    (not prefix) on purpose: the sprint's write surface spans
    data/storylines/drama/mv0001/, data/sources/mv001/ and any future
    sibling path that carries the domain name; token-free shared-infra
    files (whisper-ledger, noise dicts) never count."""
    return [p for p in paths if any(t in p for t in tokens)]


def _real_git_status(root):
    """Real seam: -> (ok, stdout_bytes). ok=False on any git failure
    (missing binary, not a work tree, timeout) -- the face goes
    unreadable, never silently empty (fail-closed contract)."""
    try:
        p = subprocess.run(
            ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
            cwd=str(root), capture_output=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return False, b""
    if p.returncode != 0:
        return False, b""
    return True, p.stdout


def collect_repo_face(repo_root, git_runner=None):
    """git-dirty MV-domain face -> {status, mtime, path}.

    status: 'ok' (newest mtime among existing MV-domain dirty files),
    'empty' (tree clean of MV-domain dirty files -- a legitimate state
    after a batch commit; carries no signal either way), 'unreadable'
    (git failed -- fail-closed). git_runner is the test injection seam
    (real seam = _real_git_status)."""
    runner = git_runner or _real_git_status
    ok, stdout = runner(repo_root)
    if not ok:
        return {"status": "unreadable"}
    paths = filter_mv_domain(parse_porcelain_z_paths(stdout))
    if not paths:
        return {"status": "empty"}
    newest_t, newest_p = None, None
    for rel in paths:
        try:
            t = (Path(repo_root) / rel).stat().st_mtime
        except OSError:
            continue  # deleted between status and stat: no signal
        if newest_t is None or t > newest_t:
            newest_t, newest_p = t, rel
    if newest_t is None:
        return {"status": "empty"}
    return {"status": "ok", "mtime": newest_t, "path": newest_p}


def scan_dir_newest(root):
    """Recursive newest (mtime, relpath) under root.

    -> (None, None) when the root is absent (legitimate absent face --
    no signal, not an error); (root, None) when the walk itself fails
    (unreadable); (mtime, relpath) normal. An existing-but-empty tree
    yields (None, 'empty') so callers can tell it from absent."""
    root = Path(root)
    if not root.is_dir():
        return None, None
    newest_t, newest_p = None, None
    try:
        for cur, dirs, files in os.walk(str(root)):
            for f in files:
                p = os.path.join(cur, f)
                try:
                    t = os.path.getmtime(p)
                except OSError:
                    continue
                if newest_t is None or t > newest_t:
                    newest_t, newest_p = t, os.path.relpath(p, str(root))
    except OSError:
        return str(root), None
    if newest_t is None:
        return None, "empty"
    return newest_t, newest_p


def scan_outbound_face(root):
    """Outbound-root face -> {status, mtime, path} (wraps
    scan_dir_newest). 'ok' = newest write readable; 'empty' = dir exists
    with no files; 'absent' = root missing (no signal); 'unreadable' =
    walk failed (fail-closed)."""
    t, p = scan_dir_newest(root)
    if t is None and p is None:
        return {"status": "absent"}
    if p is None or t is None:
        # (root, None) = walk error; (None, 'empty') = no files
        return {"status": "unreadable" if p == str(root) else "empty"}
    return {"status": "ok", "mtime": t, "path": p}


def compute_verdict(faces, now_ts, threshold_min):
    """Pure core: {name: face} -> (verdict, newest_age_min, has_error).

    verdict 'active' when any 'ok' face is younger than threshold_min,
    'quiet' when every 'ok' face is at/older, None when NO face is
    'ok' (no attestation either way). 'empty'/'absent' faces carry no
    signal; any 'unreadable' face sets has_error (fail-closed: rc 2
    even when the readable faces would say quiet)."""
    has_error = any(f.get("status") == "unreadable" for f in faces.values())
    ages = []
    for f in faces.values():
        if f.get("status") == "ok":
            ages.append(max(0.0, (now_ts - f["mtime"]) / 60.0))
    if not ages:
        return None, None, has_error
    newest = min(ages)
    verdict = "active" if newest < threshold_min else "quiet"
    return verdict, newest, has_error


def run_probe(repo_root=None, face_roots=None, threshold_min=DEFAULT_THRESHOLD_MIN,
              now=None, git_runner=None):
    """Compose the three faces and the verdict.

    -> result dict (probe/ts/verdict/rc/threshold_min/newest_age_min/
    faces). face_roots overrides the two outbound canonical roots
    ({'mv-outbound': path, 'h3-outbound': path}) for hermetic tests."""
    repo_root = Path(repo_root or REPO_ROOT)
    roots = {"mv-outbound": MV_OUTBOUND_ROOT, "h3-outbound": H3_OUTBOUND_ROOT}
    if face_roots:
        roots.update(face_roots)
    now_dt = now or datetime.datetime.now()
    now_ts = now_dt.timestamp()

    faces = {"repo-mv-dirty": collect_repo_face(repo_root, git_runner=git_runner)}
    for name, root in roots.items():
        faces[name] = scan_outbound_face(root)

    verdict, newest, has_error = compute_verdict(faces, now_ts, threshold_min)
    if verdict is None or has_error:
        rc = RC_ERROR
    else:
        rc = RC_ACTIVE if verdict == "active" else RC_QUIET
    return {
        "probe": "mv_sprint_probe",
        "ts": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "verdict": verdict,
        "rc": rc,
        "threshold_min": threshold_min,
        "newest_age_min": (round(newest, 1) if newest is not None else None),
        "faces": faces,
    }


def _face_json(face, now_ts):
    out = {"status": face.get("status")}
    if face.get("status") == "ok":
        out["age_min"] = round(max(0.0, (now_ts - face["mtime"]) / 60.0), 1)
        out["path"] = face.get("path")
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="MV sprint active-window static probe (tech#84): "
                    "write-silence verdict for the eviction-aware yield "
                    "discipline. rc 0=quiet, 1=active, 2=error.")
    parser.add_argument("--threshold-min", type=float, default=DEFAULT_THRESHOLD_MIN,
                        help="silence minutes at/over which every readable "
                             "face counts as quiet (default %d; the bm-c "
                             "receipt monitor cadence 7-57 min + 60-min "
                             "poke ceiling sits under it)" % DEFAULT_THRESHOLD_MIN)
    parser.add_argument("--json", action="store_true",
                        help="single machine-readable line")
    args = parser.parse_args(argv)

    result = run_probe(threshold_min=args.threshold_min)
    now_ts = datetime.datetime.now().timestamp()
    if args.json:
        payload = dict(result)
        payload["faces"] = {n: _face_json(f, now_ts)
                            for n, f in result["faces"].items()}
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print("mv_sprint_probe %s: verdict=%s rc=%d threshold=%.0fmin" % (
            result["ts"], result["verdict"], result["rc"], args.threshold_min))
        for n, f in result["faces"].items():
            fj = _face_json(f, now_ts)
            if fj["status"] == "ok":
                print("  %-14s age=%8.1fmin  %s" % (n, fj["age_min"], fj["path"]))
            else:
                print("  %-14s %s" % (n, fj["status"]))
        if result["verdict"] == "quiet":
            print("yield discipline: MV lanes non-active -- eviction credit "
                  "admissible (pair with the GPU hardware gate GO)")
        elif result["verdict"] == "active":
            print("yield discipline: MV lanes active -- keep skips, no "
                  "eviction credit this window")
        else:
            print("fail-closed: no readable face (or unreadable face) -- "
                  "a missing reading must never read as quiet")
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
