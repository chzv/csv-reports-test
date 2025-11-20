# -*- coding: utf-8 -*-
"""
Типы и модели данных для пакета csv_reports.

После чтения CSV все строки приводятся к этому контракту.
"""
from __future__ import annotations

from typing import TypedDict


__all__ = ["EmployeeRow"]


class EmployeeRow(TypedDict):
    """
    Строка набора данных о сотруднике после нормализации типов.

    Поля соответствуют колонкам CSV:
    - name: Имя сотрудника.
    - position: Должность.
    - completed_tasks: Количество выполненных задач.
    - performance: Оценка эффективности (float).
    - skills: Список навыков в виде строки.
    - team: Команда/подразделение.
    - experience_years: Количество лет опыта.
    """
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: str
    team: str
    experience_years: int
