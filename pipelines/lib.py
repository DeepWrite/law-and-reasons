from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
ISSUES = ROOT / "issues"
HISTORICAL = ROOT / "historical"
SITE = ROOT / "site"
DOCS = ROOT / "docs"


def today() -> dt.date:
    return dt.date.today()


def iso_today() -> str:
    return today().isoformat()


def quarter_for(date: dt.date | None = None) -> str:
    date = date or today()
    quarter = (date.month - 1) // 3 + 1
    return f"{date.year}-Q{quarter}"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str, overwrite: bool = False) -> bool:
    ensure_dir(path.parent)
    if path.exists() and not overwrite:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def require_issue_dirs(issue: str) -> Path:
    base = ISSUES / issue
    for subdir in [
        "source_dossiers",
        "drafts",
        "drafts/en",
        "drafts/ko",
        "reviews",
        "final",
        "final/en",
        "final/ko",
    ]:
        ensure_dir(base / subdir)
    return base
