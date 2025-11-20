# -*- coding: utf-8 -*-
"""
Тесты чтения CSV:
- чтение одного/нескольких файлов, проверка типов и количества строк;
- негативный кейс: отсутствие обязательной колонки.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from csv_reports.io import read_csv_files
from csv_reports.errors import ValidationError


def _assert_employee_row_schema(row: dict) -> None:
    """Проверяет схему и типы полей одной записи."""
    expected_keys = {
        "name",
        "position",
        "completed_tasks",
        "performance",
        "skills",
        "team",
        "experience_years",
    }
    assert expected_keys.issubset(row.keys())

    assert isinstance(row["name"], str)
    assert isinstance(row["position"], str)
    assert isinstance(row["skills"], str)
    assert isinstance(row["team"], str)

    assert isinstance(row["completed_tasks"], int)
    assert isinstance(row["performance"], float)
    assert isinstance(row["experience_years"], int)


def test_read_single_file_types_and_count(sample_csv_1: Path) -> None:
    rows = read_csv_files([sample_csv_1])
    # В sample_csv_1 пять строк данных (без заголовка)
    assert len(rows) == 5

    for r in rows:
        _assert_employee_row_schema(r)

    # Выборочная проверка содержимого
    names = {r["name"] for r in rows}
    assert "Alex Ivanov" in names
    assert "Anna Lee" in names


def test_read_multiple_files_merge(sample_csv_1: Path, sample_csv_2: Path) -> None:
    rows = read_csv_files([sample_csv_1, sample_csv_2])
    # 5 строк из первого + 5 строк из второго
    assert len(rows) == 10

    for r in rows:
        _assert_employee_row_schema(r)

    # Проверяем, что позиции агрегировались из обоих файлов
    positions = [r["position"] for r in rows]
    assert positions.count("Backend Developer") == 3  # Alex (2 файла) + Zoe (2-й файл)


def test_missing_required_column_raises(tmp_path: Path) -> None:
    # Создаём CSV без колонки 'performance'
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text(
        (
            "name,position,completed_tasks,skills,team,experience_years\n"
            "Alex Ivanov,Backend Developer,45,\"Python, Django\",API Team,5\n"
        ),
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(ValidationError) as exc:
        read_csv_files([bad_csv])

    assert "обязательные колонки" in str(exc.value) or "колонки" in str(exc.value)
