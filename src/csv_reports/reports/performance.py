# -*- coding: utf-8 -*-
"""
Отчёт 'performance':
- группировка по должности (position)
- среднее по метрике performance
- сортировка по убыванию средней эффективности
Результат: список словарей {"position": str, "performance": float}
(округление выполняется на этапе рендера).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Sequence

from .base import Report
from ..models import EmployeeRow
from .registry import registry


@registry.register
class PerformanceReport(Report):
    name = "performance"

    def headers(self) -> list[str]:
        return ["position", "performance"]

    def run(self, rows: Sequence[EmployeeRow]) -> List[Dict[str, Any]]:
        buckets: dict[str, list[float]] = defaultdict(list)

        for r in rows:
            # EmployeeRow гарантирует наличие и типы полей
            buckets[r["position"]].append(r["performance"])

        aggregates: List[Dict[str, Any]] = []
        for position, values in buckets.items():
            mean_value = sum(values) / len(values)
            aggregates.append({"position": position, "performance": float(mean_value)})

        # Сортировка по убыванию средней эффективности
        aggregates.sort(key=lambda x: x["performance"], reverse=True)
        return aggregates
