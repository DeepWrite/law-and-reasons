from __future__ import annotations

import csv
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def historical_config() -> dict:
    return yaml.safe_load((ROOT / "config" / "historical.yml").read_text(encoding="utf-8"))


def magazine_config() -> dict:
    return yaml.safe_load((ROOT / "config" / "magazine.yml").read_text(encoding="utf-8"))


def test_magazine_is_legal_philosophy_review_not_general_review():
    config = magazine_config()
    assert config["title"] == "법과 이유"
    assert config["title_en"] == "Law and Reasons"
    assert config["subtitle"] == "A Review of Legal Philosophy and Legal Theory"
    assert config["subtitle_ko"] == "법철학·법이론 리뷰"
    assert config["cadence"] == "quarterly"
    assert "Anglo-American analytic jurisprudence" in config["contemporary_issue_scope"]


def test_contemporary_quarterly_issue_scaffold_exists():
    base = ROOT / "issues" / "2026-Q2"
    assert (base / "agenda.md").exists()
    assert (base / "chief_editor_decisions.md").exists()
    assert (base / "final" / "en").is_dir()
    assert (base / "final" / "ko").is_dir()


def test_historical_config_declares_required_years_and_gates():
    config = historical_config()
    assert config["start_year"] == 1975
    assert config["interval_years"] == 5
    assert config["target_years"] == [1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]
    assert "approved_for_publication" in config["historical_issue_status"]
    assert config["publication"]["chief_editor_approval_required"] is True
    assert config["publication"]["stop_before_drafting_unless_approved"] is True


def test_historical_access_and_analysis_taxonomies_are_complete():
    config = historical_config()
    assert {
        "bibliographic_metadata_only",
        "abstract_or_review_only",
        "table_of_contents_only",
        "open_access_full_text",
        "chief_editor_supplied_full_text",
        "library_access_required",
        "unavailable",
    }.issubset(set(config["access_levels"]))
    assert {
        "bibliographic_notice",
        "abstract_or_review_based_note",
        "full_text_article_note",
        "full_text_review_essay",
        "retrospective_contextual_note",
    }.issubset(set(config["analysis_levels"]))


def test_historical_issue_scaffolds_have_required_files():
    required_files = [
        "agenda.md",
        "field_map.md",
        "journal_coverage_report.md",
        "book_coverage_report.md",
        "article_index.csv",
        "bibliography.bib",
        "retrospective_note.md",
        "uncertainty_note.md",
    ]
    required_dirs = ["source_dossiers", "drafts", "final/en", "final/ko"]
    for year in historical_config()["target_years"]:
        base = ROOT / "historical" / str(year)
        for relative in required_files:
            assert (base / relative).exists(), f"missing {relative} for {year}"
        for relative in required_dirs:
            assert (base / relative).is_dir(), f"missing {relative} for {year}"


def test_historical_coverage_matrix_has_access_and_approval_fields():
    matrix = ROOT / "historical" / "radar" / "historical_coverage_matrix.csv"
    with matrix.open("r", encoding="utf-8", newline="") as handle:
        fields = csv.DictReader(handle).fieldnames or []
    assert "access_level" in fields
    assert "analysis_level" in fields
    assert "importance_at_the_time" in fields
    assert "later_significance" in fields
    assert "recommended_action" in fields
    assert "chief_editor_priority" in fields


def test_historical_site_collection_exists():
    page = (ROOT / "site" / "pages" / "historical.md").read_text(encoding="utf-8")
    nav = yaml.safe_load((ROOT / "site" / "_data" / "navigation.yml").read_text(encoding="utf-8"))
    assert "Historical Issues" in page
    assert any(item["url"] == "/historical/" for item in nav["primary"])
    for year in historical_config()["target_years"]:
        assert (ROOT / "site" / "_historical_issues" / f"{year}.md").exists()
