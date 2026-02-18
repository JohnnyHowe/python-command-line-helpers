# Overview
This document defines a reusable `src/` structure for Python packages that are installed from GitHub via `pip` and used inside a temporary virtual environment for the current shell session.

* I want to be able to install packages via pip with Github links.
* The packages are to be installed to a virtual environment so they don't persist after the session.

# Structure

## Required files

1. `pyproject.toml`
- Contains package metadata (`[project]`) and build backend (`[build-system]`).
- `project.name` is the install name used by `pip`.
- `tool.setuptools.package-dir = {"" = "src"}` and `tool.setuptools.packages` (or equivalent backend config) must include the import package directory.

2. `src/<package_name>/__init__.py`
- Exposes the public API for imports (for example `from python_pretty_print import pretty_print`).

3. `README.md`
- Must include GitHub install command and venv-only install flow.

4. `tests/`
- Contains automated tests and/or visual/manual checks.

## Directory layout pattern

```text
repo-root/
  pyproject.toml
  README.md
  package-structure.md
  src/
    <package_name>/
      __init__.py
      ...module files...
  tests/
    ...test files...
```

## Current project mapping

```text
python-pretty-print/
  pyproject.toml
  README.md
  package-structure.md
  src/
    python_pretty_print/
      __init__.py
      colors.py
      print_with_color_tags.py
  tests/
    run_all.py
    visual_check_*.py
```

## Install pattern (GitHub + venv session only)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "python-pretty-print @ git+https://github.com/OWNER/REPO.git"

python3 path/to/your/entry.py
...

deactivate
```

## Reuse checklist for other projects

1. Set correct `project.name` in `pyproject.toml`.
2. Ensure `src/<package_name>/` name matches import path.
3. Export intended API from `src/<package_name>/__init__.py`.
4. Add README install commands for both direct and venv workflows.
5. Confirm tests can be run from repo root.
