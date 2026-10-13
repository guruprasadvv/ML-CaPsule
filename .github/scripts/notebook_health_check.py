#!/usr/bin/env python3
"""
Notebook Health Check Bot

Checks the Jupyter notebooks changed in a push or pull request:
  1. Structure  - the file is valid JSON and a valid nbformat notebook.
                  A broken notebook fails the check.
  2. Execution  - the notebook is run with nbconvert. Many notebooks here need
                  datasets, GPUs or extra packages that CI does not have, so
                  execution problems are reported as warnings, not failures.

Changed files are read from changed_files.txt (written by the workflow).
If that file is missing, notebooks in common folders and the repo root are used.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import nbformat

CHANGED_FILES = Path("changed_files.txt")
EXEC_TIMEOUT = 300  # seconds per notebook
MAX_EXECUTE = 10    # cap how many notebooks are executed per run


def changed_notebooks():
    """Notebooks listed in changed_files.txt that still exist (not deleted)."""
    if not CHANGED_FILES.exists():
        return None
    paths = []
    for line in CHANGED_FILES.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.endswith(".ipynb") and ".ipynb_checkpoints" not in line:
            p = Path(line)
            if p.is_file():
                paths.append(p)
    return paths


def fallback_notebooks(root_dir="."):
    """Notebooks in common folders plus the repo root (avoids scanning the whole repo)."""
    root = Path(root_dir)
    found = []
    for folder in ["notebooks", "examples", "tutorials", "docs", "guides"]:
        if (root / folder).is_dir():
            found.extend((root / folder).rglob("*.ipynb"))
    found.extend(root.glob("*.ipynb"))
    unique = []
    for p in found:
        if ".ipynb_checkpoints" not in str(p) and p not in unique:
            unique.append(p)
    return unique


def check_structure(path):
    """Return None if the notebook is valid, otherwise an error message."""
    try:
        with open(path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        nbformat.validate(nb)
        return None
    except json.JSONDecodeError as e:
        return f"invalid JSON: {e}"
    except Exception as e:  # nbformat.ValidationError and read errors
        return f"invalid notebook: {str(e).splitlines()[0]}"


def check_execution(path):
    """Return None if the notebook runs cleanly, otherwise a short error message."""
    try:
        proc = subprocess.run(
            ["jupyter", "nbconvert", "--to", "notebook", "--execute",
             "--stdout", str(path)],
            capture_output=True, text=True, timeout=EXEC_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return f"timed out after {EXEC_TIMEOUT // 60} minutes"
    if proc.returncode != 0:
        lines = [l for l in proc.stderr.strip().splitlines() if l.strip()]
        msg = lines[-1] if lines else f"exit code {proc.returncode}"
        return re.sub(r"\x1b\[[0-9;]*m", "", msg)  # strip terminal colours
    return None


def main():
    notebooks = changed_notebooks()
    if notebooks is None:
        notebooks = fallback_notebooks()
        print(f"No changed_files.txt; checking {len(notebooks)} notebook(s) from default folders")
    else:
        print(f"{len(notebooks)} changed notebook(s) to check")

    if not notebooks:
        print("No notebooks to check.")
        return 0

    broken, warnings = [], []
    for i, nb in enumerate(notebooks):
        print(f"Checking: {nb}")
        err = check_structure(nb)
        if err:
            broken.append((nb, err))
            continue
        if i < MAX_EXECUTE:
            err = check_execution(nb)
            if err:
                warnings.append((nb, err))

    if warnings:
        print(f"\n⚠️  {len(warnings)} notebook(s) did not execute cleanly in CI (not a failure):")
        for nb, err in warnings:
            print(f"  - {nb}: {err}")
            print(f"::warning file={nb}::Notebook did not execute in CI: {err}")

    if broken:
        print(f"\n❌ {len(broken)} notebook(s) are broken:")
        for nb, err in broken:
            print(f"  - {nb}: {err}")
            print(f"::error file={nb}::{err}")
        return 1

    print(f"\n✅ {len(notebooks)} notebook(s) are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
