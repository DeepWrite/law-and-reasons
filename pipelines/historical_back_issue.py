#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from lib import CONFIG, HISTORICAL, ensure_dir, iso_today, load_yaml, write_text


HISTORICAL_CONFIG = CONFIG / "historical.yml"

MODE_CHOICES = [
    "time_situated_issue",
    "retrospective_scholarly_issue",
    "retrospective_scholarly_with_time_situated_sections",
]

DEPTH_CHOICES = ["bibliographic", "standard", "deep"]
LANGUAGE_CHOICES = ["en", "ko", "all"]

YEAR_HYPOTHESES: dict[int, list[str]] = {
    1975: [
        "Hart after The Concept of Law",
        "early Dworkin and legal positivism under pressure",
        "rights discourse",
        "German postwar public law theory",
    ],
    1980: [
        "Dworkin, principles, and adjudication",
        "critical legal studies",
        "rights and liberalism",
        "systems theory and law",
    ],
    1985: [
        "interpretivism and the road to law as integrity",
        "critical legal studies",
        "constitutional rights theory",
    ],
    1990: [
        "post-Hart positivism and inclusive/exclusive positivism",
        "Habermas and discourse theory",
        "Alexy and rights theory",
    ],
    1995: [
        "authority, reasons, and positivism after Raz",
        "constitutional proportionality",
        "European integration",
    ],
    2000: [
        "global constitutionalism",
        "legal pluralism",
        "dignity and human rights",
        "analytical jurisprudence after the Hart-Dworkin debate",
    ],
    2005: [
        "constitutional pluralism",
        "proportionality",
        "legality and public reason",
        "private law theory",
    ],
    2010: [
        "global legal pluralism",
        "transnational law",
        "constitutional identity",
        "legal realism revival",
        "empirical jurisprudence",
    ],
    2015: [
        "algorithmic governance",
        "dignity",
        "populism and constitutionalism",
        "legal interpretation",
        "political constitutionalism",
    ],
    2020: [
        "pandemic legality",
        "emergency powers",
        "AI and law",
        "democratic backsliding",
        "platform governance",
        "rights under crisis",
    ],
    2025: [
        "generative AI",
        "institutional trust",
        "democracy and legality",
        "automated legal reasoning",
        "dignity and digital governance",
    ],
}

WORK_FIELDS = [
    "work",
    "author",
    "year",
    "language",
    "tradition",
    "topic",
    "source_type",
    "venue_or_publisher",
    "access_level",
    "analysis_level",
    "importance_at_the_time",
    "later_significance",
    "visibility_at_the_time",
    "relation_to_canonical_debates",
    "recommended_action",
    "notes",
]

COVERAGE_FIELDS = [
    "target_year",
    "work",
    "author",
    "year",
    "language",
    "tradition",
    "topic",
    "access_level",
    "analysis_level",
    "importance_at_the_time",
    "later_significance",
    "relation_to_canonical_debates",
    "recommended_action",
    "chief_editor_priority",
    "notes",
]


def load_historical_config() -> dict[str, Any]:
    return load_yaml(HISTORICAL_CONFIG)


def configured_years(config: dict[str, Any]) -> list[int]:
    years = config.get("target_years") or []
    return [int(year) for year in years]


def validate_target_year(target_year: int, config: dict[str, Any]) -> None:
    start = int(config["start_year"])
    interval = int(config["interval_years"])
    if target_year < start or (target_year - start) % interval != 0:
        raise ValueError(f"{target_year} is not on the configured {interval}-year historical interval from {start}")


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]] | None = None, force: bool = False) -> bool:
    if path.exists() and not force:
        return False
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows or []:
            writer.writerow(row)
    return True


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def year_hypothesis_text(target_year: int) -> str:
    hypotheses = YEAR_HYPOTHESES.get(target_year, ["TODO: identify historically plausible debates for this year."])
    return bullets(hypotheses)


def metadata(target_year: int, mode: str, language: str, depth: str, publish: bool) -> str:
    return f"""---
target_year: {target_year}
historical_issue: "Historical Issue: {target_year}"
status: proposed
chief_editor_status: proposed
mode: {mode}
language: {language}
depth: {depth}
created: "{iso_today()}"
publication_model: human_approved
publish_requested: {str(publish).lower()}
---
"""


