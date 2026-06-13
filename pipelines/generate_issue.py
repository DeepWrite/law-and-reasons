#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lib import ISSUES, iso_today, quarter_for, require_issue_dirs, write_text


def issue_files(issue: str) -> dict[str, str]:
    return {
        "agenda.md": f"""---
issue: "{issue}"
status: proposed
chief_editor_status: proposed
created: "{iso_today()}"
---

# Law and Reasons {issue} Agenda

This is the contemporary quarterly issue workspace. No theme, table of contents, commissioned article list, draft, translation, or publication decision is approved yet.

## Candidate Focus

- TODO: identify major legal philosophy and legal theory debates for this quarter.
- TODO: distinguish current developments from historical back-issue reconstruction.
- TODO: identify source dossiers required before commissioning.
""",
        "chief_editor_decisions.md": f"""---
issue: "{issue}"
status: active
chief_editor: "Jeyoun Son"
chief_editor_ko: "손제연"
---

# Chief Editor Decisions

Silence is not approval. Use `approve`, `revise`, `reject`, or `hold`.

## Quarterly Theme

- Decision: hold
- Date:
- Notes:

## Final Table Of Contents

- Decision: hold
- Date:
- Notes:

## Commissioned Article List

- Decision: hold
- Date:
- Notes:

## Publication Merge

- Decision: hold
- Date:
- Notes:
""",
        "issue_en.md": f"""---
issue: "{issue}"
language: en
title: "Law and Reasons {issue}"
chief_editor_status: proposed
status: draft
---

# Law and Reasons {issue}

Draft contemporary issue scaffold. No article is approved for publication.
""",
        "issue_ko.md": f"""---
issue: "{issue}"
language: ko
title: "법과 이유 {issue}"
chief_editor_status: proposed
status: draft
---

# 법과 이유 {issue}

동시대 분기호 초안용 골격입니다. 발행 승인된 글은 없습니다.
""",
        "bibliography.bib": "% Add only verified sources. Do not add fabricated citations.\n",
        "uncertainty_note.md": f"---\nissue: \"{issue}\"\nstatus: draft\n---\n\n# Issue Uncertainty Note\n\n- TODO.\n",
    }


def issue_readme_files(issue: str) -> dict[str, str]:
    return {
        "source_dossiers/README.md": f"""# Source Dossiers: {issue}

Create public source dossiers only after the Chief Editor approves source review. Do not include filesystem paths, private working notes, or restricted-source details.
""",
        "drafts/en/README.md": f"""# English Drafts: {issue}

English drafting waits for theme, source dossier, and commissioned article approval.
""",
        "drafts/ko/README.md": f"""# Korean Drafts: {issue}

Korean drafting or translation waits for the relevant English or Korean-first authorization.
""",
        "reviews/README.md": f"""# Editorial Reviews: {issue}

Record durable review decisions here only when they are safe for the repository. Keep raw private review materials outside git.
""",
        "final/en/README.md": f"""# Final English: {issue}

No final English material belongs here until the Chief Editor approves publication.
""",
        "final/ko/README.md": f"""# Final Korean: {issue}

No final Korean material belongs here until the Chief Editor approves publication or translation.
""",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Law and Reasons quarterly issue scaffold.")
    parser.add_argument("--issue", default=quarter_for())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    base = require_issue_dirs(args.issue)
    for relative, content in issue_files(args.issue).items():
        write_text(base / relative, content, overwrite=args.force)
    for relative, content in issue_readme_files(args.issue).items():
        write_text(base / relative, content, overwrite=args.force)
    print(f"Issue scaffold ready: {base.relative_to(ISSUES.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
