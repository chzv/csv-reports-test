# -*- coding: utf-8 -*-
"""
Единая точка форматирования табличного вывода.

- Используется библиотека `tabulate`.
- Числовое поле 'performance' форматируется как "{:.2f}".
"""
from __future__ import annotations

from typing import Any, Mapping

from tabulate import tabulate

__all__ = ["render_table"]


def _format_cell(key: str, value: Any) -> Any:
    """Точечное форматирование значений по ключам."""
    if key == "performance" and isinstance(value, (int, float)):
        return f"{value:.2f}"
    return value


from tabulate import tabulate

def render_table(headers: list[str], rows: list[Mapping[str, Any]]) -> str:
    table_data = [[_format_cell(h, r.get(h, "")) for h in headers] for r in rows]

    colalign = tuple("right" if h == "performance" else "left" for h in headers)

    return tabulate(
        table_data,
        headers=headers,
        tablefmt="github",
        stralign="left",
        numalign="right",
        disable_numparse=True,
        colalign=colalign,
    )
