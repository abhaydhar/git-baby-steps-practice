# Implementation Tasks: Jira Sprint Dashboard Prototype

- **Status**: Draft; tasks cover only the approved mock-only prototype in [plan.md](./plan.md).
- **Specification**: [specification.md](./specification.md)
- **Constitution**: [constitution.md](./constitution.md)
- **Plan**: [plan.md](./plan.md)

## Task Rules

- `PT` IDs identify tasks for this prototype and do not replace or unblock the specification's T0.1 identity decision.
- Complete a task only after its dependencies are satisfied and every acceptance criterion has evidence.
- The prototype must use invented local data only. Do not connect to Jira or an identity provider, serve dashboard data through an API, persist Jira-like records, or imply data is current.
- An item described as deferred or unresolved is not complete and is not approved for implementation. Update this file and the specification if scope changes.
- Keep project files under `jira-dashboard/`; do not change the root Python calculator.

## Phase 0 — Baseline Scope and Acceptance

### PT0.1 — Establish the prototype scope baseline

**Depends on**: None

**Work**: Use the confirmed G-01 through G-14 decisions recorded in the specification to bound implementation. Preserve the mock-only boundary and distinguish future requirements from prototype acceptance.

**Acceptance criteria**:

- The specification records each confirmed G-01 through G-14 disposition and the plan/task list do not contradict those decisions.
- T0.1 remains blocked; no Jira-owner or security-owner approval is asserted.
- No live Jira, real user-data access, external-user access, Jira data persistence, API-backed dashboard data, interactive filters, completion percentage, timeline, or refresh is treated as prototype work.
- Unanswered review items are listed as unresolved or deferred, not silently decided.

### PT0.2 — Define the minimal synthetic fixture contract

**Depends on**: PT0.1

**Work**: Specify the smallest deterministic, invented fixture needed to demonstrate the approved status mapping without asserting Jira completeness or issue-presentation requirements.

**Acceptance criteria**:

- The fixture contract includes To Do, In Progress, Done, and an unmapped status case.
- Every fixture value is invented; it contains no copied Jira records, real people, credentials, or sensitive data.
- Mapping an unmapped status never classifies it as Done.
- The fixture is explicitly not a representative or complete Jira project/sprint dataset.
- The contract does not define issue identifiers, links, sorting, issue-list behavior, or additional metrics while G-16 and related presentation decisions remain unresolved.

### PT0.3 — Record remaining prototype gates and deferrals

**Depends on**: PT0.1

**Work**: Reconcile the unresolved findings in [clarify.md](./clarify.md) with the prototype plan without inventing user decisions.

**Acceptance criteria**:

- G-15 through G-23 are each classified as resolved, deferred, or blocking with the basis documented.
- G-16 is a gate for any issue-level presentation; if still unresolved, prototype UI work excludes issue lists and issue navigation.
- Toolchain versions required by the constitution are selected and documented before application bootstrap.
- Configuration governance, field/data policy, accessibility/browser targets, deployment, and release-evidence ownership are not treated as approved without a recorded decision.

### PT0.4 — Align the task analysis with the prototype plan

**Depends on**: PT0.1, PT0.3

**Work**: Update [analyze.md](./analyze.md) so its assessments describe the current prototype tasks and deferred production work rather than the superseded live-Jira task list.

**Acceptance criteria**:

- Every actionable `PT` task has a corresponding complexity, dependency, and risk assessment.
- The analysis distinguishes prototype tasks from blocked or deferred production work.
- No live Jira, authentication, synchronization, Jira-data persistence, or refresh task is presented as ready under the current plan.
- Task IDs and dependencies in the analysis resolve against this file.

**Milestone M0 — Scope baseline ready**: PT0.1–PT0.4 meet their acceptance criteria; no live Jira or real-user work is authorized.

## Phase 1 — Reproducible Application Foundation

### PT1.1 — Bootstrap the isolated frontend and backend

**Depends on**: M0, PT0.3

**Work**: Create the React 18/Vite frontend and Node.js/Express backend within the constitution's `jira-dashboard/` structure.

**Acceptance criteria**:

