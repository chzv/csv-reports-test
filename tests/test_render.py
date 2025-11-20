# -*- coding: utf-8 -*-
"""
Тесты рендера:
- проверка форматирования чисел с 2 знаками после запятой;
- снапшот-тест всей строки вывода для стабильного Markdown-формата (tablefmt="github").
"""
from __future__ import annotations

from csv_reports.render import render_table


def test_render_table_formats_two_decimals() -> None:
    headers = ["position", "performance"]
    rows = [
        {"position": "DevOps Engineer", "performance": 4.854},
        {"position": "Backend Developer", "performance": 4.8},
        {"position": "QA Engineer", "performance": 4.5},
    ]
    out = render_table(headers, rows)

    # Числа должны быть отформатированы с точностью до 2 знаков
    assert "4.85" in out
    assert "4.80" in out
    assert "4.50" in out


def test_render_table_snapshot_full_string() -> None:
    headers = ["position", "performance"]
    rows = [
        {"position": "DevOps Engineer", "performance": 4.85},
        {"position": "Backend Developer", "performance": 4.80},
        {"position": "QA Engineer", "performance": 4.50},
    ]
    out = render_table(headers, rows)

    expected = (
        "| position          |   performance |\n"
        "|-------------------|---------------|\n"
        "| DevOps Engineer   |          4.85 |\n"
        "| Backend Developer |          4.80 |\n"
        "| QA Engineer       |          4.50 |"
    )

    # Снапшот: строка должна совпадать полностью
    assert out == expected
