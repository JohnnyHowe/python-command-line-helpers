"""Tests for the public cast_cli_arg entrypoint."""

from __future__ import annotations

import unittest
from typing import Any, Union, cast

from python_command_line_helpers import arg_casting


class CastCliArgTests(unittest.TestCase):
    def test_casts_primitives_with_generic_caster(self) -> None:
        self.assertEqual(arg_casting.cast_cli_arg("123", int), 123)
        self.assertEqual(arg_casting.cast_cli_arg("2.5", float), 2.5)
        self.assertEqual(arg_casting.cast_cli_arg("hello", str), "hello")

    def test_casts_dict_from_csv_string(self) -> None:
        result = arg_casting.cast_cli_arg("a=1, b=2,c = 3", dict)
        self.assertEqual(result, {"a": "1", "b": "2", "c": "3"})

    def test_casts_dict_from_list_entries(self) -> None:
        result = arg_casting.cast_cli_arg(["name=jon", "lang=python"], dict)
        self.assertEqual(result, {"name": "jon", "lang": "python"})

    def test_casts_none_to_empty_dict(self) -> None:
        self.assertEqual(arg_casting.cast_cli_arg(None, dict), {})

    def test_casts_parametrized_list_from_csv(self) -> None:
        result = arg_casting.cast_cli_arg("a,b,c", list[str])
        self.assertEqual(result, ["a", "b", "c"])

    def test_union_prefers_first_matching_type(self) -> None:
        union_type = cast(type[Any], Union[int, str])
        self.assertEqual(arg_casting.cast_cli_arg("42", union_type), 42)
        self.assertEqual(arg_casting.cast_cli_arg("abc", union_type), "abc")

    def test_union_no_match_raises_type_error(self) -> None:
        union_type = cast(type[Any], Union[int, dict])
        with self.assertRaises(TypeError):
            arg_casting.cast_cli_arg(object(), union_type)

    def test_union_no_match_should_raise_type_error(self) -> None:
        """Regression: failed union casts should raise TypeError."""
        union_type = cast(type[Any], Union[int, dict])
        with self.assertRaises(TypeError):
            arg_casting.cast_cli_arg(object(), union_type)

    def test_unsupported_target_raises_type_error(self) -> None:
        with self.assertRaises(TypeError) as ctx:
            arg_casting.cast_cli_arg("abc", complex)
        self.assertIn("Could not cast abc", str(ctx.exception))

    def test_builtin_list_target_should_split_csv(self) -> None:
        """Regression: list targets should parse CSV tokens."""
        self.assertEqual(arg_casting.cast_cli_arg("a,b", list), ["a", "b"])
