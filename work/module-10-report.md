# Module 10 Completion Report

## Instruction Files
C:\workspace\hello-genai\work\module03-task\instructions\create-status-report.agent.md
C:\workspace\hello-genai\work\module03-task\instructions\creating-instructions.agent.md
C:\workspace\hello-genai\work\module03-task\instructions\main.agent.md
C:\workspace\hello-genai\work\module03-task\instructions\update-stale-open-tickets.agent.md
C:\workspace\hello-genai\work\module03-task\instructions\write-tests.agent.md

## main.agent.md Contents
# Instruction Catalog

- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Generate concise weekly status reports in Markdown.
  + Keywords: weekly status report, status update, accomplishments, blockers, next week
  + Target: `**/*.md`
  + Exceptions: use the standard status-report structure only

---

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — Create and maintain project instruction files and the instruction catalog.
  + Keywords: create instruction, create instructions, add workflow, setup instruction, instruction catalog
  + Target: `**/*.md`
  + Exceptions: apply only when creating or updating instruction files

---

- [`./instructions/update-stale-open-tickets.agent.md`](./update-stale-open-tickets.agent.md) — Identify users whose Jira tickets remain open from past sprints and prepare a concise update.
  + Keywords: stale tickets, past sprints, open tickets, Jira assignee update, sprint follow-up
  + Target: `**/*.md`
  + Exceptions: use only when processing Jira issue data for unresolved past-sprint work

---

- [`./instructions/main.agent.md`](./main.agent.md) — Catalog of instructions for this project.
  + Keywords: instructions, catalog, workflow, rules
  + Target: `**/*.md`

## Sample Instruction
- File: update-stale-open-tickets.agent.md
- Contents:
---
name: update-stale-open-tickets
description: Identify assignees with Jira tickets still open from past sprints and prepare the update message or action list.
---

- Accept the input as a Jira export or structured issue list with these fields: `issue_key`, `summary`, `status`, `assignee`, `sprint_name`, `sprint_end_date`, `updated_at`, `created_at`.
  + If the source is CSV, treat each row as one issue and require all required fields to be present.
  + If the source is JSON, treat it as an array of issue objects with the same field names.

- Filter the dataset to tickets that meet all of these conditions:
  + `status` is still open or not resolved
  + `sprint_name` belongs to a prior sprint or a sprint that has already ended
  + the ticket is not already marked as `Done`, `Closed`, or `Resolved`
  + the issue is still assigned to a valid user

- For each remaining ticket, compute the stale-ticket signal:
  + `days_open = today - created_at` or `today - updated_at` when the workflow needs recency-based handling
  + `sprint_overlap = whether the issue belongs to a closed or completed sprint`
  + `owner = assignee` and `issue_link = jira_url + issue_key`

- Group the filtered tickets by assignee and sort each group by oldest open ticket first.
  + Keep the oldest items at the top of the list so follow-up is prioritized.
  + Exclude tickets that are already on the current sprint plan unless the user explicitly wants them included.

- Build the update payload for each assignee using this format:
  + `assignee_name`
  + `total_open_past_sprint_tickets`
  + `ticket_list` with each item containing `issue_key`, `summary`, `sprint_name`, `days_open`, `status`, `issue_link`
  + `recommended_action` such as `resolve`, `reassign`, `move to current sprint`, or `confirm status`

- Produce the final output in Markdown with exactly these sections in this order:
  + `## Assignee Updates`
  + `## Summary`
  + `## Recommended Actions`

- In `## Assignee Updates`, list each assignee as a bullet with the affected tickets beneath it.
  + Use one bullet per assignee, and one nested bullet per ticket.
  + Include the ticket key, summary, sprint, and age in days.

- In `## Summary`, report totals only:
  + total assignees affected
  + total stale open tickets
  + oldest ticket age
  + number of tickets that require reassignment or escalation

- In `## Recommended Actions`, provide only actionable next steps.
  + Prioritize resolution, reassignment, or confirmation of ownership.
  + Keep actions explicit and operational.

- Constraints:
  + Never update or reassign tickets without the user's approval or the project's defined workflow.
  + Do not include resolved, closed, or current-sprint tickets unless explicitly requested.
  + Ignore duplicates and malformed rows rather than guessing missing values.
  + Keep the output factual; do not invent ticket metadata, assignee names, or sprint dates.
  + Use only Jira data provided in the input; do not infer missing values beyond the available fields.
  + If no stale tickets are found, return a single explicit result: `No stale open tickets found for past sprints.`
  + Keep the output concise, readable, and operational, with no marketing or filler language.
