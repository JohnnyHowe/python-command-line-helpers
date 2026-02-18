"""Tests for list and union helper casters."""

from __future__ import annotations

import unittest
from typing import Union

from python_command_line_helpers import arg_casting


class ListHelperTests(unittest.TestCase):
    def test_list_caster_rejects_non_list_target(self) -> None:
        with self.assertRaises(TypeError):
            arg_casting._list_caster("a,b", tuple)

    def test_list_caster_splits_csv(self) -> None:
        self.assertEqual(arg_casting._list_caster("x,y,z", list[str]), ["x", "y", "z"])

    def test_list_caster_preserves_empty_entry_for_empty_string(self) -> None:
        self.assertEqual(arg_casting._list_caster("", list[str]), [""])


class UnionHelperTests(unittest.TestCase):
    def test_union_caster_rejects_non_union_target(self) -> None:
        with self.assertRaises(TypeError):
            arg_casting._union_caster("1", int)

    def test_union_caster_raises_when_all_members_fail(self) -> None:
        with self.assertRaises(TypeError):
            arg_casting._union_caster(object(), Union[int, dict])
