# -*- coding: utf-8 -*-
"""
Базовые контракты для отчётов.

Любой новый отчёт должен унаследоваться от Report и реализовать:
- статическое поле name: уникальный идентификатор отчёта (например, "performance");
- headers(): список заголовков таблицы;
- run(rows): вычисление данных отчёта по нормализованным строкам EmployeeRow.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Sequence

from ..models import EmployeeRow

__all__ = ["Report"]


class Report(ABC):
    """Абстрактный базовый класс отчёта."""

    name: ClassVar[str]

    @abstractmethod
    def headers(self) -> list[str]:
        """Заголовки для табличного вывода."""
        raise NotImplementedError

    @abstractmethod
    def run(self, rows: Sequence[EmployeeRow]) -> list[dict[str, Any]]:
        """
        Выполняет расчёт и возвращает список словарей,
        совместимых с заголовками, возвращаемыми headers().
        """
        raise NotImplementedError
