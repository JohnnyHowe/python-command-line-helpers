"""White-box tests for overwrite_then_delete internals."""

from __future__ import annotations

from pathlib import Path
import tempfile
import types
import unittest
from unittest import mock

from python_command_line_helpers import overwrite_then_delete as otd


class OverwriteThenDeleteWhiteBoxTests(unittest.TestCase):
    def test_overwrite_then_delete_calls_fill_then_delete(self) -> None:
        path = Path("secret.txt")
        with mock.patch.object(otd, "fill_with_junk") as fill_mock, mock.patch.object(
            otd, "delete"
        ) as delete_mock:
            otd.overwrite_then_delete(path)

        fill_mock.assert_called_once_with(path)
        delete_mock.assert_called_once_with(path)

    def test_get_contents_length_returns_default_for_missing_file(self) -> None:
        missing = Path("does_not_exist.txt")
        self.assertEqual(otd._get_contents_length(missing, default_length=77), 77)

    def test_get_contents_length_returns_length_for_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "value.txt"
            path.write_text("hello")
            self.assertEqual(otd._get_contents_length(path), 5)

    def test_delete_short_circuits_for_missing_file(self) -> None:
        missing = Path("not_here.txt")
        with mock.patch.object(otd, "_get_secure_delete_commands_for_current_platform") as commands_mock, mock.patch.object(
            otd, "_try_run_command"
        ) as run_mock, mock.patch.object(otd.Path, "unlink", autospec=True) as unlink_mock:
            otd.delete(missing)

        commands_mock.assert_not_called()
        run_mock.assert_not_called()
        unlink_mock.assert_not_called()

    def test_delete_stops_after_success_when_file_is_gone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "secret.txt"
            path.write_text("sensitive")

            calls: list[list[str]] = []

            def fake_try_run(cmd: list[str]) -> bool:
                calls.append(cmd)
                path.unlink()
                return True

            with mock.patch.object(
                otd,
                "_get_secure_delete_commands_for_current_platform",
                return_value=iter([["tool", "{path}"], ["tool2", "{path}"]]),
            ), mock.patch.object(otd, "_try_run_command", side_effect=fake_try_run) as run_mock:
                otd.delete(path)

            run_mock.assert_called_once()
            self.assertEqual(calls[0], ["tool", str(path)])
            self.assertFalse(path.exists())

    def test_delete_falls_back_to_unlink_when_commands_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "secret.txt"
            path.write_text("value")

            with mock.patch.object(
                otd,
                "_get_secure_delete_commands_for_current_platform",
                return_value=iter([["a", "{path}"], ["b", "{path}"]]),
            ), mock.patch.object(
                otd, "_try_run_command", side_effect=[False, False]
            ) as run_mock, mock.patch.object(otd.Path, "unlink", autospec=True) as unlink_mock:
                otd.delete(path)

            self.assertEqual(run_mock.call_count, 2)
            unlink_mock.assert_called_once_with(path, missing_ok=True)

    def test_get_secure_delete_commands_matches_current_platform_prefix(self) -> None:
        with mock.patch.object(otd.sys, "platform", "linux"):
            commands = list(otd._get_secure_delete_commands_for_current_platform())

        self.assertEqual(commands, otd.SECURE_DELETE_COMMANDS_BY_PLATFORM["linux"])

    def test_get_secure_delete_commands_supports_win32_runtime(self) -> None:
        with mock.patch.object(otd.sys, "platform", "win32"):
            commands = list(otd._get_secure_delete_commands_for_current_platform())

        self.assertEqual(commands, otd.SECURE_DELETE_COMMANDS_BY_PLATFORM["nt"])

    def test_try_run_command_returns_false_when_executable_missing(self) -> None:
        with mock.patch.object(otd.shutil, "which", return_value=None), mock.patch.object(
            otd.subprocess, "run"
        ) as run_mock:
            result = otd._try_run_command(["missing", "arg"])

        self.assertFalse(result)
        run_mock.assert_not_called()

    def test_try_run_command_returns_true_for_zero_exit(self) -> None:
        completed = types.SimpleNamespace(returncode=0)
        with mock.patch.object(otd.shutil, "which", return_value="/bin/tool"), mock.patch.object(
            otd.subprocess, "run", return_value=completed
        ) as run_mock:
            result = otd._try_run_command(["tool", "arg"])

        self.assertTrue(result)
        run_mock.assert_called_once_with(
            ["tool", "arg"],
            stdout=otd.subprocess.DEVNULL,
            stderr=otd.subprocess.DEVNULL,
            check=False,
        )

    def test_try_run_command_returns_false_for_nonzero_exit(self) -> None:
        completed = types.SimpleNamespace(returncode=7)
        with mock.patch.object(otd.shutil, "which", return_value="/bin/tool"), mock.patch.object(
            otd.subprocess, "run", return_value=completed
        ):
            result = otd._try_run_command(["tool", "arg"])

        self.assertFalse(result)
