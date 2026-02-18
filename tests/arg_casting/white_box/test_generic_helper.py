"""Tests for the generic caster helper."""

from __future__ import annotations

import unittest

from python_command_line_helpers import arg_casting


class GenericHelperTests(unittest.TestCase):
    def test_generic_caster_calls_target_constructor(self) -> None:
        class Wrap:
            def __init__(self, value: str) -> None:
                self.value = value

        wrapped = arg_casting._generic_caster("ok", Wrap)
        self.assertEqual(wrapped.value, "ok")

    def test_generic_caster_propagates_constructor_error(self) -> None:
        class Fails:
            def __init__(self, value: str) -> None:
                raise RuntimeError(f"boom:{value}")

        with self.assertRaises(RuntimeError) as ctx:
            arg_casting._generic_caster("x", Fails)
        self.assertIn("boom:x", str(ctx.exception))