def issue_files(target_year: int, mode: str, language: str, depth: str, publish: bool) -> dict[str, str]:
    front = metadata(target_year, mode, language, depth, publish)
    hypotheses = year_hypothesis_text(target_year)
    return {
        "agenda.md": f"""{front}
# Historical Issue: {target_year} Agenda

This is a reconstruction workspace, not a draft issue. No historical issue text, article note, translation, or publication is approved yet.

## Core Editorial Principle

Reconstruct legal philosophy and legal theory as they could reasonably have appeared in {target_year}. Keep three registers separate:

1. time-situated analysis: what could reasonably be seen from {target_year}
2. retrospective editor's notes: what later became important but was not yet visible
3. archival uncertainty: what cannot be confidently reconstructed from available sources

## Starting Hypotheses To Verify

These are prompts for source mapping, not findings.

{hypotheses}

## Required Issue Sections

1. Historical Editor's Note
2. Field Map of the Year
3. Journal and Book Coverage Report
4. Ten Works to Read in That Year
5. Debate Map
6. Anglo-American Jurisprudence
7. European Legal Theory
8. German Legal Philosophy / Public Law Theory
9. Concepts Under Pressure
10. Retrospective Note from the Present
11. Annotated Bibliography
12. Teaching Note
13. What Would Have Been Worth Watching Next?

## Chief Editor Choice Required

Default production order is reverse chronological reconstruction: 2025, 2020, 2015, 2010, 2005, 2000, 1995, 1990, 1985, 1980, 1975.

Available alternatives:

- chronological reconstruction
- theme-first reconstruction
- opportunistic reconstruction based on available sources

Record any change in `chief_editor_decisions.md`.
""",
        "chief_editor_decisions.md": f"""{front}
# Chief Editor Decisions: Historical Issue {target_year}

Silence is not approval. Use `approve`, `revise`, `reject`, or `hold`.

## Reconstruction Order

- Decision: hold
- Selected order: reverse_chronological_reconstruction
- Date:
- Notes:

## Source Map

- Decision: hold
- Date:
- Notes:

## Coverage Matrix

- Decision: hold
- Date:
- Notes:

## Full-Text Requests

- Decision: hold
- Date:
- Notes:

## Draft Authorization

- Decision: hold
- Date:
- Notes:

## Translation Authorization

- Decision: hold
- Date:
- Notes:

## Publication Authorization

- Decision: hold
- Date:
- Notes:
""",
        "field_map.md": f"""{front}
# Field Map of {target_year}

## Method

This field map must distinguish what was central, emerging, marginal, later important, overestimated by present readers, and underestimated by present readers. Do not upgrade later-famous works into {target_year} centrality without evidence of contemporary visibility.

## Central Then

- TODO: source-mapped traditions, debates, journals, and books central in or around {target_year}.

## Emerging Then

- TODO.

## Marginal Or Not Yet Visible

- TODO.

## Later Important But Not Clearly Visible Then

- TODO. Use only in retrospective framing.

## Present Readers May Overestimate

- TODO.

## Present Readers May Underestimate

- TODO.

## Archival Limits

See `uncertainty_note.md`.
""",
        "journal_coverage_report.md": f"""{front}
# Journal Coverage Report: {target_year}

## Coverage Rule

Verify that each journal was active and relevant in or around {target_year}. Do not infer debate centrality from later reputation alone.

## Candidate Journal Archives To Check

- Archiv fuer Rechts- und Sozialphilosophie
- Rechtstheorie
- Der Staat
- JuristenZeitung
- Harvard Law Review
- Yale Law Journal
- University of Chicago Law Review
- The Modern Law Review
- The Cambridge Law Journal
- Public Law
- The American Journal of Jurisprudence
- Oxford Journal of Legal Studies, if active for the target year
- Law and Philosophy, if active for the target year
- Ratio Juris, if active for the target year
- Legal Theory, if active for the target year
- Common Market Law Review
- European Law Journal, if active for the target year
- International Journal for the Semiotics of Law, if active for the target year

## Special Issues

| Journal | Issue | Year | Topic | Access level | Evidence of relevance | Action |
| --- | --- | ---: | --- | --- | --- | --- |

## Review Essays And Book Reviews

| Review | Work reviewed | Venue | Year | Access level | Use | Action |
| --- | --- | --- | ---: | --- | --- | --- |
""",
        "book_coverage_report.md": f"""{front}
# Book Coverage Report: {target_year}

## Coverage Rule

Treat books, translations, edited collections, festschrifts, and conference volumes as historically situated objects. Separate publication date, reception date, translation date, and later canonical status.

## Monographs

| Work | Author | Publisher | Year | Language | Access level | Visibility at the time | Action |
| --- | --- | --- | ---: | --- | --- | --- | --- |

## Edited Collections, Conference Volumes, Festschrifts

| Work | Editors | Publisher | Year | Language | Access level | Visibility at the time | Action |
| --- | --- | --- | ---: | --- | --- | --- | --- |

## Important Translations

| Work | Original year | Translation year | Language pair | Access level | Reception note | Action |
| --- | ---: | ---: | --- | --- | --- | --- |

## Reviews To Locate

| Work | Likely review venue | Reason to seek review | Action |
| --- | --- | --- | --- |
""",
        "debate_map.md": f"""{front}
# Debate Map: {target_year}

## Starting Hypotheses

These hypotheses must be revised or rejected after source mapping.

{hypotheses}

## Debate Nodes

| Debate | Visible in {target_year}? | Main traditions | Key sources | Under pressure | Later status |
| --- | --- | --- | --- | --- | --- |

## Faded Debates

- TODO.

## Minor Then, Important Later

- TODO. Keep this retrospective.
""",
        "ten_works.md": f"""{front}
# Ten Works To Read In {target_year}

Do not fill this list from hindsight alone. A candidate work needs a visibility-at-the-time note and an access-level note.

| Rank | Work | Author | Year | Language | Access level | Visibility at the time | Why a serious reader in {target_year} would read it |
| ---: | --- | --- | ---: | --- | --- | --- | --- |
""",
        "retrospective_note.md": f"""{front}
# Retrospective Note from the Present

This section may use later sources. It must remain clearly separated from time-situated analysis.

## What We Know Now

- TODO.

## Later Significance

- TODO.

## Later Canonization Risks

- TODO: note where contemporary visibility is uncertain or weak.
""",
        "uncertainty_note.md": f"""{front}
# Archival Uncertainty Note: {target_year}

## Source Limits

- TODO: missing full text, incomplete metadata, inaccessible archives, translation gaps.

## Paywalled Or Restricted Sources

- Do not bypass paywalls or restricted archives.
- Mark `access_level` accurately.
- Request Chief Editor-supplied files where needed.

## Inference Limits

- Do not infer detailed arguments from titles alone.
- Use reviews and later historiography cautiously.
- Distinguish contemporary reception from later canonical status.

## Open Questions

- TODO.
""",
        "teaching_note.md": f"""{front}
# Teaching Note: {target_year}

## Course Use

- TODO: how to teach this historical issue without presentism.

## Suggested Seminar Questions

1. Which debates were central in {target_year} but later faded?
2. Which later-canonical works were actually visible in {target_year}?
3. How did Anglo-American, European, and German legal theory differ at this moment?

## Reading Sequence

- TODO.
""",
        "full_text_requests.md": f"""{front}
# Full-Text Requests: Historical Issue {target_year}

Use this file to request Chief Editor-supplied files or library access for important inaccessible works. Do not bypass paywalls or restricted archives.

| Work | Author | Year | Current access level | Needed for | Recommended action | Chief Editor response |
| --- | --- | ---: | --- | --- | --- | --- |
""",
        "bibliography.bib": f"% Historical Issue {target_year}. Add only verified bibliographic records. Do not fabricate citations.\n",
    }


