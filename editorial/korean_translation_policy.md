---
status: active
source_policy_ref: internal Korean translation policy
applies_to:
  - Korean issue translations
  - Korean model issues
  - Korean source notes
---

# Korean Translation Policy

Law and Reasons adopts the internal Korean translation policy as its default Korean translation policy. The governing source is:

- the internal internal Korean translation policy.

Public Law and Reasons repository files should refer to the policy by name rather than publishing local working paths.

The internal translation policy is not merely a style preference. It is a term-discipline and argument-preservation rule. Korean translations should preserve distinctions made by the source text unless a documented source-level or issue-level reason justifies collapsing them.

## Core Rule

Prefer distinction-preserving Korean over smooth paraphrase when the source uses neighboring terms as part of its legal-philosophical architecture. If a translation collapses distinct source terms into one Korean expression, the reason must be recorded in a translation note.

## Standing Regression Guards

The following families must be checked in Law and Reasons Korean publication work:

- `law`, `the law`, `a law`, `laws`: preserve domain, specified law, countable law, and plural laws where they matter.
- `reason`, `a reason`, `reasons`, `Reason`: keep countable reasons separate from the faculty or tradition of reason.
- `source`, `foundation`, `basis`, `ground`, `reference`: keep 원천, 토대, 기초, 근거, 참조 apart.
- `rule of recognition`: use `승인 규칙`.
- `internal point of view` / `external point of view`: use `내부적 관점` / `외부적 관점`.
- legal `validity`: use `유효성`, not logical `타당성`.
- `obligation`, `duty`, `being obliged`: use `의무`, `책무`, and `하지 않을 수 없음` unless a local note justifies a smoother surface.
- Hohfeldian or Hartian `power`: use `권한`; do not default to `권능` or `형성권`.
- `uptake`: use `화행적수인` for Austinian or interpretive-convergence uptake, while keeping Hartian `acceptance` as `수용`.
- `correctness`, `rightness`, `validity`, `justification`, and `legitimacy`: preserve 올바름, 옳음, 유효성/타당성, 정당화, 정당성.

## Two-Dimensional Review Standard

Korean translation review must assess two dimensions independently.

**1. Term discipline** — Does the Korean version preserve the jurisprudential distinctions of the source text? Do the standing regression guards above pass? This is the primary and non-negotiable dimension.

**2. Prose quality** — Does the Korean version read as natural Korean legal-philosophical scholarship, free of 번역투 (translation-ese)? Would a Korean reader encountering the text alone find it coherent and well-formed as Korean academic prose?

Both dimensions must pass before `translation_status: checked` can be recorded. A translation that preserves all term distinctions but reads as mechanical English calque has not passed review. Conversely, polished Korean prose that collapses a term distinction has also not passed.

The prose quality standard is defined in `editorial/style_guide_ko.md`. The most common prose failures are: mechanical calquing of "It is…" as "그것은/이것은…"; using "도착하다" for the arrival of abstract concepts; over-long pre-nominal modifier chains; and direct borrowing of English section-heading conventions.

## Relation to Reader-Facing Style

Law and Reasons may polish Korean prose for readability, but readability cannot erase a jurisprudential distinction. Where the first occurrence of a term is likely to be ambiguous, keep the English term in parentheses.

## Current Model Issue Note

The 2025 Korean model issue has been revised under this policy. It remains temporarily approved rather than final; permanent publication requires a separate translation review against internal translation term memory.