- Frontend and backend manifests, lockfiles, and source roots are under `jira-dashboard/frontend/` and `jira-dashboard/backend/`.
- The chosen compatible versions and runtime requirements are documented and pinned according to repository conventions.
- The frontend uses React 18 and Vite; the backend uses Node.js and Express.
- No Jira adapter, identity integration, dashboard-data API, Jira credentials, or Jira calls are introduced.
- Root calculator files and behavior are unchanged.

### PT1.2 — Configure PostgreSQL 15 for local development

**Depends on**: PT1.1, PT0.3

**Work**: Add Docker configuration and safe local settings for the constitution-required PostgreSQL service.

**Acceptance criteria**:

- The documented Docker configuration starts PostgreSQL 15 in the approved development environment.
- Readiness and shutdown can be verified without a Jira connection.
- Credentials are provided through local configuration; committed examples contain placeholders only.
- No Jira sprint or issue tables, fixture persistence, or Jira-data cache are created.

### PT1.3 — Establish backend runtime and migration foundations

**Depends on**: PT1.1, PT1.2

**Work**: Add configuration validation, health/readiness behavior, and a versioned migration workflow without creating Jira data features.

**Acceptance criteria**:

- Missing or invalid required configuration is reported explicitly.
- Health/readiness distinguishes an unavailable required database from a ready backend.
- A versioned migration can be applied and verified against a clean PostgreSQL 15 database.
- No route serves dashboard fixture data, and no Jira-specific schema or data is present.

### PT1.4 — Add repeatable development and quality commands

**Depends on**: PT1.1

**Work**: Configure the selected test, lint, formatting, and build tools for the frontend and backend.

**Acceptance criteria**:

- Documented commands exist for frontend/backend tests, linting, formatting checks, and builds.
- Commands run with the pinned toolchain from a clean checkout.
- A failing test, lint, format check, or build exits unsuccessfully.

### PT1.5 — Document local setup and safe configuration

**Depends on**: PT1.2, PT1.3, PT1.4

**Work**: Document prerequisites and the local development workflow.

**Acceptance criteria**:

- Setup instructions cover frontend/backend startup, PostgreSQL startup, tests, and builds.
- Environment variable names and safe placeholders are documented; no real credentials are included.
- A clean-checkout setup walkthrough succeeds without Jira access.

**Milestone M1 — Clean local baseline**: PT1.1–PT1.5 are accepted; the isolated app and PostgreSQL can be run and checked locally without Jira.

## Phase 2 — Synthetic Fixture and Status Mapping

### PT2.1 — Add deterministic local mock data

**Depends on**: M1, PT0.2

**Work**: Implement the approved synthetic fixture at the frontend/demo-data boundary.

**Acceptance criteria**:

- The fixture matches the approved contract and is deterministic across test runs.
- The fixture is local and is not fetched from Express, Jira, or another network service.
- The fixture is not written to PostgreSQL.
- Documentation and fixture naming identify it as synthetic; no completeness or representativeness claim is made.

### PT2.2 — Implement and test fixture status mapping

**Depends on**: PT2.1

**Work**: Map fixture statuses directly to To Do, In Progress, and Done, with explicit unmapped handling.

**Acceptance criteria**:

- Tests verify each approved category maps to itself.
- An unmapped status remains explicitly unmapped and cannot be treated as Done.
- Blocked is not a separate category unless explicitly present in approved fixture data.
- No completion percentage or additional summary metric is calculated.

**Milestone M2 — Safe deterministic demo data**: PT2.1 and PT2.2 pass, and fixture provenance and limits are documented.

## Phase 3 — Minimal Local Prototype Presentation

### PT3.1 — Render the approved local fixture

**Depends on**: M2

**Work**: Build a minimal, read-only React presentation of only the approved non-issue-level fixture information.

**Acceptance criteria**:

- The frontend renders data sourced only from the local synthetic fixture.
- A visible notice identifies the data as mock/synthetic and not current Jira data.
- The prototype does not imply live connectivity, user-specific visibility, production readiness, or refresh recency.
- No issue list, issue links, timeline, completion percentage, additional metrics, interactive filters, refresh control, or Jira navigation is present.
- If an issue-level presentation is later requested, work stops until G-16 is resolved and the specification is updated.

