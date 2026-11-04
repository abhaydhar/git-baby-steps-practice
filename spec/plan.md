# Implementation Plan: Jira Sprint Dashboard Prototype

- **Status**: Draft; prototype scope is mock-only.
- **Source**: `spec/specification.md`, including the product-owner decisions recorded in its Prototype Scope Decisions section.
- **Constitution**: Follow `spec/constitution.md`. Do not change the required React 18/Vite, Node.js/Express, or PostgreSQL 15/Docker stack without an approved amendment.
- **Target**: A local, read-only demonstration using synthetic fixture data. This plan does not authorize implementation of live Jira integration or production access.

## Plan Outcome

Deliver a reproducible local application foundation and a small, clearly labeled presentation of synthetic Jira-like data. The prototype must not connect to Jira, authenticate real users, expose data through a dashboard API, persist Jira sprint/issue records, or suggest that mock data is current.

The prototype does not implement external-user access, Jira permission enforcement, issue-count completion percentages, additional summary metrics, a sprint timeline, interactive filters, manual/live refresh, or scheduled refresh. Related product requirements remain deferred; they are not considered satisfied by the prototype.

No dates or effort estimates are assigned. Exact compatible tool versions must be selected and documented before bootstrap as required by the constitution.

## Scope and Stop Conditions

### Included

- A separate `jira-dashboard/` application, isolated from the repository's Python calculator.
- React 18/Vite frontend and Node.js/Express backend, with PostgreSQL 15 available through Docker as required by the constitution.
- Synthetic, local-only sample data and a visible indication that it is mock data.
- Fixture status mapping directly to To Do, In Progress, or Done; unmapped statuses must never be treated as Done. A blocked category is shown only if explicitly represented in fixture data.
- A minimal read-only prototype presentation, limited to behaviors that do not require unresolved production access or metric decisions.
- Automated checks that prove the demo uses only mock data and does not make Jira or dashboard-data API calls.

### Excluded

- Real Jira or identity-provider connections, credentials, authentication, authorization, external users, Jira permission checks, or production-like access claims.
- Jira sprint/issue persistence, data synchronization, Jira API endpoints, or a cache of Jira data.
- Sprint completeness claims against a live or authoritative Jira source.
- Completion percentages, additional summary metrics, timeline, interactive filters, refresh controls, current-data claims, and scheduled jobs.
- Confluence automation, Jira issue mutations, and production deployment.

### Stop conditions

- Stop before any live Jira data flow, real-user access, or Jira data persistence. T0.1 remains blocked until its required technical validation and Jira/security-owner approvals are recorded.
- Stop before implementing an issue list if issue identification and presentation remain unresolved under G-16; do not invent issue keys, titles, links, sorting, or large-result behavior as product requirements.
- Stop before bootstrap if the exact compatible toolchain versions required by the constitution have not been selected and documented.
- If a requested prototype behavior conflicts with a deferred requirement or an unresolved clarification, record it for approval rather than inferring a design.

## Phases and Milestones

### Phase 0 — Baseline scope and acceptance

**Dependencies**: None.

**Work**

- Confirm that the Prototype Scope Decisions in `spec/specification.md` are the controlling boundary for this prototype; retain the broader requirements as future product scope.
- Reconcile `spec/tasks.md` and `spec/analyze.md` with the mock-only scope. Identify tasks that are prototype work, deferred, or blocked; do not leave live-Jira tasks appearing ready to execute.
- Resolve or explicitly defer the remaining clarification items that affect the prototype, especially G-16 (issue presentation), G-18 (toolchain versions), and any fixture/verification criteria needed for acceptance.
- Record the prototype's local-only demonstration and verification criteria in the task breakdown.

**Milestone M0 — Scope baseline approved**

- Prototype scope and deferred requirements are traceable in the specification and task list.
- T0.1 is still marked blocked; there is no implication of Jira or security-owner approval.
- No unresolved decision is silently converted into a product behavior.

### Phase 1 — Reproducible application foundation

**Dependencies**: M0.

**Work**

- Select and document compatible, supported Node.js, Express, Vite, Docker Engine, and Docker Compose versions. Keep React and React DOM on major version 18 and PostgreSQL on major version 15.
- Bootstrap frontend and backend projects under `jira-dashboard/`; keep manifests, lockfiles, scripts, and runtime configuration within their owning project roots.
- Configure PostgreSQL 15 through Docker and a migration workflow, without creating Jira sprint/issue tables or storing Jira-like records.
- Add the minimum backend operational surface required by the foundation (configuration validation and health/readiness checks); do not add a dashboard-data API or Jira adapter.
- Establish formatter, linter, test runner, build scripts, and local setup documentation. Use placeholders only; add no credentials.

**Milestone M1 — Clean local baseline**

- A clean checkout can install dependencies, start the required local services, run checks, and build the frontend/backend.
- PostgreSQL 15 starts through Docker; no Jira data schema or Jira connectivity is present.
- No secrets are committed or bundled into the frontend.

### Phase 2 — Synthetic fixture and status mapping

**Dependencies**: M1; fixture acceptance criteria from M0.

**Work**

- Create a small, deterministic fixture made entirely of invented data. Do not copy real Jira content, identifiers, people, or sensitive information.
- Keep the fixture local to the frontend/demo data boundary; do not expose it through an Express dashboard endpoint or write it to PostgreSQL.
- Represent the approved To Do / In Progress / Done mapping. Include an unmapped status test case; verify it is not silently counted as Done. Include blocked work only if explicitly represented in the fixture.
- Mark the fixture as synthetic in both code/documentation and the user-visible prototype.
- Do not claim the fixture is complete or representative of any Jira project, board, or sprint population.

