#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from historical_back_issue import COVERAGE_FIELDS, YEAR_HYPOTHESES, configured_years, ensure_historical_issue, load_historical_config
from lib import HISTORICAL, SITE, ensure_dir, iso_today, write_text


PROGRESS_FIELDS = [
    "target_year",
    "production_order",
    "source_mapping_status",
    "bibliography_status",
    "source_review_status",
    "field_map_status",
    "translation_status",
    "publication_status",
    "chief_editor_approval_status",
    "next_action",
]

DEFAULT_ORDER = [2025, 2020, 2015, 2010, 2005, 2000, 1995, 1990, 1985, 1980, 1975]


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def read_existing_progress(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["target_year"]: row for row in csv.DictReader(handle)}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]] | None = None, force: bool = True) -> None:
    if path.exists() and not force:
        return
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows or []:
            writer.writerow(row)


def production_position(year: int, order: list[int]) -> str:
    if year not in order:
        return "future_interval"
    return str(order.index(year) + 1)


def status_for(path: Path, label: str) -> str:
    return label if path.exists() else "not_started"


def progress_rows(years: list[int]) -> list[dict[str, str]]:
    path = HISTORICAL / "progress_matrix.csv"
    existing = read_existing_progress(path)
    rows: list[dict[str, str]] = []
    for year in DEFAULT_ORDER:
        if year not in years:
            continue
        base = HISTORICAL / str(year)
        previous = existing.get(str(year), {})
        rows.append(
            {
                "target_year": str(year),
                "production_order": production_position(year, DEFAULT_ORDER),
                "source_mapping_status": previous.get(
                    "source_mapping_status",
                    status_for(base / "journal_coverage_report.md", "scaffolded"),
                ),
                "bibliography_status": previous.get("bibliography_status", status_for(base / "bibliography.bib", "scaffolded")),
                "source_review_status": previous.get(
                    "source_review_status",
                    status_for(base / "source_review.md", "scaffolded"),
                ),
                "field_map_status": previous.get("field_map_status", status_for(base / "field_map.md", "scaffolded")),
                "translation_status": previous.get("translation_status", "not_started"),
                "publication_status": previous.get("publication_status", "not_started"),
                "chief_editor_approval_status": previous.get("chief_editor_approval_status", "proposed"),
                "next_action": previous.get("next_action", "Chief Editor review of source map and coverage priorities"),
            }
        )
    return rows


def backlog_markdown(years: list[int]) -> str:
    rows = progress_rows(years)
    table = "\n".join(
        "| {target_year} | {production_order} | {source_mapping_status} | {bibliography_status} | {source_review_status} | {field_map_status} | {translation_status} | {publication_status} | {chief_editor_approval_status} | {next_action} |".format(**row)
        for row in rows
    )
    return f"""---
status: active
updated: "{iso_today()}"
production_order: reverse_chronological_reconstruction
---

# Historical Back-Issue Backlog

Default production order is reverse chronological reconstruction because recent sources are easier to verify and connect to the contemporary legal philosophy review.

Alternative orders remain available if the Chief Editor chooses them:

- chronological reconstruction
- theme-first reconstruction
- opportunistic reconstruction based on available sources

| Target year | Order | Source mapping | Bibliography | Source review | Field map | Translation | Publication | Chief Editor approval | Next action |
| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
{table}

## Rule

Do not produce full historical issues in bulk. Move one issue at a time from source mapping to bibliography, coverage matrix, Chief Editor approval, editorial source reviews, field map, draft, translation, and publication.
"""


def canonical_timeline(years: list[int]) -> str:
    blocks = []
    for year in years:
        hypotheses = YEAR_HYPOTHESES.get(year, ["TODO: identify source-grounded debates."])
        blocks.append(f"## {year}\n\nStatus: scaffolded, hypotheses only.\n\n{bullets(hypotheses)}\n")
    return f"""---
status: scaffold
updated: "{iso_today()}"
---

# Historical Canonical Timeline

This timeline is a production aid. It records initial hypotheses that must be verified through historical source mapping. It is not a retrospective canon and should not be used as evidence of contemporary centrality.

{chr(10).join(blocks)}
"""


