# Batch Document Workflows Design

## Goal

Review instruction files for single responsibility, extract explicit action items from the selected project documents, and validate project Markdown formatting. Process each input file independently and preserve source evidence.

## Scope and Inputs

- SRP review: every Markdown file directly under `instructions/`, including the catalog and newly added instruction files.
- Action extraction: `BACKLOG.md`, `project_spec.md`, and `work/jira-dashboard-requirements.md`.
- Markdown validation: project Markdown files, excluding `.git`, virtual environments, and build output directories.

## Components and Outputs

- `instructions/validate-instructions.agent.md` defines the semantic, per-file SRP review and its result schema.
- `tools/extract_action_items.py` extracts unchecked checklist items and explicit open requirements from each configured source. It preserves source file and line information and does not invent owners or due dates.
- `tools/validate_markdown.py` checks each Markdown file independently for UTF-8 readability, final newline, trailing whitespace, heading spacing and hierarchy, and balanced fenced code blocks.
- `reports/instruction-srp-audit.md` records each instruction file's purpose, responsibilities, evidence, SRP result, and recommendation.
- `reports/action-items.md` lists extracted actions with their source locations and any owner/date explicitly present.
- `reports/markdown-validation.md` lists per-file validation findings and a summary.

The scripts perform deterministic checks and extraction only. SRP decisions remain semantic review findings, not automated certainty.

## Processing and Error Handling

- Process files in stable path order and report each file separately.
- Continue after a file-level read or parse error, record the error with the path, and return a non-zero status if any errors or validation violations remain.
- Do not overwrite input documents.
- Keep extraction limited to explicitly open tasks and requirements; preserve wording and avoid duplicating a requirement already represented by a backlog task when equivalence is clear.
- Do not silently drop malformed content or fabricate missing metadata.

## Validation

- Add focused tests for parsing unchecked and checked tasks, source line preservation, duplicate handling, malformed/unreadable files, and each Markdown rule.
- Run both tools against the repository and review all generated reports for omissions and false positives.
- Refine instructions or rules if report results are inconsistent, then rerun the affected workflow.

## Non-goals

- Automatically rewriting or splitting existing instructions.
- Editing project source documents or changing task status.
- LLM/API calls from scripts.
- Enforcing arbitrary line-length or stylistic preferences not specified here.