def readme_files(target_year: int) -> dict[str, str]:
    return {
        "source_dossiers/README.md": f"""# Source Dossiers: Historical Issue {target_year}

Create one dossier per source, debate, or source cluster. Each dossier must state access level, analysis level, visibility at the time, and later significance only where retrospective framing is explicitly allowed.
""",
        "drafts/README.md": f"""# Drafts: Historical Issue {target_year}

Drafting must wait until the Chief Editor approves the source map, coverage matrix, and full-text request plan.
""",
        "final/en/README.md": f"""# Final English: Historical Issue {target_year}

No English historical issue material belongs here until it is approved for publication.
""",
        "final/ko/README.md": f"""# Final Korean: Historical Issue {target_year}

Korean translation begins only after the English version is approved for translation, unless the Chief Editor explicitly approves Korean-first production.
""",
    }


def ensure_historical_issue(
    target_year: int,
    mode: str,
    language: str,
    depth: str,
    publish: bool = False,
    force: bool = False,
) -> Path:
    config = load_historical_config()
    validate_target_year(target_year, config)
    base = HISTORICAL / str(target_year)
    for subdir in ["source_dossiers", "drafts", "final", "final/en", "final/ko"]:
        ensure_dir(base / subdir)
    for relative, content in issue_files(target_year, mode, language, depth, publish).items():
        write_text(base / relative, content, overwrite=force)
    for relative, content in readme_files(target_year).items():
        write_text(base / relative, content, overwrite=force)
    write_csv(base / "article_index.csv", WORK_FIELDS, force=force)
    write_csv(base / "coverage_matrix.csv", COVERAGE_FIELDS, force=force)
    return base


def main() -> int:
    config = load_historical_config()
    parser = argparse.ArgumentParser(description="Create a historical back-issue reconstruction scaffold.")
    parser.add_argument("--target-year", type=int, default=max(configured_years(config)))
    parser.add_argument("--mode", choices=MODE_CHOICES, default=str(config.get("mode", MODE_CHOICES[-1])))
    parser.add_argument("--language", choices=LANGUAGE_CHOICES, default="en")
    parser.add_argument("--depth", choices=DEPTH_CHOICES, default="standard")
    parser.add_argument("--publish", action="store_true", help="Record a publish request, but do not publish without approval.")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    base = ensure_historical_issue(
        target_year=args.target_year,
        mode=args.mode,
        language=args.language,
        depth=args.depth,
        publish=args.publish,
        force=args.force,
    )
    print(f"Historical issue scaffold ready: {base.relative_to(HISTORICAL.parent)}")
    if args.publish:
        print("Publish was requested, but this scaffold does not publish without Chief Editor approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
