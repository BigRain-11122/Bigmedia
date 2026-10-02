# -*- coding: utf-8 -*-
# Run the full test suite and print a pure-ASCII verdict (GBK-console safe).
import io, sys, unittest, contextlib

loader = unittest.TestLoader()
suite = loader.discover("tests")
buf = io.StringIO()
runner = unittest.TextTestRunner(stream=buf, verbosity=0)
res = runner.run(suite)
print("tests=%d failures=%d errors=%d skipped=%d" % (
    res.testsRun, len(res.failures), len(res.errors), len(res.skipped)))
for t, _ in res.failures:
    print("FAIL:", t)
for t, _ in res.errors:
    print("ERROR:", t)
print("VERDICT:", "GREEN" if (not res.failures and not res.errors) else "RED")
