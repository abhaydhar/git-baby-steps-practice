---
name: validate-instructions
description: Review each project instruction document for one clear responsibility.
---

# Validate Instruction Responsibilities

Review every Markdown file directly in `./instructions/` one file at a time, including `main.agent.md` and this instruction.

## Review

- Read each file completely before assessing it.
- Identify its intended audience, primary purpose, and distinct responsibilities.
- Treat closely related steps that serve one outcome as one responsibility.
- Treat independent workflows, unrelated outputs, or unrelated triggers as possible responsibility boundaries.
- For the catalog, assess whether it only routes users to instructions and describes their scope.
- For an empty or unreadable file, mark it **Unassessable**; do not infer its purpose.
- Do not treat file length, number of headings, or number of bullets alone as evidence of an SRP violation.
- Do not edit files as part of the audit.

## Output

Write `reports/instruction-srp-audit.md` with:

- A summary of files reviewed and outcome counts.
- One table row per file with its relative path, intended purpose, responsibility assessment (`Pass`, `Concern`, `Fail`, or `Unassessable`), concrete evidence, and a recommended next step.
- Explicit source evidence for each concern or failure; distinguish observations from recommendations.
- A `## Catalog Coverage` section listing instruction files missing from the catalog.
- A `## Review Notes` section for limitations, including empty or unreadable files.

Do not claim an automated semantic decision. Preserve file paths and do not invent missing purpose or ownership.
