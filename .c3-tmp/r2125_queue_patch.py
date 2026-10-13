"""R2125 queue patch: insert tech#126 execution note + append tech#148 seed.

Content lives in UTF-8 side files (encoding law: script ASCII, Chinese
only in data files). Fail-closed: refuses if any anchor is missing or
already applied (idempotent guard).
"""
import io
import sys

QUEUE = "state/queue/tech.md"
NOTE_FILE = ".c3-tmp/r2125_t126_note.txt"
ITEM_FILE = ".c3-tmp/r2125_t148_item.txt"
NOTE_KEY = "R2125 执行注记"
ITEM_KEY = "148. [R2125 补货"

def read_utf8(path):
    with io.open(path, "r", encoding="utf-8-sig", errors="strict") as fh:
        return fh.read()

def main():
    text = read_utf8(QUEUE)
    note = read_utf8(NOTE_FILE).rstrip("\n")
    item = read_utf8(ITEM_FILE).rstrip("\n")
    if NOTE_KEY in text:
        print("ANCHOR-ALREADY-APPLIED note; refusing (idempotent)")
        return 2
    if ITEM_KEY in text:
        print("ANCHOR-ALREADY-APPLIED item; refusing (idempotent)")
        return 2
    lines = text.splitlines()
    idx126 = [i for i, l in enumerate(lines) if l.startswith("126.")]
    if len(idx126) != 1:
        print("ANCHOR-MISSING 126 line count=%d" % len(idx126))
        return 2
    insert_at = idx126[0] + 1
    lines.insert(insert_at, note)
    # append the new item before end, keep trailing newline structure
    while lines and lines[-1] == "":
        lines.pop()
    lines.append(item)
    out = "\n".join(lines) + "\n"
    with io.open(QUEUE, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print("QUEUE-PATCHED insert@%d append#148 lines=%d" % (insert_at, len(lines)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
