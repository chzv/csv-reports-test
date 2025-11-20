# -*- coding: utf-8 -*-
"""
Инициализация пакета csv_reports.

Задача: обеспечить регистрацию всех доступных отчётов при импорте пакета.
"""
from __future__ import annotations
from .reports import performance as _perf  # noqa: F401

__all__: list[str] = []
