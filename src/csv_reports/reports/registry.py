# -*- coding: utf-8 -*-
"""
Реестр отчётов и удобный декоратор регистрации.

Использование:
    from .registry import registry

    @registry.register
    class MyReport(Report):
        name = "myreport"
        ...

CLI получает список доступных отчётов через registry.choices().
"""
from __future__ import annotations

from typing import Dict, List, Type

from .base import Report
from ..errors import ReportNotFound

__all__ = ["ReportRegistry", "registry"]


class ReportRegistry:
    """Хранилище соответствий <имя отчёта> -> <класс отчёта>."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Report]] = {}

    def register(self, cls: Type[Report]) -> Type[Report]:
        """
        Декоратор/метод регистрации класса отчёта.

        Проверки:
        - cls должен быть подклассом Report;
        - у класса должно быть непустое поле `name`;
        - имя должно быть уникальным в пределах реестра.
        """
        if not issubclass(cls, Report):
            raise TypeError("Можно регистрировать только подклассы Report")

        name = getattr(cls, "name", None)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("У класса отчёта должно быть непустое строковое поле `name`")

        if name in self._registry:
            raise ValueError(f"Отчёт с именем '{name}' уже зарегистрирован")

        self._registry[name] = cls
        return cls

    def get(self, name: str) -> Type[Report]:
        """Возвращает класс отчёта по его machine-id или бросает ReportNotFound."""
        try:
            return self._registry[name]
        except KeyError as exc:
            raise ReportNotFound(f"Отчёт '{name}' не найден") from exc

    def choices(self) -> List[str]:
        """Список доступных имён отчётов (для CLI choices)."""
        return sorted(self._registry.keys())


registry = ReportRegistry()
