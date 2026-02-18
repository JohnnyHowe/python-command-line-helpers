#!/usr/bin/env python3
"""Run project tests from repository root."""

from __future__ import annotations

import pathlib
import sys
import unittest


def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    src_dir = repo_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    suite = unittest.defaultTestLoader.discover(
        start_dir=str(pathlib.Path(__file__).resolve().parent),
        pattern="test_*.py",
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
