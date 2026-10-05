"""Regression checks for preservation and the local editorial workflow."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills" / "li-human"
SPEC = importlib.util.spec_from_file_location("voice_edit", SKILL / "humanize.py")
EDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EDIT)
LEX = EDIT.load_lexicon()


class VoiceEditingTests(unittest.TestCase):
    def test_default_preserves_draft_and_offers_suggestions(self):
        draft = '  We leverage robust tools.\r\n\r\nAI-assisted draft. Credit: Ana.\n'
        preview, report = EDIT.humanize(draft, LEX)
        self.assertEqual(preview, draft)
        self.assertIn("leverage", [item["find"] for item in report["wording"]])
        self.assertEqual(report["typographic"], [])

    def test_unicode_survives_both_modes(self):
        draft = ('\ufeff👩\u200d💻 👨\u200d👩\u200d👧\u200d👦 می\u200cروم '
                 '\u061cالعربية\u200f \u2066עברית\u2069 café e\u0301 '
                 '🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f '
                 '\u200b\u2060\u00ad\u180e\u200e\u00a0\u202f\u2009\u2007\u2003\u2002')
        for enabled in (False, True):
            with self.subTest(plain_typography=enabled):
                self.assertEqual(EDIT.humanize(draft, LEX, plain_typography=enabled)[0], draft)

    def test_optional_punctuation_preserves_links_and_numbers(self):
        link = 'https://example.com/leverage/“quote”/a—b?price=$4200'
        email = 'robust@example.com'
        draft = f'We tried 3 teams—carefully. “Cost: $4,200.” {link} {email}'
        preview, report = EDIT.humanize(draft, LEX, plain_typography=True)
        self.assertEqual(preview, f'We tried 3 teams, carefully. "Cost: $4,200." {link} {email}')
        self.assertTrue(report["typographic"])
        self.assertEqual(report["wording"], [])

    def test_no_arbitrary_rhythm_or_disclosure_removal(self):
        draft = 'As an AI, I cannot attend. AI-assisted draft. Apples, pears, and grapes. 🚀'
        preview, report = EDIT.humanize(draft, LEX)
        self.assertEqual(preview, draft)
        self.assertEqual(report["structures"], [])

    def test_phrase_suggestions_do_not_double_count(self):
        _, report = EDIT.humanize('We delve into examples.', LEX)
        self.assertEqual([item["find"] for item in report["wording"]], ['delve into'])

    def test_empty_input_is_valid(self):
        preview, report = EDIT.humanize('', LEX)
        self.assertEqual(preview, '')
        self.assertFalse(any(report.values()))

    def test_cli_success_does_not_depend_on_suggestions(self):
        result = subprocess.run([sys.executable, str(SKILL / 'humanize.py'), '-', '--json'],
                                input=b'We leverage robust tools.', capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload['text'], 'We leverage robust tools.')
        self.assertTrue(payload['report']['wording'])
        self.assertEqual(set(payload), {'text', 'report'})
        self.assertEqual(set(payload['report']), {'typographic', 'wording', 'structures'})

    def test_cli_preserves_bytes_and_original_file(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / 'draft.txt', Path(temp) / 'preview.txt'
            raw = '\ufeffWe leverage tools.\r\nCredit: Ana.\r\n'.encode('utf-8')
            source.write_bytes(raw)
            result = subprocess.run([sys.executable, str(SKILL / 'humanize.py'),
                                     str(source), '-o', str(target), '--report'], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(source.read_bytes(), raw)
            self.assertEqual(target.read_bytes(), raw)
            self.assertIn(b'consider', result.stderr)

    def test_cli_refuses_to_overwrite_source_or_existing_preview(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / 'draft.txt', Path(temp) / 'preview.txt'
            source.write_text('Original draft')
            target.write_text('Earlier preview')
            for output in (source, target):
                with self.subTest(output=output):
                    result = subprocess.run([sys.executable, str(SKILL / 'humanize.py'),
                                             str(source), '-o', str(output)], capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(source.read_text(), 'Original draft')
                    self.assertEqual(target.read_text(), 'Earlier preview')


if __name__ == '__main__':
    unittest.main()
