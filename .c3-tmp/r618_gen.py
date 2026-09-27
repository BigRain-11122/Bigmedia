# r618_gen.py -- generate R618 probe-family scripts from R617 templates
# generation law (R612/R615): global r617->r618 FIRST (prevents double-hit),
# then baseline name r616_lednew5->r617_lednew5; verify number expectations updated in sync.
import io, os

TMP = os.path.dirname(os.path.abspath(__file__))

def rd(name):
    with io.open(os.path.join(TMP, name), encoding='utf-8') as fh:
        return fh.read()

def wr(name, text):
    with io.open(os.path.join(TMP, name), 'w', encoding='utf-8') as fh:
        fh.write(text)
    print('GEN %s' % name)

# 1) r618_all.py
t = rd('r617_all.py')
t = t.replace('r617', 'r618')  # global first
t = t.replace("'r616_lednew5.txt'", "'r617_lednew5.txt'")  # then baseline name
t = t.replace('# generation law (R612): global r616->r618 first, then baseline name r615_lednew5->r616_lednew5',
              '# generation law (R612): global r617->r618 first, then baseline name r616_lednew5->r617_lednew5')
wr('r618_all.py', t)

# 2) r618_probes.py
t = rd('r617_probes.py')
t = t.replace('r617', 'r618')
wr('r618_probes.py', t)

# 3) r618_verify.py (filename replace + number expectations in sync, per R615 addendum law)
t = rd('r617_verify.py')
t = t.replace('r617', 'r618')
t = t.replace('u"\u65b0\u7a97 3/6=R615-R620" in log[-1]', 'u"\u65b0\u7a97 4/6=R615-R620" in log[-1]')
t = t.replace('len(log) >= 641', 'len(log) >= 642')
t = t.replace('("FOCUS_WINDOW_4_6", "R615-R620" in focus and u"\u7a97 4/6" in focus)',
              '("FOCUS_WINDOW_5_6", "R615-R620" in focus and u"\u7a97 5/6" in focus)')
t = t.replace('u"3/6" in osrow', 'u"4/6" in osrow')
wr('r618_verify.py', t)
print('GEN_DONE')