### PT3.2 — Verify the mock-only presentation behavior

**Depends on**: PT3.1

**Work**: Add focused frontend tests for the fixture rendering and prototype boundary.

**Acceptance criteria**:

- Tests verify the synthetic-data notice is rendered.
- Tests verify only approved fixture values/categories are shown and no issue-level or deferred controls appear.
- Tests do not call a live service or depend on a dashboard-data API.
- Frontend tests and production build pass.

**Milestone M3 — Mock-only demonstrator**: The app renders approved local fixture data without implying live Jira or unresolved product behavior.

## Phase 4 — Verification and Prototype Handoff

### PT4.1 — Run clean-environment project checks

**Depends on**: M3, PT1.5

**Work**: Run all applicable tests, static checks, builds, and database startup/migration checks from a clean setup.

**Acceptance criteria**:

- Frontend/backend tests, lint/format checks, and production builds pass, or unavailable checks are explicitly reported.
- PostgreSQL 15 starts through Docker and its migration workflow succeeds on a clean database.
- Setup does not depend on undocumented local state or committed secrets.

### PT4.2 — Verify prototype exclusion boundaries

**Depends on**: M3, PT4.1

**Work**: Inspect the source, configuration, routes, database schema, and runtime behavior for prohibited prototype features.

**Acceptance criteria**:

- No live Jira or identity-provider call, Jira endpoint, Jira credential, or dashboard-data API endpoint exists.
- No Jira sprint/issue records are persisted, and no scheduled refresh job is present.
- No UI claims Jira permission parity, external-user approval, data completeness, or currentness.
- Any violation blocks prototype acceptance until removed and rechecked.

### PT4.3 — Prepare prototype evidence and handoff documentation

**Depends on**: PT4.1, PT4.2

**Work**: Record what was tested, what the prototype demonstrates, and which product requirements remain deferred or blocked.

**Acceptance criteria**:

- The evidence matrix distinguishes prototype checks from deferred FRs/SCs; deferred criteria are not marked passed.
- Local startup instructions, fixture boundaries, known omissions, and T0.1's blocked status are documented.
- Remaining unresolved decisions have clear labels; no owner approval is inferred.

**Milestone M4 — Prototype accepted**: Applicable checks pass, mock-only boundaries are verified, and deferred product requirements remain explicit.

## Deferred or Blocked Work — Not Prototype Tasks

These items are not actionable under this task breakdown. They require a later user decision, a revised specification/plan, and where applicable required owner approval.

| Item | Disposition |
|---|---|
| T0.1 identity, Jira permission enforcement, live Jira access, and real-user data | **Blocked**. Remains blocked until technical validation and explicit Jira/security-owner approval are documented. |
| G-02 external stakeholder policy and real external access | Out of scope for this prototype; no population or data permission is approved. |
| G-03/G-04 live Jira API, project/board/sprint discovery, and source-of-truth completeness | Out of scope for this prototype. |
| G-06 completion percentage and issue-population edge cases | Deferred; no completion metric acceptance behavior in this prototype. |
| G-07 dashboard data API and live provider behavior | Out of scope; local fixture only. |
| G-09 Jira data persistence, isolation, retention, and deletion | Out of scope for this prototype; do not persist Jira-like records. |
| G-11/G-12 timeline and interactive filters | Out of scope for this prototype. |
| G-13/G-14 manual/live and scheduled refresh | Out of scope; criteria are deferred, not passed. |
| G-15 provider pagination, rate limits, retries, timeouts, and partial-result behavior | Not exercised without a Jira provider; define before any future Jira integration. |
| G-16 issue identification, details, links, sorting, and large-result behavior | Unresolved gate for any issue-level UI; no issue list in this prototype. |
| G-17 configuration governance, G-19 field/data handling, G-20 screen states, G-21 browser/accessibility, G-22 fixture provenance/counts, G-23 evidence owners | Unresolved or deferred; do not infer decisions from the prototype scope. |
| Production deployment, live integration, authorization, synchronization, or broader product release | Requires a separately approved plan revision and satisfaction of the future production gate in [plan.md](./plan.md). |
