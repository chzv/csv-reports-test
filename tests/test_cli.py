# -*- coding: utf-8 -*-
"""
Интеграционные тесты CLI:
- Happy-path: генерация отчёта из двух файлов, проверка stdout.
- Негативные кейсы: неизвестный отчёт, отсутствующий файл, отсутствие --files, отсутствие --report.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from csv_reports.cli import main as cli_main


def test_cli_happy_path_stdout(capsys, sample_csv_1: Path, sample_csv_2: Path) -> None:
    """Проверяем, что CLI печатает корректную таблицу и завершает с кодом 0."""
    with pytest.raises(SystemExit) as e:
        cli_main(
            [
                "--files",
                str(sample_csv_1),
                str(sample_csv_2),
                "--report",
                "performance",
            ]
        )
    assert e.value.code == 0

    out = capsys.readouterr().out
    # Заголовки таблицы
    assert "position" in out
    assert "performance" in out
    # Ожидаемые строки и форматирование чисел
    assert "DevOps Engineer" in out and "4.85" in out
    assert "Backend Developer" in out and "4.80" in out
    assert "QA Engineer" in out and "4.50" in out
    # Убеждаемся, что это Markdown-таблица (формат github)
    assert "|" in out and "---" in out


def test_cli_unknown_report_exits_with_code_2(sample_csv_1: Path) -> None:
    """Неизвестный отчёт должен ловиться argparse через choices и приводить к коду 2."""
    with pytest.raises(SystemExit) as e:
        cli_main(
            [
                "--files",
                str(sample_csv_1),
                "--report",
                "unknown-report",
            ]
        )
    # argparse использует код 2 для ошибок парсинга аргументов
    assert e.value.code == 2


def test_cli_missing_file_exits_with_code_1(capsys, sample_csv_1: Path, tmp_path: Path) -> None:
    """Если передан несуществующий файл — печатается сообщение об ошибке и код 1."""
    missing = tmp_path / "no_such.csv"
    with pytest.raises(SystemExit) as e:
        cli_main(
            [
                "--files",
                str(sample_csv_1),
                str(missing),
                "--report",
                "performance",
            ]
        )
    assert e.value.code == 1
    err = capsys.readouterr().err
    assert "не найдены" in err or "не найден" in err or "Ошибка" in err


def test_cli_no_files_argument_exits_with_code_2() -> None:
    """Отсутствует обязательный аргумент --files -> код 2 от argparse."""
    with pytest.raises(SystemExit) as e:
        cli_main(
            [
                "--report",
                "performance",
            ]
        )
    assert e.value.code == 2


def test_cli_no_report_argument_exits_with_code_2(sample_csv_1: Path) -> None:
    """Отсутствует обязательный аргумент --report -> код 2 от argparse."""
    with pytest.raises(SystemExit) as e:
        cli_main(
            [
                "--files",
                str(sample_csv_1),
            ]
        )
    assert e.value.code == 2
