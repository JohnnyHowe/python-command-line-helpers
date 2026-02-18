"""Tests for dict-related helper casters."""

from __future__ import annotations

import unittest

from python_command_line_helpers import arg_casting


class DictHelperTests(unittest.TestCase):
    def test_dict_caster_rejects_non_dict_target(self) -> None:
        with self.assertRaises(TypeError):
            arg_casting._dict_caster("a=1", str)

    def test_dict_caster_raises_for_malformed_csv_pair(self) -> None:
        with self.assertRaises(ValueError):
            arg_casting._dict_caster("a=1,bad", dict)

    def test_list_to_dict_supports_equals_in_value(self) -> None:
        result = arg_casting._list_to_dict_caster(["a=1=2", "b=3"])
        self.assertEqual(result, {"a": "1=2", "b": "3"})

    def test_list_to_dict_rejects_invalid_entry(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            arg_casting._list_to_dict_caster(["missing_equals"])
        self.assertIn("invalid dict entry", str(ctx.exception))

    def test_dict_caster_csv_should_allow_equals_in_value(self) -> None:
        """Regression: CSV dict parsing should preserve '=' in values."""
        result = arg_casting._dict_caster("a=1=2,b=3", dict)
        self.assertEqual(result, {"a": "1=2", "b": "3"})
