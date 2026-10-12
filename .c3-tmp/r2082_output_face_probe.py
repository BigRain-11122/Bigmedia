"""R2082 tech#139 observation probe: ComfyUI output tree fresh entries with depth tags.

Question (tech#139): during the night MV wave, does a real TWO-LEVEL deep
write (output/<a>/<b>/file) land on THIS machine's output tree (exercising
the tech#138 depth-2 face), or is the wave one-level only (kf_bma/*.png)?
"""
import os
import time

D = r'C:\Users\sjs20\comfyui-krea\ComfyUI_windows_portable\ComfyUI\output'
R = 900  # recency window (matches probe default)


def main():
    now = time.time()
    fresh = []

    def walk(base, depth, prefix):
        try:
            entries = list(os.scandir(base))
        except OSError:
            return
        for e in entries:
            try:
                m = e.stat(follow_symlinks=False).st_mtime
            except OSError:
                continue
            age = now - m
            p = prefix + e.name
            if e.is_dir(follow_symlinks=False):
                if age <= R:
                    fresh.append((age, p + "/", "FRESH dir L%d" % (depth + 1)))
                elif depth < 1:
                    walk(e.path, depth + 1, p + "/")
            else:
                if age <= R:
                    fresh.append((age, p, "FRESH file"))

    walk(D, 0, "")
    fresh.sort()
    for age, p, t in fresh[:14]:
        print("%7.0fs  %-14s %s" % (age, t, p))
    print("total fresh:", len(fresh))


if __name__ == "__main__":
    main()
