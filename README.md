# CSV Reports (CLI)

CLI-утилита для формирования отчётов из CSV. Внутри — только стандартная библиотека (`argparse`, `csv`) и `tabulate` для красивого вывода в консоль. Архитектура плагинов: новые отчёты добавляются отдельными классами.

---

## Требования
- Python 3.10+
- Зависимости устанавливаются через `pip` (см. ниже)

## Установка и запуск

```bash
# 1) изолируем окружение (рекомендуется)
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .\.venv\Scripts\Activate.ps1

# 2) ставим зависимости и проект
python -m pip install --upgrade pip
pip install -e .

# 3) запуск (пример)
python ./main.py --files ./data/employees1.csv ./data/employees2.csv --report performance

Пример вывода
| position            |   performance |
|---------------------|---------------|
| DevOps Engineer     |          4.85 |
| Backend Developer   |          4.80 |
| Frontend Developer  |          4.65 |
| Data Scientist      |          4.65 |
| QA Engineer         |          4.50 |

Тесты
pip install pytest pytest-cov
pytest

Как добавить новый отчёт
Создайте файл в src/csv_reports/reports/, унаследуйтесь от Report, укажите name.
Зарегистрируйте класс декоратором @registry.register.
Верните заголовки в headers() и подготовьте строки в run(rows).
Мини-шаблон:
# src/csv_reports/reports/my_report.py
from __future__ import annotations
from typing import Any, Dict, List, Sequence
from .base import Report
from ..models import EmployeeRow
from .registry import registry

@registry.register
class MyReport(Report):
    name = "myreport"

    def headers(self) -> list[str]:
        return ["col1", "col2"]

    def run(self, rows: Sequence[EmployeeRow]) -> List[Dict[str, Any]]:
        # Ваша агрегация/логика
        return [{"col1": "value", "col2": 123}]
Запуск:
python ./main.py --files ./data/employees1.csv ./data/employees2.csv --report myreport

Структура проекта
.
├─ main.py
├─ pyproject.toml
├─ src/
│  └─ csv_reports/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ errors.py
│     ├─ io.py
│     ├─ models.py
│     ├─ render.py
│     ├─ service.py
│     └─ reports/
│        ├─ base.py
│        ├─ registry.py
│        └─ performance.py
├─ tests/
│  ├─ conftest.py
│  ├─ test_cli.py
│  ├─ test_io.py
│  ├─ test_registry.py
│  ├─ test_render.py
│  └─ test_report_performance.py
├─ data/        # примеры CSV 
└─ docs/        # скриншоты запуска и тестов

Коротко о ключевых решениях
Строгий формат входа: name, position, completed_tasks, performance, skills, team, experience_years.
Отчёты = плагины: новые метрики добавляются без правок CLI — только новый класс и регистрация.
Вывод: tabulate в формате GitHub-таблицы, performance печатается с двумя знаками.
