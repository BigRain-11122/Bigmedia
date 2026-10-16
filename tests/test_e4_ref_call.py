# -*- coding: utf-8 -*-
"""Hermetic tests for src/e4_ref_call.py (tech#180 leg-2 / tech#63 ②).

The shell's anti-drift law is the test's chief object: the prompt
contract and the auto-ledger machinery must come from the generator
(e4_launcher_gen), so several tests assert the import/execution
delegation rather than re-stating the contract.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, '..', 'src'))
sys.path.insert(0, os.path.join(_HERE, '..', 'src', 'os'))

import e4_launcher_gen as gen  # noqa: E402
import e4_ref_call as shell  # noqa: E402

PY = sys.executable or 'python'
TOOL = os.path.join(_HERE, '..', 'src', 'e4_ref_call.py')

# tech#175: the real pre-run urllib faces, captured at module import --
# the teardown-hygiene lock asserts they survive every test class.
PRE_URLLIB = sys.modules.get('urllib')
PRE_URLLIB_REQUEST = sys.modules.get('urllib.request')


class AssemblyAndLabelTests(unittest.TestCase):
    def test_assemble_prompt_delegates_to_generator(self):
        body = u'角色+卡面描述+背景叙事。'
        got = shell.assemble_prompt(body, gen.CANONICAL_QUESTIONS)
        self.assertEqual(got, gen.build_prompt(body, gen.CANONICAL_QUESTIONS))
        self.assertTrue(got.startswith(body + u'\n'))
        self.assertIn(gen.QUESTION_MARKER, got)

    def test_double_append_guard_raises(self):
        with self.assertRaises(gen.UsageError):
            shell.assemble_prompt(u'正文 请回答三个问题 误嵌',
                                  gen.CANONICAL_QUESTIONS)

    def test_default_label_strips_tmp_suffix(self):
        self.assertEqual(
            shell.default_label(os.path.join(
                'repo', 'data', 'storylines', 'cards',
                'MC-20261016-REACT-v22-tmp', 'e4-body.txt')),
            'MC-20261016-REACT-v22')

    def test_default_label_plain_dir(self):
        self.assertEqual(
            shell.default_label(os.path.join('a', 'b', 'e4-body.txt')),
            'b')

    def test_default_label_root_file_fallback(self):
        # drive-root prompt file: empty parent -> file stem
        self.assertEqual(shell.default_label('C:\\body.txt'), 'body')


class LedgerBlockRenderTests(unittest.TestCase):
    def test_block_substituted_with_e4_seat_identity(self):
        src = shell.render_ledger_block()
        self.assertIn("EXPERT_ID = 'E4-audience'", src)
        self.assertNotIn('__EXPERT_ID__', src)
        self.assertNotIn('__ROLE_DEPT_EXPR__', src)
        self.assertIn(repr(gen.E4_ROLE_DEPT), src)

    def test_block_is_the_generator_source(self):
        # the exec'd block IS the generator's block (single source):
        # both tech#173 ledger + tech#174 stage markers present.
        src = shell.render_ledger_block()
        raw = gen.AUTO_LEDGER_BLOCK
        self.assertIn('_auto_ledger(', src)
        self.assertIn('_auto_stage_result()', src)
        self.assertIn('tech#173', src)
        self.assertIn('tech#174', src)
        self.assertEqual(
            src,
            raw.replace('__EXPERT_ID__', repr(gen.E4_EXPERT_ID))
               .replace('__ROLE_DEPT_EXPR__', repr(gen.E4_ROLE_DEPT)))


class CliUsageTests(unittest.TestCase):
    """In-process rc2 paths (no HTTP is ever reached on these)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='e4ref_')

    def _write(self, name, text):
        path = os.path.join(self.tmp, name)
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        return path

    def _main(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = shell.main(list(argv))
        return rc, buf.getvalue()

    def test_rc2_missing_prompt_file(self):
        rc, out = self._main('--prompt-file',
                             os.path.join(self.tmp, 'nope.txt'))
        self.assertEqual(rc, 2)
        self.assertIn('USAGE-ERROR', out)

    def test_rc2_empty_body(self):
        body = self._write('empty.txt', '  \n ')
        rc, out = self._main('--prompt-file', body)
        self.assertEqual(rc, 2)
        self.assertIn('empty', out)

    def test_rc2_body_already_has_questions(self):
        body = self._write('body.txt', u'叙事 请回答三个问题 误嵌')
        rc, out = self._main('--prompt-file', body)
        self.assertEqual(rc, 2)
        self.assertIn('question block', out)

    def test_rc2_missing_questions_file(self):
        body = self._write('body.txt', u'叙事。')
        rc, out = self._main('--prompt-file', body, '--questions-file',
                             os.path.join(self.tmp, 'noq.txt'))
        self.assertEqual(rc, 2)

    def test_rc2_bad_timeout(self):
        body = self._write('body.txt', u'叙事。')
        rc, out = self._main('--prompt-file', body, '--timeout', '0')
        self.assertEqual(rc, 2)
        self.assertIn('positive', out)

    def test_cli_no_args_rc2(self):
        p = subprocess.run([PY, TOOL], stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=60)
        self.assertEqual(p.returncode, 2)


class RefCallBehaviorTests(unittest.TestCase):
    """tech#169 CPU-lane shell behavior, exec-fresh with fake urllib
    (both keys installed before exec -- the family pattern)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='e4refb_')
        self.repo = os.path.join(self.tmp, 'repo')
        self.item = os.path.join(self.repo, 'data', 'storylines',
                                 'cards', 'x-tmp')
        os.makedirs(os.path.join(self.repo, '.git'))
        os.makedirs(self.item)
        self.body = os.path.join(self.item, 'e4-body.txt')
        with io.open(self.body, 'w', encoding='utf-8') as fh:
            fh.write(u'角色：E4 直觉观众参考仪。\n卡面八行 verbatim。\n')
        # tech#175: BOTH keys the fakes install must be saved/restored
        self.saved = {k: sys.modules.get(k)
                      for k in ('urllib', 'urllib.request')}
        self.captured = []

    def tearDown(self):
        for key, mod in self.saved.items():
            if mod is None:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = mod

    def _exec_shell(self, mode, argv):
        """Exec the shell fresh with fake urllib pre-installed, then
        call main(argv). Returns (rc, stdout, last_generate_payload)."""
        this = self

        class _Resp(object):
            def __init__(self, payload):
                self._payload = payload

            def read(self):
                return self._payload

        class _Req(object):
            def __init__(self, url, data=None, headers=None):
                self.url = url
                self.data = data
                this.captured.append(self)

        @contextlib.contextmanager
        def _urlopen(req_or_url, timeout=None):
            if isinstance(req_or_url, str):
                if mode == 'liveness-fail':
                    raise Exception('ConnectionRefusedError: dead server')
                yield _Resp(b'{"status": "ok"}')
            else:
                if mode == 'gen-timeout':
                    raise Exception('The read operation timed out')
                if mode == 'gen-transport':
                    raise Exception('HTTP Error 404: model not found')
                if mode == 'gen-empty':
                    yield _Resp(
                        b'{"choices": [{"message": '
                        b'{"content": "   \\n"}}]}')
                else:
                    yield _Resp(
                        b'{"choices": [{"message": '
                        b'{"content": "8.0\\nverdict line"}}]}')

        urllib_mod = types.ModuleType('urllib')
        request_mod = types.ModuleType('urllib.request')
        request_mod.Request = _Req
        request_mod.urlopen = _urlopen
        urllib_mod.request = request_mod
        sys.modules['urllib'] = urllib_mod
        sys.modules['urllib.request'] = request_mod

        buf = io.StringIO()
        code = compile(io.open(TOOL, encoding='utf-8').read(),
                       TOOL, 'exec')
        ns = {'__file__': TOOL, '__name__': 'e4_ref_call_under_test'}
        with contextlib.redirect_stdout(buf):
            exec(code, ns)
            rc = ns['main'](list(argv))
        payload = None
        for req in self.captured:
            if getattr(req, 'data', None):
                payload = json.loads(req.data.decode('utf-8'))
        return rc, buf.getvalue(), payload

    def test_success_verdict_five_keys_and_brain_wire_law(self):
        rc, out, payload = self._exec_shell(
            'ok', ['--prompt-file', self.body])
        self.assertEqual(rc, 0, out)
        self.assertIn('DONE', out)
        self.assertIn('LEDGER-ROW E4-audience', out)
        # tech#186 OpenAI wire law: brain default model + messages
        # shape + thinking-off + NO server-owned options block
        self.assertEqual(payload['model'], 'qwen3.6-35b')
        self.assertFalse(payload['stream'])
        self.assertEqual(payload['chat_template_kwargs'],
                         {'enable_thinking': False})
        self.assertNotIn('options', payload)
        self.assertNotIn('think', payload)
        content = payload['messages'][0]['content']
        self.assertTrue(content.startswith(
            u'角色：E4 直觉观众参考仪。\n卡面八行 verbatim。\n'))
        self.assertIn(gen.QUESTION_MARKER, content)
        # five-key result json parity (R2261 audit shape)
        with io.open(os.path.join(self.item, 'e4-result.json'),
                     encoding='utf-8') as fh:
            result = json.load(fh)
        self.assertEqual(set(result.keys()),
                         {'ts', 'model', 'material', 'lane', 'verdict'})
        self.assertEqual(result['lane'], 'cpu')
        self.assertEqual(result['model'], 'qwen3.6-35b')
        self.assertEqual(result['verdict'], '8.0\nverdict line')

    def test_default_label_from_item_dir(self):
        rc, out, _ = self._exec_shell('ok', ['--prompt-file', self.body])
        self.assertEqual(rc, 0)
        with io.open(os.path.join(self.item, 'e4-result.json'),
                     encoding='utf-8') as fh:
            result = json.load(fh)
        self.assertEqual(result['material'], 'x')  # 'x-tmp' -> 'x'
        ledger = io.open(os.path.join(self.repo, 'docs', 'reviews',
                                      'expert-calls.md'),
                         encoding='utf-8').read()
        self.assertIn('| x | 0 |', ledger)

    def test_label_override(self):
        rc, out, _ = self._exec_shell(
            'ok', ['--prompt-file', self.body, '--label', 'MC-X-180'])
        self.assertEqual(rc, 0)
        with io.open(os.path.join(self.item, 'e4-result.json'),
                     encoding='utf-8') as fh:
            result = json.load(fh)
        self.assertEqual(result['material'], 'MC-X-180')

    def test_questions_file_override_payload(self):
        qf = os.path.join(self.tmp, 'custom_q.txt')
        with io.open(qf, 'w', encoding='utf-8') as fh:
            fh.write(u'请回答三个问题（自定义形态）：\n1) Q1？')
        rc, out, payload = self._exec_shell(
            'ok', ['--prompt-file', self.body,
                   '--questions-file', qf])
        self.assertEqual(rc, 0, out)
        self.assertIn(u'请回答三个问题（自定义形态）',
                      payload['messages'][0]['content'])
        self.assertNotIn(u'指出原句',
                         payload['messages'][0]['content'])

    def test_liveness_fail_rc3_no_result(self):
        rc, out, _ = self._exec_shell(
            'liveness-fail', ['--prompt-file', self.body])
        self.assertEqual(rc, 3)
        self.assertIn('LIVENESS-FAIL', out)
        self.assertFalse(os.path.isfile(
            os.path.join(self.item, 'e4-result.json')))

    def test_transport_error_rc3_no_result(self):
        rc, out, _ = self._exec_shell(
            'gen-transport', ['--prompt-file', self.body])
        self.assertEqual(rc, 3)
        self.assertIn('TRANSPORT-ERROR', out)
        self.assertFalse(os.path.isfile(
            os.path.join(self.item, 'e4-result.json')))

    def test_timeout_verdict_rc0(self):
        rc, out, _ = self._exec_shell(
            'gen-timeout', ['--prompt-file', self.body])
        self.assertEqual(rc, 0)
        self.assertIn('TIMEOUT', out)
        with io.open(os.path.join(self.item, 'e4-result.json'),
                     encoding='utf-8') as fh:
            result = json.load(fh)
        self.assertEqual(result['verdict'], 'TIMEOUT-1500s')

    def test_empty_response_verdict_rc0(self):
        rc, out, _ = self._exec_shell(
            'gen-empty', ['--prompt-file', self.body])
        self.assertEqual(rc, 0)
        self.assertIn('DONE', out)
        with io.open(os.path.join(self.item, 'e4-result.json'),
                     encoding='utf-8') as fh:
            result = json.load(fh)
        self.assertEqual(result['verdict'], 'EMPTY-RESPONSE')

    def test_no_repo_root_warn_ledger_skipped_verdict_kept(self):
        # prompt outside any repo: WARN skip, rc 0, result still lands
        orphan_dir = tempfile.mkdtemp(prefix='e4orphan_')
        orphan_body = os.path.join(orphan_dir, 'e4-body.txt')
        with io.open(orphan_body, 'w', encoding='utf-8') as fh:
            fh.write(u'orphan narrative.')
        rc, out, _ = self._exec_shell('ok', ['--prompt-file', orphan_body])
        self.assertEqual(rc, 0)
        self.assertIn('WARN auto-ledger skipped', out)
        self.assertTrue(os.path.isfile(
            os.path.join(orphan_dir, 'e4-result.json')))

    def test_ledger_row_and_archive_written(self):
        rc, out, _ = self._exec_shell('ok', ['--prompt-file', self.body])
        self.assertEqual(rc, 0)
        self.assertIn('LEDGER-ROW E4-audience', out)
        ledger = io.open(os.path.join(self.repo, 'docs', 'reviews',
                                      'expert-calls.md'),
                         encoding='utf-8').read()
        self.assertIn('| E4-audience |', ledger)
        self.assertIn(u'｜ 8.0', ledger)  # fullwidth-pipe note + first line
        vdir = os.path.join(self.repo, 'docs', 'reviews',
                            'expert-verdicts')
        names = sorted(os.listdir(vdir))
        self.assertEqual(len(names), 1)
        self.assertTrue(names[0].endswith('-E4-audience.md'))
        body = io.open(os.path.join(vdir, names[0]),
                       encoding='utf-8').read()
        self.assertIn(u'结论全文', body)
        self.assertIn('verdict line', body)
        self.assertIn('tech#173', body)


class StageBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.saved = {k: sys.modules.get(k)
                      for k in ('urllib', 'urllib.request')}

    def tearDown(self):
        for key, mod in self.saved.items():
            if mod is None:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = mod

    def test_auto_stage_stages_result_json_in_real_repo(self):
        # tech#174 born-level: in a REAL git repo the raw verdict json
        # self-stages into the index at landing (the shell execs the
        # same shared block, so the R2261 residue class dies here too).
        real = tempfile.mkdtemp(prefix='e4refstage_')
        try:
            p = subprocess.run(
                ['git', 'init', '-q', real], stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=60)
            self.assertEqual(p.returncode, 0, p.stdout)
            item = os.path.join(real, 'data', 'storylines', 'cards',
                                'x-tmp')
            os.makedirs(item)
            body = os.path.join(item, 'e4-body.txt')
            with io.open(body, 'w', encoding='utf-8') as fh:
                fh.write(u'staging narrative.')

            class _Resp(object):
                @staticmethod
                def read():
                    return (b'{"choices": [{"message": '
                            b'{"content": "9.0"}}]}')

            class _Req(object):
                def __init__(self, *a, **k):
                    pass

            @contextlib.contextmanager
            def _urlopen(*a, **k):
                yield _Resp()

            urllib_mod = types.ModuleType('urllib')
            request_mod = types.ModuleType('urllib.request')
            request_mod.Request = _Req
            request_mod.urlopen = _urlopen
            urllib_mod.request = request_mod
            sys.modules['urllib'] = urllib_mod
            sys.modules['urllib.request'] = request_mod
            buf = io.StringIO()
            code = compile(io.open(TOOL, encoding='utf-8').read(),
                           TOOL, 'exec')
            ns = {'__file__': TOOL, '__name__': 'e4_ref_call_under_test'}
            with contextlib.redirect_stdout(buf):
                exec(code, ns)
                rc = ns['main'](['--prompt-file', body])
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertIn('DONE', buf.getvalue())
            raw = os.path.join(item, 'e4-result.json')
            self.assertIn('STAGED-RESULT %s (tech#174 auto-stage)'
                          % os.path.relpath(raw, real),
                          buf.getvalue())
            ls = subprocess.run(
                ['git', '-C', real, 'ls-files', '--cached'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=60)
            listed = ls.stdout.decode('utf-8', 'replace')
            self.assertIn('e4-result.json', listed)
        finally:
            import shutil
            shutil.rmtree(real, ignore_errors=True)


class TeardownHygieneTests(unittest.TestCase):
    """tech#175 mirror: runs last (alphabetical class order) -- both
    urllib faces survive every behavior class in this module."""

    def test_process_urllib_keys_restored(self):
        if PRE_URLLIB is not None:
            self.assertIs(sys.modules.get('urllib'), PRE_URLLIB)
        if PRE_URLLIB_REQUEST is not None:
            self.assertIs(sys.modules.get('urllib.request'),
                          PRE_URLLIB_REQUEST)


if __name__ == '__main__':
    unittest.main()
