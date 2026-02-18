"""White-box tests for input_cleaning implementation behavior."""

from __future__ import annotations

from argparse import Namespace
import unittest

from python_command_line_helpers import input_cleaning


class InputCleaningWhiteBoxTests(unittest.TestCase):
    def test_replace_hypens_with_underscore_keeps_original_attributes(self) -> None:
        args = Namespace()
        setattr(args, "dry-run", True)

        input_cleaning.replace_hypens_with_underscore(args)

        self.assertTrue(getattr(args, "dry-run"))
        self.assertTrue(getattr(args, "dry_run"))

    def test_unescape_uses_only_requested_literals(self) -> None:
        value = r"\n\:"
        result = input_cleaning.unescape(value, literals_to_unescape=[":"])
        self.assertEqual(result, r"\n:")

    def test_unescape_supports_multiple_custom_literals(self) -> None:
        value = r"path\:\ value"
        result = input_cleaning.unescape(value, literals_to_unescape=[":", " "])
        self.assertEqual(result, "path: value")
