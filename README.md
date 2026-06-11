# 법과 이유 / Law and Reasons

Law and Reasons is a Markdown-first, English-Korean bilingual review of legal philosophy and legal theory.

Subtitle: A Review of Legal Philosophy and Legal Theory.

한국어 부제: 법철학·법이론 리뷰.

It has two distinct editorial tracks:

1. contemporary quarterly issues under `/issues/YYYY-QN`
2. historical back issues under `/historical/YYYY`

The historical back issues reconstruct the field as it could reasonably have appeared in the target year, while clearly separating:

1. time-situated analysis
2. retrospective editor's notes
3. archival uncertainty

No issue, article note, translation, or public reconstruction is approved by default. The Chief Editor must approve source maps, coverage matrices, full-text requests, drafts, translations, and publication.

## Editorial Depth Policy

The review's standing policy is recorded in `config/editorial_depth.yml` and `editorial/publishing_depth_policy.md`. Published work should aim at leading Anglophone legal philosophy review depth: primary source research, representative journal coverage, canonical legal-philosophical literature, Postema-level historical context where relevant, SEP-level field orientation, and explicit access-level discipline.

Applied topics such as AI and computational legal reasoning are admissible only when they bear on core jurisprudential questions and are visible in serious legal philosophy venues. They do not replace the magazine's center of gravity: legal philosophy and legal theory.

The 2025 English and Korean model issues are temporarily published for editorial calibration at `/historical/2025/` and `/historical/2025/ko/`.

Korean translation follows the source-library translation policy by default. The local policy bridge is `editorial/korean_translation_policy.md`, which points to `/Users/jeyounson/GithubRepo/source-library/docs/source-translation-policy-2026-06-07.md`.

## Structure

- `/issues/YYYY-QN/`: contemporary quarterly issue workspace
- `/historical/YYYY/`: historical target-year issue workspace
- `/historical/radar/`: source registry, master bibliography, coverage matrix, timeline, and bias notes
- `/config/magazine.yml`: magazine identity and contemporary issue scope
- `/config/historical.yml`: historical program policy
- `/pipelines/`: scaffold and backlog generators
- `/site/`: Jekyll publication surface for clearly labeled historical issue pages
- `/.github/workflows/`: manual Chief Editor review workflows

## Generate A Contemporary Quarterly Issue

```bash
python3 pipelines/generate_issue.py --issue 2026-Q2
```

## Generate The Backlog

```bash
python3 pipelines/historical_backlog_plan.py
```

## Generate One Historical Issue Scaffold

```bash
python3 pipelines/historical_back_issue.py --target-year 2025 --depth standard
```

The generator creates source-map, bibliography, coverage-matrix, and full-text-request scaffolds. It stops before drafting.

## Source Access Rules

Every historical article or book chapter must be marked with one access level:

- `bibliographic_metadata_only`
- `abstract_or_review_only`
- `table_of_contents_only`
- `open_access_full_text`
- `chief_editor_supplied_full_text`
- `library_access_required`
- `unavailable`

Every note must also state its analysis level. Do not pretend to have read a work when only metadata, abstracts, tables of contents, or reviews are available.

## Local Checks

```bash
python3 -m pip install -r requirements.txt
pytest
bundle exec jekyll build --source site --destination docs
```

## Publication Rule

The website may show contemporary and historical issue placeholders and status pages. It must not publish reconstructed issue text, contemporary articles, or translations until Chief Editor approval is recorded.
