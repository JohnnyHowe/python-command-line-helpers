"""White-box tests for pretty_command helper functions."""

from __future__ import annotations

import unittest

from python_command_line_helpers import pretty_command


class PrettyCommandHelperTests(unittest.TestCase):
    def test_get_command_line_parts_groups_flag_with_value(self) -> None:
        command = ["cmd", "--name", "a b", "--switch", "-x"]
        parts = list(pretty_command._get_command_line_parts(command))
        self.assertEqual(parts, ["cmd", "--name 'a b'", "--switch", "-x"])

    def test_get_command_lines_appends_continuation_to_non_final_lines(self) -> None:
        command = ["cmd", "--a", "1", "--b"]
        lines = list(pretty_command._get_command_lines(command, multiline_char="\\"))
        self.assertEqual(lines, ["cmd \\", "--a 1 \\", "--b"])
