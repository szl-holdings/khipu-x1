"""Locate scripts.demo regardless of install context.

The demo entry point lives in the repository-level ``scripts/`` package.
When khipu-x1 is installed editable the project root is importable; when it
is installed as a wheel, scripts/ no longer ships. Import it via the project
root resolved from this file's location so both contexts work.
"""
from __future__ import annotations

import importlib.util
import pathlib


def load_run_demo():
    root = pathlib.Path(__file__).resolve().parents[2]  # src/khipu_x1 -> src -> repo root
    demo = root / "scripts" / "demo.py"
    if not demo.is_file():
        raise ModuleNotFoundError(
            "scripts/demo.py is not shipped in the installed wheel; run the "
            "demo from the repository checkout."
        )
    spec = importlib.util.spec_from_file_location("khipu_x1_scripts_demo", demo)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "run_demo"):
        raise ImportError("scripts/demo.py has no run_demo()")
    return mod.run_demo
