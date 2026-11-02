# Instruction SRP Audit

## Summary

- Instruction documents reviewed individually: 8
- Pass: 6
- Concern: 1
- Fail: 0
- Unassessable: 1

## Per-File Findings

| File | Intended purpose | Assessment | Evidence | Recommended next step |
|---|---|---|---|---|
| `instructions/main.agent.md` | Route users to the relevant project instructions. | Pass | Contains catalog entries, routing keywords, target scopes, and exceptions; it does not implement the workflows. | Keep catalog entries aligned with instruction files. |
| `instructions/create-status-report.agent.md` | Produce a concise weekly status report in a fixed structure. | Pass | All requirements define the input handling, sections, and constraints for one report-generation outcome. | No change needed. |
| `instructions/calculate-compound-interest.agent.md` | Calculate and present compound-interest results using the project CLI. | Pass | Input validation, CLI invocation, and result formatting are parts of one calculation workflow. | No change needed. |
| `instructions/calculate-sprint-velocity-ins.agent.md` | Calculate and present sprint velocity using completed story points. | Pass | Input validation, CLI invocation, and reporting all serve the same calculation outcome. | No change needed. |
| `instructions/creating-instructions.agent.md` | Create and maintain the project instruction system. | Concern | Covers authoring individual instructions, maintaining the catalog, IDE-specific setup, project scaffolding, and skill placement. These are related to the instruction system but span distinct lifecycle activities. | Keep the current cohesive scope; consider separating IDE/project scaffolding if it grows or becomes independently reusable. |
| `instructions/update-stale-open-tickets.agent.md` | Identify stale Jira tickets and prepare assignee follow-ups. | Pass | Input validation, filtering, grouping, and output formatting all support one stale-ticket follow-up workflow. | No change needed. |
| `instructions/validate-instructions.agent.md` | Assess each instruction document for one clear responsibility. | Pass | Defines one per-file semantic review and one audit output format. | No change needed. |
| `instructions/write-tests.agent.md` | Not determinable. | Unassessable | The file is empty, so it declares no purpose or workflow. | Add its intended instruction or remove the empty file after confirming ownership. |

## Catalog Coverage

- `instructions/write-tests.agent.md` is not listed in `instructions/main.agent.md`.
- The file is empty, so its missing entry cannot be described or routed accurately.
- `instructions/validate-instructions.agent.md` is listed in the catalog.

## Review Notes

- Assessments are semantic review findings, not automated proof.
- The empty `write-tests.agent.md` was not treated as an SRP pass or failure.
- No existing instruction file was changed as part of this audit.
