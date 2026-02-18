"""Black-box tests for pretty_command.command_to_str."""

from __future__ import annotations

import unittest

from python_command_line_helpers import pretty_command


class CommandToStrBlackBoxTests(unittest.TestCase):
    def test_empty_command_returns_empty_string(self) -> None:
        self.assertEqual(pretty_command.command_to_str([]), "")

    def test_formats_multiline_command_and_quotes_flag_values(self) -> None:
        command = ["python", "-m", "tool", "--name", "hello world", "--flag"]
        rendered = pretty_command.command_to_str(command, multiline_char="\\", indent_char="\t")
        expected = "python \\\n\t-m tool \\\n\t--name 'hello world' \\\n\t--flag"
        self.assertEqual(rendered, expected)

    def test_custom_indent_and_continuation_characters_are_used(self) -> None:
        command = ["run", "--path", "/tmp/work dir"]
        rendered = pretty_command.command_to_str(command, multiline_char="|", indent_char="  ")
        self.assertEqual(rendered, "run |\n  --path '/tmp/work dir'")
