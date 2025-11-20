# -*- coding: utf-8 -*-
"""
Тесты отчёта 'performance':
- корректный расчёт среднего по должностям и сортировка по убыванию;
- идемпотентность по отношению к перестановке строк/порядка файлов (кроме порядка при равных значениях);
- отсутствие преждевременного округления (в run() возвращаются float, форматирование — в рендере).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from csv_reports.reports.performance import PerformanceReport
from csv_reports.io import read_csv_files


def _as_map(data):
    """Удобное представление результата отчёта: {position: performance}."""
    return {row["position"]: row["performance"] for row in data}


def test_performance_report_basic(rows):
    report = PerformanceReport()
    data = report.run(rows)

    # Ожидаемые средние значения по всем переданным файлам:
    # Backend Developer: (4.8 + 4.9 + 4.7) / 3 = 4.8
    # Frontend Developer: (4.7 + 4.6) / 2 = 4.65
    # Data Scientist: (4.6 + 4.7) / 2 = 4.65
    # DevOps Engineer: (4.9 + 4.8) / 2 = 4.85
    # QA Engineer: 4.5
    expected = {
        "DevOps Engineer": 4.85,
        "Backend Developer": 4.8,
        "Frontend Developer": 4.65,
        "Data Scientist": 4.65,
        "QA Engineer": 4.5,
    }

    # Проверяем значения
    as_map = _as_map(data)
    assert as_map == expected

    # Проверяем сортировку по убыванию эффективности
    positions_in_order = [row["position"] for row in data]
    assert positions_in_order[0] == "DevOps Engineer"
    assert positions_in_order[1] == "Backend Developer"

    # Для равных значений порядок определяется стабильной сортировкой (по порядку появления ключа),
    # в данной фикстуре ожидается: Frontend Developer перед Data Scientist.
    assert positions_in_order[2:4] == ["Frontend Developer", "Data Scientist"]
    assert positions_in_order[4] == "QA Engineer"


def test_performance_report_idempotent_under_row_permutation(rows):
    """Перестановка строк не должна менять значения и ранжирование по числам (кроме порядка при равных значениях)."""
    report = PerformanceReport()

    data_normal = report.run(rows)
    # Переставим строки в обратном порядке
    rows_reversed = list(reversed(rows))
    data_reversed = report.run(rows_reversed)

    # Значения по должностям совпадают
    assert _as_map(data_normal) == _as_map(data_reversed)

    # Ранжирование по числам совпадает
    perf_normal = [row["performance"] for row in data_normal]
    perf_reversed = [row["performance"] for row in data_reversed]
    assert perf_normal == perf_reversed == [4.85, 4.8, 4.65, 4.65, 4.5]


def test_performance_report_idempotent_under_file_permutation(sample_csv_1: Path, sample_csv_2: Path):
    """Перестановка порядка файлов не меняет рассчитанные значения."""
    report = PerformanceReport()

    data_a = report.run(read_csv_files([sample_csv_1, sample_csv_2]))
    data_b = report.run(read_csv_files([sample_csv_2, sample_csv_1]))

    assert _as_map(data_a) == _as_map(data_b)


def test_run_returns_raw_floats_not_formatted(rows):
    """Внутри run() значения производительности — float, форматирование выполняется на этапе рендера."""
    report = PerformanceReport()
    data = report.run(rows)
    assert all(isinstance(row["performance"], float) for row in data)
