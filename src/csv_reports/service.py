# -*- coding: utf-8 -*-
"""
Координирующий слой: чтение данных -> выбор отчёта -> расчёт -> возврат заголовков и строк.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .io import read_csv_files
from .reports.registry import registry


def build_report(report_name: str, files: list[Path]) -> tuple[list[str], list[dict]]:
    """
    Формирует отчёт из одного или нескольких CSV-файлов.

    Порядок шагов:
    1) Читаем и нормализуем данные из всех переданных файлов.
    2) Получаем класс отчёта из реестра по имени.
    3) Вычисляем данные отчёта.
    4) Возвращаем заголовки и строки для дальнейшего рендера.

    Parameters
    ----------
    report_name : str
        Машинное имя отчёта (например, "performance").
    files : list[Path]
        Пути к CSV-файлам.

    Returns
    -------
    tuple[list[str], list[dict]]
        Кортеж (headers, rows), где headers — заголовки таблицы,
        rows — список словарей со значениями по колонкам.
    """
    rows = read_csv_files(files)

    report_cls = registry.get(report_name)
    report = report_cls()

    headers = report.headers()
    data = report.run(rows)

    return headers, data
