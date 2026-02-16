from pathlib import Path


def resolve_paths(command: list) -> list[str]:
    for index in range(len(command)):
        if isinstance(command[index], Path):
            command[index] = str(command[index].resolve())
    return command
