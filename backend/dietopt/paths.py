"""Caminhos do projeto e do RuFaS. Fonte única: os demais módulos importam daqui."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUFAS_DIR = PROJECT_ROOT / "vendor" / "RuFaS"
RUNS_DIR = PROJECT_ROOT / "runs"
PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
if not PYTHON.exists():  # Linux/Mac
    PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"

INPUT = RUFAS_DIR / "input"
FEED_DATA_DIR = INPUT / "data" / "feed"