**Milestone M2 — Safe deterministic demo data**

- Tests establish the expected fixture categories and mapping behavior.
- A repository scan/check confirms the fixture contains only invented sample values and no credentials.
- Fixture provenance and its limits are documented.

### Phase 3 — Minimal local prototype presentation

**Dependencies**: M2; resolve G-16 before adding an issue list.

**Work**

- Build a minimal read-only React presentation over the local fixture. Avoid adding screen-level acceptance claims, production visual design, or unapproved interaction behavior.
- Clearly label all rendered data as synthetic/mock and not current Jira data.
- Present only approved fixture information. Do not add timeline, completion percentage, additional summary metrics, interactive filters, refresh affordances, or Jira navigation.
- Do not render an issue list until G-16 is answered or that issue-list behavior is explicitly deferred. If deferred, keep the prototype at a non-issue-level demonstration.
- Keep frontend services free of Jira credentials and network calls. The Express backend must not serve dashboard data in this prototype.

**Milestone M3 — Mock-only demonstrator**

- The frontend builds and renders the approved local fixture.
- The UI does not imply live Jira connectivity, user-specific visibility, refresh recency, or production readiness.
- Any unresolved presentation requirement is visibly excluded from scope rather than guessed.

### Phase 4 — Verification and prototype handoff

**Dependencies**: M3.

**Work**

- Run frontend/backend unit tests, lint/format checks, and production builds.
- Verify status categorization, unmapped-status behavior, and the synthetic-data label.
- Verify there are no live Jira/identity calls, dashboard-data endpoints, Jira credentials, Jira sprint/issue persistence, or scheduler jobs.
- Smoke-test the required PostgreSQL 15 Docker service and confirm that no Jira records are persisted.
- Produce a requirement-evidence matrix that separates prototype acceptance from deferred FRs/SCs; record approved deferrals and unresolved owners without treating them as passed.
- Document local startup, fixture boundaries, known omissions, and the T0.1 stop condition.

**Milestone M4 — Prototype accepted**

- Applicable prototype tests and builds pass, or any unavailable check is explicitly reported.
- Evidence confirms the app is mock-only and conforms to the approved prototype exclusions.
- Deferred production requirements remain visible and are not represented as delivered.

## Future Production Gate — Not Authorized by This Plan

Production Jira work requires a separately approved plan revision after, at minimum:

1. T0.1 is unblocked with confirmed Jira/identity capabilities, a validated per-viewer access design, and explicit Jira- and security-owner approval.
2. The external-user policy, Jira endpoint/API and project scope, issue/status/completion semantics, and permitted fields are defined.
3. Permission-safe persistence, refresh behavior, scheduler compatibility, retention, and deletion are approved.
4. API contracts, screen-level behavior, filters, timeline, issue identification, accessibility/browser targets, and release evidence are specified or explicitly deferred.
5. Toolchain and deployment assumptions are recorded.

Until that gate is met, do not implement a live Jira adapter, Jira-backed API, synchronization, Jira data persistence, or real-user access.

## Requirement Traceability

| Requirement area | Prototype treatment |
|---|---|
| FR-001–FR-003 | Separate application and server/client boundaries may be established; no Jira data flow or privileged provider call is implemented. |
| FR-004 | Live sprint discovery and completeness are deferred; synthetic fixture only. |
| FR-005 | Interactive filters deferred. |
| FR-006 | Timeline and completion percentage deferred; no additional metrics. |
| FR-007 | Issue presentation is gated by G-16; no issue list until identification/presentation is resolved. |
| FR-008 | Fixture status mapping follows the approved prototype decision. |
| FR-009–FR-010 | Completion percentage and story-point reporting are not prototype acceptance behaviors. |
| FR-011–FR-012 | Manual/live refresh and scheduled refresh are deferred. |
| FR-013 | PostgreSQL 15 remains a stack requirement; no Jira sprint/issue records are persisted. |
| FR-014 | Provider/refresh handling is not exercised without provider integration; local errors must not be disguised as Jira outcomes. |
| FR-015–FR-016 | Real authentication, Jira permission enforcement, and external access are out of scope; T0.1 remains blocked. |
| FR-017 | Configuration governance is not implied by the prototype; unresolved details remain deferred. |
| FR-018–FR-019 | No Jira issue mutations; preserve the backend integration boundary for any future provider work. |
| SC-001–SC-004 | Live completeness, filters, completion percentage, and issue-field acceptance are not claimed. Fixture/status tests apply only where specified above. |
| SC-005–SC-007 | Scheduled and live refresh criteria are deferred, not passed. |
| SC-008–SC-009 | Real-user access and authorized Jira integration criteria are deferred, not passed. |

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Prototype is mistaken for live or permission-safe Jira access | Prominent mock-data labeling, no real data, and explicit T0.1/production gate. |
| Unresolved product decisions leak into implementation as assumptions | Keep G-16 and toolchain choices as entry gates; maintain a decision/deferral matrix. |
| Synthetic fixture is mistaken for completeness evidence | Document that no Jira source-of-truth comparison is performed. |
| Prototype grows into production integration without approvals | Keep Jira adapters, data APIs, Jira persistence, authentication, and scheduler out of scope; require a separately approved plan revision. |
| PostgreSQL is treated as permission-safe Jira storage by default | Do not create Jira data tables; require approved data isolation and retention design before any future persistence work. |
