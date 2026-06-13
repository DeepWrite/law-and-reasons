from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BANNED_GENERIC_HEADINGS = {
    "Opening Issue",
    "Central Question",
    "Conceptual Clarification",
    "Evidence",
    "Argument",
    "Policy Or Civic Implications",
    "Further Reading",
    "Uncertainty Note",
}


def split_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    assert end != -1, path
    meta = yaml.safe_load(text[4:end]) or {}
    return meta, text[end + 5 :]


def h2_headings(body: str) -> list[str]:
    return [line[3:].strip() for line in body.splitlines() if line.startswith("## ")]


def public_temporary_model_issues() -> list[Path]:
    paths: list[Path] = []
    for path in sorted((ROOT / "site" / "_historical_issues").glob("*.md")):
        meta, _body = split_front_matter(path)
        if meta.get("publication_mode") == "temporary_model_publication":
            paths.append(path)
    return paths


def test_public_historical_model_issues_declare_agent_structured_body_generation():
    for path in public_temporary_model_issues():
        meta, _body = split_front_matter(path)
        assert meta.get("body_generation") == "agent_structured_historical_model", path
        assert meta.get("assigned_agents"), path
        assert isinstance(meta.get("section_editorial_agents"), dict), path


def test_public_historical_model_issue_sections_have_agent_owners():
    for path in public_temporary_model_issues():
        meta, body = split_front_matter(path)
        agent_map = meta["section_editorial_agents"]
        headings = h2_headings(body)

        assert "Editorial Agent Register" in headings or "편집 역할 등록" in headings, path
        missing = [heading for heading in headings if heading not in agent_map]
        assert not missing, f"{path} has sections without editorial-agent ownership: {missing}"


def test_public_historical_model_issues_do_not_reuse_generic_article_scaffold():
    for path in public_temporary_model_issues():
        _meta, body = split_front_matter(path)
        hits = BANNED_GENERIC_HEADINGS.intersection(h2_headings(body))
        assert not hits, f"{path} exposes generic article headings: {sorted(hits)}"


def test_historical_model_markers_match_public_agent_structure():
    for public_path in public_temporary_model_issues():
        meta, _body = split_front_matter(public_path)
        target_year = str(meta["target_year"])
        language = meta["language"]
        marker = ROOT / "historical" / target_year / "final" / language / "model_issue.md"
        marker_meta, marker_body = split_front_matter(marker)

        assert marker_meta.get("body_generation") == "agent_structured_historical_model", marker
        assert marker_meta.get("assigned_agents"), marker
        assert "section-level editorial-agent rule" in marker_body, marker


def test_magazine_config_declares_historical_agent_policy():
    config = yaml.safe_load((ROOT / "config" / "magazine.yml").read_text(encoding="utf-8"))
    policy = config["historical_editorial_agent_policy"]
    assert policy["body_generation"] == "agent_structured_historical_model"
    assert "Historical Jurisprudence Editor" in policy["required_roles"]
    assert "Final Managing Editor" in policy["required_roles"]
