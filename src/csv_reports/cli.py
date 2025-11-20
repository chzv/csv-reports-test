#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Командный интерфейс для формирования отчётов по CSV.

Требования:
- --files: один или несколько путей к .csv
- --report: имя отчёта (берётся динамически из реестра)

Ошибки пользователя:
- отсутствие обязательных аргументов или неверное имя отчёта -> argparse завершит с кодом 2
- несуществующие файлы -> выводим сообщение и завершаем с кодом 1
- пустой результат -> выводим сообщение и завершаем с кодом 1
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import csv_reports as _pkg  # noqa: F401

from .errors import CsvReportsError, ReportNotFound
from .render import render_table
from .service import build_report
from .reports.registry import registry


def _existing_files(paths: Iterable[Path]) -> tuple[list[Path], list[Path]]:
    ok, missing = [], []
    for p in paths:
        (ok if p.exists() else missing).append(p)
    return ok, missing


def _build_parser() -> argparse.ArgumentParser:
    choices = registry.choices()
    parser = argparse.ArgumentParser(
        prog="csv-reports",
        description="Generate console reports from one or more CSV files.",
    )
    parser.add_argument(
        "--files",
        metavar="PATH",
        nargs="+",
        type=Path,
        required=True,
        help="One or more CSV files to read.",
    )
    if choices:
        parser.add_argument(
            "--report",
            required=True,
            choices=choices,
            help="Report name to generate (dynamic choices).",
        )
    else:
        parser.add_argument(
            "--report",
            required=True,
            help="Report name to generate.",
        )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Точка входа CLI. Завершает процесс через sys.exit с кодом возврата."""
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        raise

    _, missing = _existing_files(args.files)
    if missing:
        missing_str = ", ".join(str(p) for p in missing)
        print(f"Ошибка: файл(ы) не найдены: {missing_str}", file=sys.stderr)
        sys.exit(1)

    try:
        headers, rows = build_report(report_name=args.report, files=args.files)
    except ReportNotFound:
        print(f"Ошибка: неизвестный отчёт '{args.report}'", file=sys.stderr)
        sys.exit(1)
    except CsvReportsError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print(f"Нет данных для отчёта '{args.report}'.", file=sys.stderr)
        sys.exit(1)

    table = render_table(headers=headers, rows=rows)
    print(table)
    sys.exit(0)


if __name__ == "__main__":
    main()
