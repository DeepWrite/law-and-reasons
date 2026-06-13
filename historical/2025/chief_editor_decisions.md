---
target_year: 2025
historical_issue: "Historical Issue: 2025"
status: temporary_model_issue_public
chief_editor_status: temporary_model_approved
mode: retrospective_scholarly_with_time_situated_sections
language: en
depth: standard
created: "2026-06-11"
publication_model: human_approved
publish_requested: true
---

# Chief Editor Decisions

## Temporary Model Approval

The user requested one current or historical issue to be temporarily approved and published to DeepWrite Pages as a model issue. The selected issue is Historical Issue: 2025.

## Temporary Korean Model Approval

The user subsequently requested that the Korean version also proceed and be temporarily approved for publication. The Korean model issue is approved for temporary public demonstration at `/historical/2025/ko/`.

## Korean Translation Policy Approval

The user instructed that Korean translation should adopt the internal Korean translation policy as its governing default. This policy is now recorded in `editorial/korean_translation_policy.md`, `config/editorial_depth.yml`, and `config/magazine.yml`. The current Korean model issue has been revised under that policy, with particular attention to distinction-preserving jurisprudential terms such as `reason/reasons/Reason`, `rule of recognition`, `internal point of view`, legal `validity`, Hohfeldian `power`, and interpretive-convergence `uptake`.

## Editorial Direction Applied

- The center is orthodox legal philosophy and legal theory.
- AI is not the frame. It is included only where leading legal philosophy venues treat it as a jurisprudential pressure point.
- The standing depth policy is recorded in `config/editorial_depth.yml` and `editorial/publishing_depth_policy.md`.
- The Korean version preserves the English model issue's source discipline, access-level caveats, orthodox legal-philosophy center, and the internal Korean translation policy's distinction-preserving term discipline.

## Editorial-Agent Structure Repair

The June 13 review found that the public 2025 model issue had a serious but narrower version of the DeepWrite Review failure mode: the issue had temporary approval and a strong legal-philosophy frame, but it did not record which editorial role was responsible for each public section. That allowed the table of contents to behave like a generic historical-issue scaffold rather than a section-by-section legal-philosophy reconstruction.

The repair records `body_generation: agent_structured_historical_model`, adds assigned editorial roles to the English and Korean public copies, renders an editorial-agent register in both languages, and adds regression tests requiring section-level role maps for any public temporary historical model issue.

## Still Required

- Permanent approval for the final 2025 issue.
- Full source-map approval.
- Final Korean translation approval.
