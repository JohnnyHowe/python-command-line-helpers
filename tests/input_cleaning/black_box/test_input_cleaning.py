"""Black-box tests for input_cleaning public functions."""

from __future__ import annotations

from argparse import Namespace
import unittest

from python_command_line_helpers import input_cleaning


class InputCleaningBlackBoxTests(unittest.TestCase):
    def test_replace_hypens_with_underscore_adds_alias_attributes(self) -> None:
        args = Namespace()
        setattr(args, "output-dir", "dist")
        setattr(args, "log-level", "debug")

        input_cleaning.replace_hypens_with_underscore(args)

        self.assertEqual(getattr(args, "output_dir"), "dist")
        self.assertEqual(getattr(args, "log_level"), "debug")

    def test_unescape_default_replaces_escaped_newline(self) -> None:
        value = "line1\\nline2"
        self.assertEqual(input_cleaning.unescape(value), "line1\nline2")

    def test_unescape_default_should_convert_escaped_newline(self) -> None:
        """Regression: default unescape should convert '\\n' to newline."""
        value = "line1\\nline2"
        self.assertEqual(input_cleaning.unescape(value), "line1\nline2")