def source_registry() -> str:
    return f"""---
status: scaffold
updated: "{iso_today()}"
---

# Historical Source Registry

This registry identifies source families useful for reconstructing historical legal philosophy and legal theory. It does not assume complete source availability. Every article or chapter must receive a public `access_level` and `analysis_level` before it is used.

Public registry files should say only what is needed for the public record: source type, public verification status, analysis level, and whether further editorial verification is needed. Do not publish filesystem paths or working notes.

## Access Levels

- `bibliographic_metadata_only`
- `abstract_or_review_only`
- `table_of_contents_only`
- `open_access_full_text`
- `editorial_review_required`
- `library_access_required`
- `unavailable`

## Analysis Levels

- `bibliographic_notice`
- `abstract_or_review_based_note`
- `full_text_article_note`
- `full_text_review_essay`
- `retrospective_contextual_note`

## Archive And Database Families

| Source family | Examples | Likely access level | Use | Cautions |
| --- | --- | --- | --- | --- |
| Law journal archives | Harvard Law Review, Yale Law Journal, Modern Law Review, Public Law, Cambridge Law Journal | library_access_required or table_of_contents_only | Anglo-American doctrinal and jurisprudential reception | Verify target-year availability and do not infer arguments from titles. |
| Philosophy and jurisprudence journals | The American Journal of Jurisprudence, Oxford Journal of Legal Studies, Law and Philosophy, Legal Theory, Ratio Juris | library_access_required or open_access_full_text | Analytic jurisprudence, natural law, interpretivism, legal positivism | Some journals did not exist for early target years. Mark active-year status. |
| German legal theory and public law journals | Archiv fuer Rechts- und Sozialphilosophie, Rechtstheorie, Der Staat, JuristenZeitung, Archiv des oeffentlichen Rechts | library_access_required | German legal philosophy, constitutional theory, public law theory | German terminology and reception history require cautious translation notes. |
| European and international law journals | Common Market Law Review, European Law Journal, International and Comparative Law Quarterly, European Journal of International Law | library_access_required or open_access_full_text | European integration, constitutional pluralism, transnational law | Separate legal theory from doctrinal institutional reporting. |
| Multidisciplinary archives | JSTOR, HeinOnline, Oxford Academic, Cambridge Core, SpringerLink, Wiley Online Library | library_access_required or abstract_or_review_only | Metadata, tables of contents, book reviews, public source records | Respect restricted archives, licenses, and platform terms. |
| Legal research platforms | Westlaw, Lexis, Beck-Online, Nomos eLibrary, Mohr Siebeck, De Gruyter | library_access_required | Law reviews, German and European monographs, commentaries, festschrifts | Access varies by institution and jurisdiction. |
| Working paper repositories | SSRN and institutional repositories | open_access_full_text or bibliographic_metadata_only | Working papers, early online circulation, later version trails | Historically appropriate mainly for later target years; distinguish upload date from publication date. |
| Bibliographic and citation databases | WorldCat, Library of Congress, Deutsche Nationalbibliothek, Google Scholar, Scopus, Web of Science | bibliographic_metadata_only | Publication facts, catalogue records, citation trails | Citation counts are retrospective and cannot prove target-year centrality. |
| Publisher catalogues | Oxford University Press, Cambridge University Press, Hart Publishing, Suhrkamp, Nomos, Mohr Siebeck, De Gruyter | bibliographic_metadata_only or table_of_contents_only | Monographs, edited collections, translations | Catalogue descriptions are not substitutes for argument reconstruction. |
| Reviews and review essays | Journal book reviews, review symposia, later historiographical essays | abstract_or_review_only or full_text_article_note | Contemporary reception and later contextualization | Mark whether the review is contemporary or retrospective. |
| Conference volumes and festschrifts | Edited collections, academy proceedings, commemorative volumes | bibliographic_metadata_only or library_access_required | Networks, schools, debate clusters | Often difficult to reconstruct without library access. |
| Encyclopedias and handbooks | Legal theory encyclopedias, philosophy of law handbooks, public law handbooks | retrospective_contextual_note | Later orientation and terminology | Use only in retrospective sections unless published by target year. |

## Source-Use Rule

For each work, record:

- access level
- analysis level
- visibility at the time
- later significance, only in a marked retrospective section
- relation to canonical debates
- recommended action
"""


def retrospective_bias_notes() -> str:
    return f"""---
status: scaffold
updated: "{iso_today()}"
---

# Retrospective Bias Notes

Historical issues must avoid presentism. The editorial team should not write as if later outcomes were already visible or as if later canonical works were necessarily central in the target year.

## Common Bias Risks

- Canonical backfilling: treating later-famous works as obviously central at publication.
- Citation hindsight: using later citation volume as evidence of contemporary importance.
- Translation distortion: ignoring delays between original publication, translation, and reception.
- Platform availability bias: privileging sources that are easy to access now.
- Anglo-American over-weighting: allowing accessible English sources to crowd out German and European debates.
- Doctrine-theory conflation: treating institutional or doctrinal legal developments as legal theory without showing the conceptual link.

## Required Countermeasures

- Add a visibility-at-the-time note for every major work.
- Separate time-situated analysis from retrospective notes.
- Mark source access honestly.
- Route important sources with incomplete verification to editorial source review.
- Keep archival uncertainty visible.
"""


def write_radar_files(force: bool = False) -> None:
    radar = HISTORICAL / "radar"
    write_text(radar / "historical_source_registry.md", source_registry(), overwrite=force)
    write_text(radar / "historical_bibliography_master.bib", "% Master historical bibliography. Add only verified records.\n", overwrite=force)
    write_csv(radar / "historical_coverage_matrix.csv", COVERAGE_FIELDS, force=force)
    write_text(radar / "canonical_timeline.md", canonical_timeline(configured_years(load_historical_config())), overwrite=force)
    write_text(radar / "retrospective_bias_notes.md", retrospective_bias_notes(), overwrite=force)


def site_page_for(year: int) -> str:
    return f"""---
title: "Historical Issue: {year}"
target_year: {year}
historical_status: proposed
mode: retrospective_scholarly_with_time_situated_sections
publication_mode: human_approved
time_situated: true
retrospective: true
coverage_note: "Source mapping is scaffolded; no reconstruction has been approved."
uncertainty_note: "Archival uncertainty will be tracked before drafting."
---
"""


def write_site_pages(years: list[int], force: bool = False) -> None:
    collection = SITE / "_historical_issues"
    for year in years:
        write_text(collection / f"{year}.md", site_page_for(year), overwrite=force)


def main() -> int:
    config = load_historical_config()
    years = configured_years(config)
    mode = str(config.get("mode", "retrospective_scholarly_with_time_situated_sections"))
    for year in years:
        ensure_historical_issue(year, mode=mode, language="en", depth="bibliographic", publish=False, force=False)
    write_text(HISTORICAL / "backlog.md", backlog_markdown(years), overwrite=True)
    write_text(HISTORICAL / "canonical_timeline.md", canonical_timeline(years), overwrite=True)
    write_csv(HISTORICAL / "progress_matrix.csv", PROGRESS_FIELDS, progress_rows(years), force=True)
    write_radar_files(force=False)
    write_site_pages(years, force=False)
    print(f"Historical backlog ready: {HISTORICAL.relative_to(HISTORICAL.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
