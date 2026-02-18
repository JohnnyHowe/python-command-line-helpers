"""Basic package structure smoke tests."""

import unittest

from python_command_line_helpers import (
    arg_casting,
    command_building,
    input_cleaning,
    pretty_command,
)


class ImportTests(unittest.TestCase):
    def test_modules_import(self) -> None:
        self.assertIsNotNone(arg_casting)
        self.assertIsNotNone(command_building)
        self.assertIsNotNone(input_cleaning)
        self.assertIsNotNone(pretty_command)
