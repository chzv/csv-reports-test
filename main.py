#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import sys


def _ensure_src_on_path() -> None:
    """Prepend the local `src/` to sys.path when running from project root."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_root, "src")
    if os.path.isdir(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)


def main() -> None:
    _ensure_src_on_path()
    from csv_reports.cli import main as _cli_main  # lazy import after path fix

    _cli_main()


if __name__ == "__main__":
    main()
