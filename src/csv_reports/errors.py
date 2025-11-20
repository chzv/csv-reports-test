# -*- coding: utf-8 -*-
"""
Доменные исключения пакета csv_reports.

Единая иерархия ошибок позволяет:
- отделить пользовательские ошибки от системных,
- аккуратно форматировать сообщения в CLI,
- расширять типы ошибок без ломки интерфейсов.
"""
from __future__ import annotations

__all__ = [
    "CsvReportsError",
    "InvalidArguments",
    "ReportNotFound",
    "DataReadError",
    "ValidationError",
]


class CsvReportsError(Exception):
    """Базовый класс для всех доменных ошибок csv_reports."""


class InvalidArguments(CsvReportsError):
    """Некорректные пользовательские аргументы (на уровне домена, помимо argparse)."""


class ReportNotFound(CsvReportsError):
    """Запрошенный отчёт не зарегистрирован в системе."""


class DataReadError(CsvReportsError):
    """Ошибка чтения данных из CSV (I/O, кодировка и т.п.)."""


class ValidationError(CsvReportsError):
    """Структура или содержимое данных не соответствуют ожиданиям."""
