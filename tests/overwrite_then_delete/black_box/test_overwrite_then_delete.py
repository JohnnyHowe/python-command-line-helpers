"""Black-box tests for overwrite_then_delete public behavior."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest import mock

from python_command_line_helpers import overwrite_then_delete as otd


class OverwriteThenDeleteBlackBoxTests(unittest.TestCase):
    def test_fill_with_junk_overwrites_existing_content_with_same_length(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "secret.txt"
            original = b"super-secret"
            replacement = b"X" * len(original)
            path.write_bytes(original)

            with mock.patch(
                "python_command_line_helpers.overwrite_then_delete.os.urandom",
                return_value=replacement,
            ):
                otd.fill_with_junk(path)

            self.assertEqual(path.read_bytes(), replacement)
            self.assertEqual(len(path.read_bytes()), len(original))

    def test_overwrite_then_delete_removes_binary_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "payload.bin"
            path.write_bytes(b"\xff\xfe\xfd")

            otd.overwrite_then_delete(path)

            self.assertFalse(path.exists())

    def test_delete_removes_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "to_delete.txt"
            path.write_text("data")

            otd.delete(path)

            self.assertFalse(path.exists())

    def test_delete_missing_file_is_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "missing.txt"
            otd.delete(path)
            self.assertFalse(path.exists())
