"""Helpers for formatting shell command arrays as readable strings."""

import shlex
from typing import Iterable


def command_to_str(command: list[str], multiline_char="\\", indent_char="\t") -> str:
    """Convert a command list into a safely quoted, multi-line shell string.

    Flags that take values are kept on the same line for readability.
    """
    if not command:
        return ""

    lines = _get_command_lines(command, multiline_char)
    return ("\n" + indent_char).join(lines)


def _get_command_lines(command: list[str], multiline_char="\\") -> Iterable[str]:
    parts = list(_get_command_line_parts(command))
    for index in range(len(parts)):
        line = parts[index]
        if not index == len(parts) - 1:
            line += " " + multiline_char
        yield line


def _get_command_line_parts(command: list[str]) -> Iterable[str]:
    part_index = 0
    while part_index < len(command):
        part = command[part_index]
        next_part = None if part_index >= len(command) - 1 else command[part_index + 1]

        if next_part is not None and part.startswith("-") and not next_part.startswith("-"):
            part_index += 2
            yield f"{part} {shlex.quote(next_part)}"
        else:
            part_index += 1
            yield part

