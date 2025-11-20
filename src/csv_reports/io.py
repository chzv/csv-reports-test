# -*- coding: utf-8 -*-
"""
Чтение и валидация CSV-файлов стандартной библиотекой.

Функция read_csv_files(paths) объединяет данные со всех переданных путей,
валидирует наличие обязательных колонок и приводит типы к контракту EmployeeRow.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

from .errors import DataReadError, ValidationError
from .models import EmployeeRow

__all__ = ["read_csv_files"]

# Обязательные колонки в точном соответствии с форматом входных данных
REQUIRED_COLUMNS: set[str] = {
    "name",
    "position",
    "completed_tasks",
    "performance",
    "skills",
    "team",
    "experience_years",
}


def _normalize_text(value: str) -> str:
    """Нормализация пробелов: обрезка по краям и схлопывание подряд идущих пробелов."""
    return " ".join(value.strip().split())


def _coerce_row(raw: dict[str, str]) -> EmployeeRow:
    """
    Приведение типов строки CSV к контракту EmployeeRow.
    Предполагается, что колонки существуют и содержат валидные значения.
    """
    try:
        name = _normalize_text(raw["name"])
        position = _normalize_text(raw["position"])
        skills = _normalize_text(raw["skills"])
        team = _normalize_text(raw["team"])

        completed_tasks = int(_normalize_text(raw["completed_tasks"]))
        # Числа в формате '4.8' -> float; если вдруг встретится локальная запятая, поддержим
        perf_str = _normalize_text(raw["performance"]).replace(",", ".")
        performance = float(perf_str)

        experience_years = int(_normalize_text(raw["experience_years"]))
    except (KeyError, ValueError) as exc:
        raise ValidationError(f"Некорректные значения полей: {exc}") from exc

    return EmployeeRow(
        name=name,
        position=position,
        completed_tasks=completed_tasks,
        performance=performance,
        skills=skills,
        team=team,
        experience_years=experience_years,
    )


def _validate_header(fieldnames: Iterable[str] | None, source: Path) -> None:
    if not fieldnames:
        raise ValidationError(f"В файле {source} отсутствуют заголовки столбцов.")
    missing = REQUIRED_COLUMNS.difference(fieldnames)
    if missing:
        raise ValidationError(
            f"В файле {source} отсутствуют обязательные колонки: {', '.join(sorted(missing))}"
        )


def read_csv_files(paths: List[Path]) -> list[EmployeeRow]:
    """
    Считывает все файлы целиком в память и возвращает объединённый список строк.

    Parameters
    ----------
    paths : list[Path]
        Пути к CSV-файлам.

    Returns
    -------
    list[EmployeeRow]
        Нормализованные строки данных.

    Raises
    ------
    DataReadError
        Проблемы с чтением файлов (I/O, кодировка).
    ValidationError
        Нарушение схемы — отсутствие колонок или неверные значения.
    """
    rows: list[EmployeeRow] = []

    for path in paths:
        try:
            # По умолчанию utf-8; newline="" — рекомендовано модулем csv
            with path.open("r", encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                _validate_header(reader.fieldnames, path)

                for raw in reader:
                    # DictReader возвращает строки; приводим к типам и нормализуем
                    rows.append(_coerce_row(raw))

        except FileNotFoundError as exc:
            # CLI обычно проверяет существование, но дублируем защиту в слое I/O
            raise DataReadError(f"Файл не найден: {path}") from exc
        except UnicodeDecodeError as exc:
            raise DataReadError(f"Ошибка декодирования файла {path}: ожидается UTF-8") from exc
        except OSError as exc:
            raise DataReadError(f"Ошибка чтения файла {path}: {exc}") from exc

    return rows
