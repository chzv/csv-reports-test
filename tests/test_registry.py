# -*- coding: utf-8 -*-
"""
Тесты реестра отчётов:
- регистрация нового отчёта и получение его по имени;
- ошибка при дублировании имени;
- choices() содержит "performance";
- get("performance") возвращает класс PerformanceReport.
"""
from __future__ import annotations

import pytest

from csv_reports.reports.base import Report
from csv_reports.reports.registry import ReportRegistry, registry
from csv_reports.reports.performance import PerformanceReport


def test_global_registry_contains_performance() -> None:
    """Глобальный реестр должен знать про встроенный отчёт 'performance'."""
    choices = registry.choices()
    assert "performance" in choices

    cls = registry.get("performance")
    assert cls is PerformanceReport
    assert issubclass(cls, Report)


def test_register_and_get_on_local_registry() -> None:
    """Регистрация и извлечение отчёта в отдельном локальном реестре."""
    local = ReportRegistry()

    @local.register
    class DummyReport(Report):
        name = "dummy"

        def headers(self) -> list[str]:
            return ["col"]

        def run(self, rows):
            return [{"col": 1}]

    assert "dummy" in local.choices()
    assert local.get("dummy") is DummyReport


def test_duplicate_name_raises_value_error() -> None:
    """Повторная регистрация отчёта с тем же именем должна привести к ошибке."""
    local = ReportRegistry()

    @local.register
    class R1(Report):
        name = "dup"

        def headers(self) -> list[str]:
            return ["x"]

        def run(self, rows):
            return [{"x": 1}]

    with pytest.raises(ValueError):

        @local.register
        class R2(Report):
            name = "dup"  # дублируем имя

            def headers(self) -> list[str]:
                return ["y"]

            def run(self, rows):
                return [{"y": 2}]
