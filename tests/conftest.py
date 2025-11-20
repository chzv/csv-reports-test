# -*- coding: utf-8 -*-
"""
Общие фикстуры для тестов:
- sample_csv_1, sample_csv_2: временные CSV-файлы с данными из задания.
- rows: объединённые нормализованные строки из обоих файлов.
"""
from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent
from typing import List

import pytest

# Обеспечиваем доступ к пакету из src/ при локальном запуске тестов без установки
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from csv_reports.io import read_csv_files  # noqa: E402


def _write_csv(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(dedent(content).lstrip("\n"), encoding="utf-8", newline="\n")
    return path


@pytest.fixture
def sample_csv_1(tmp_path: Path) -> Path:
    """CSV с примерными данными №1 (из условия)."""
    content = """
    name,position,completed_tasks,performance,skills,team,experience_years
    Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
    Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
    John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3
    Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
    Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4
    """
    return _write_csv(tmp_path, "sample_1.csv", content)


@pytest.fixture
def sample_csv_2(tmp_path: Path) -> Path:
    """CSV с примерными данными №2 (дополняет и частично пересекается по позициям)."""
    content = """
    name,position,completed_tasks,performance,skills,team,experience_years
    Alex Ivanov,Backend Developer,30,4.9,"Python, Django, PostgreSQL, Docker",API Team,5
    Maria Petrova,Frontend Developer,25,4.6,"React, TypeScript, Redux, CSS",Web Team,4
    John Smith,Data Scientist,35,4.7,"Python, ML, SQL, Pandas",AI Team,3
    Anna Lee,DevOps Engineer,40,4.8,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
    Zoe Adams,Backend Developer,50,4.7,"Python, FastAPI, Redis, Docker",API Team,7
    """
    return _write_csv(tmp_path, "sample_2.csv", content)


@pytest.fixture
def rows(sample_csv_1: Path, sample_csv_2: Path) -> List[dict]:
    """Объединённые нормализованные строки из двух файлов."""
    return read_csv_files([sample_csv_1, sample_csv_2])
