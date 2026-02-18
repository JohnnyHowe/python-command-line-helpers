"""White-box tests for command_building.resolve_paths internals."""

from __future__ import annotations

from pathlib import Path
import unittest

from python_command_line_helpers import command_building


class ResolvePathsWhiteBoxTests(unittest.TestCase):
    def test_mutates_input_list_and_returns_same_list(self) -> None:
        command = ["echo", Path(".")]
        result = command_building.resolve_paths(command)
        self.assertIs(result, command)
        self.assertEqual(command[1], str(Path(".").resolve()))

    def test_uses_isinstance_for_path_subclasses(self) -> None:
        custom_path = Path("src")
        command = [custom_path]
        result = command_building.resolve_paths(command)
        self.assertEqual(result, [str(custom_path.resolve())])
