"""Helpers for constructing command argument lists."""

from pathlib import Path


def resolve_paths(command: list) -> list[str]:
    """Resolve any ``Path`` entries in a command list to absolute strings."""
    for index in range(len(command)):
        if isinstance(command[index], Path):
            command[index] = str(command[index].resolve())
    return command