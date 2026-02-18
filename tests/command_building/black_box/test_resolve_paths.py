"""Black-box tests for command_building.resolve_paths."""

from __future__ import annotations

import pathlib
import unittest

from python_command_line_helpers import command_building


class ResolvePathsBlackBoxTests(unittest.TestCase):
    def test_resolves_path_entries_to_absolute_strings(self) -> None:
        command = ["python", pathlib.Path("."), pathlib.Path("src")]
        result = command_building.resolve_paths(command)

        self.assertEqual(result[0], "python")
        self.assertTrue(isinstance(result[1], str))
        self.assertTrue(isinstance(result[2], str))
        self.assertEqual(result[1], str(pathlib.Path(".").resolve()))
        self.assertEqual(result[2], str(pathlib.Path("src").resolve()))

    def test_non_path_entries_remain_unchanged(self) -> None:
        command = ["python", "-m", "unittest"]
        result = command_building.resolve_paths(command)
        self.assertEqual(result, ["python", "-m", "unittest"])
