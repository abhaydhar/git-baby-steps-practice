# Instruction Catalog

- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Battle-tested: generates concise weekly status reports in Markdown.
  + Keywords: weekly status report, status update, accomplishments, blockers, next week
  + Target: `**/*.md`
  + Exceptions: use the standard status-report structure only; reject malformed numbered lists and stray text

---

- [`./instructions/calculate-compound-interest.agent.md`](./calculate-compound-interest.agent.md) — Use the compound-interest CLI and present its results.
  + Keywords: compound interest, interest calculation, principal, annual rate, compounding frequency
  + Target: compound-interest calculation requests
  + Tool: `./tools/compound_interest.py`
  + Exceptions: ask for missing inputs; annual rate is entered as a percentage

---

- [`./instructions/calculate-sprint-velocity-ins.agent.md`](./calculate-sprint-velocity-ins.agent.md) — Use the sprint-velocity CLI to total completed story points for a project.
  + Keywords: sprint velocity, story points, completed points, project code
  + Target: sprint-velocity calculation requests
  + Tool: `./tools/sprint-velocity.py`
  + Exceptions: requires a project code and one or more completed story-point values

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