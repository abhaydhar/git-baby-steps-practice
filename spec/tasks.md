# Implementation Tasks: Jira Sprint Dashboard

- **Status**: Draft task breakdown; implementation remains gated by the decisions in this file.
- **Source plan**: [plan.md](./plan.md)
- **Feature specification**: [specification.md](./specification.md)
- **Clarification review**: [clarify.md](./clarify.md)
- **Constitution**: [constitution.md](./constitution.md)

## How to Use This Task List

- Complete tasks only after their dependencies and applicable decision gates are satisfied.
- Phase 1 setup may proceed in parallel with Phase 0 only for reversible work that does not access Jira, persist Jira data, or implement authorization.
- Do not begin Jira data access, shared persistence, scheduled synchronization, or user-facing Jira data until Gate 0 is satisfied.
- A task is complete only when all of its acceptance criteria pass and its verification evidence is recorded.
- If an approved decision changes the scope or design, update the specification and this task list before continuing.

## Phase 0 — Requirements and Integration Decisions

### T0.1 — Approve user identity and Jira permission model

**Depends on**: None

**Acceptance criteria**:

- The specification documents how dashboard users authenticate and how their trusted identity reaches the backend.
- It specifies how project, issue-security, and relevant field visibility are enforced on each data request.
- It states whether viewer delegation is supported and how unauthorized users are denied.
- It explains whether scheduled refresh is compatible with viewer-specific Jira permissions; a shared service-account dataset is not assumed safe.
- Security and Jira owners approve the model, or a documented blocking constraint is recorded.

**Current disposition (2026-11-04): Blocked.** The T0.1 decision record in `specification.md` documents the blocking constraint: Jira Server/API and identity-provider capabilities are unconfirmed, no access or scheduled-refresh model is selected, and security/Jira-owner approvals are not recorded. The blocking-constraint acceptance path is documented; the identity-model criteria remain unresolved. Do not treat this as approval or proceed with Jira authorization, data access, persistence, synchronization, or user-facing Jira data. Reopen this task when the required technical facts and owner decisions are available.

### T0.2 — Approve external stakeholder data policy

**Depends on**: None; coordinate with T0.1 as needed.

**Acceptance criteria**:

- The eligible external stakeholder population is defined.
- “Full dashboard access” is explicitly defined as feature access and the exact data/issue-detail visibility allowed.
- Required Jira accounts/permissions or other approved access prerequisites for external users are documented.
- The source conflict between full dashboard access and summary-only versus issue-level visibility is resolved in the specification.

### T0.3 — Confirm Jira API contract and data scope

**Depends on**: None

**Acceptance criteria**:

- Jira Server base URL, version, supported API version, network reachability, and required Jira/plugin capabilities are documented without committing credentials.
- Included Jira projects/boards and configuration ownership are specified.
- The source fields/API data for sprint identity, state, project/board association, and timeline dates are documented.
- Historical, active, future, archived, parallel, cross-project, and removed sprint handling is specified to the extent required by the approved scope.
- An authorized non-production Jira environment or controlled, representative API fixture is available for verification.

### T0.4 — Approve metric and status semantics

**Depends on**: T0.3

**Acceptance criteria**:

- Jira statuses are mapped to To Do, In Progress, Done, and (if in scope) Blocked, with an explicit rule for unmapped statuses.
- The issue population for totals is defined, including sub-tasks, multi-sprint issues, removed issues, and cross-project issues where applicable.
- Completion is defined, including how Done category and Jira resolution interact.
- Per-sprint and multi-sprint aggregation, filter effects, zero-issue behavior, and percentage precision are specified.
- Story points remain excluded from the count-based formula unless separately approved and specified.

### T0.5 — Approve refresh and stale-data behavior

**Depends on**: T0.1, T0.3

**Acceptance criteria**:

- The specification defines what happens on initial load and user-triggered refresh, including whether cached data may render while a refresh runs.
- Successful, failed, and partial refreshes have explicit definitions and user-visible outcomes; stale data cannot be represented as current.
- The scheduled refresh time zone/window, missed-run recovery, retries, overlapping-run behavior, and outage handling are specified.
- The schedule and any persisted refresh state are compatible with the approved viewer-permission model.

### T0.6 — Confirm feature boundary and blocked-work scope

**Depends on**: None

**Acceptance criteria**:

- The product owner confirms this task breakdown covers the Jira sprint dashboard only.
- Blocked work is either given a source, mapping, and acceptance behavior or explicitly excluded from the initial feature.
- Any Confluence automation is recorded as a separate feature specification and plan, not silently added here.
- The responsible team lead and the mechanism for reviewing configuration changes through Jira governance are identified, or recorded as a release-blocking decision.

### T0.7 — Finalize implementation-ready specification

**Depends on**: T0.1–T0.6

**Acceptance criteria**:

- `spec/specification.md` contains approved answers for the P0 findings C-01–C-03 and G-01–G-06, G-10, or explicitly accepted out-of-scope decisions.
- Requirements and success criteria affected by decisions are updated and remain consistent with `spec/constitution.md`.
- Each in-scope user story and success criterion has a repeatable verification method.
- No unresolved P0 item blocks building the authorized Jira read boundary.

**Milestone M0**: T0.7 is accepted; later phases may still be gated on remaining persistence, UX, governance, and deployment decisions.

## Phase 1 — Application Foundation

### T1.1 — Select compatible toolchain versions

**Depends on**: None; implementation must comply with the constitution stack constraints.

**Acceptance criteria**:

- Compatible Node.js, Express, Vite, test, lint, formatting, and migration tool versions are selected and documented.
- React 18 and PostgreSQL 15 remain the mandated versions; no constitution change is assumed.
- The intended scope for Docker/PostgreSQL (development and/or deployment) is stated for the environments being configured.

### T1.2 — Bootstrap isolated frontend and backend projects

**Depends on**: T1.1

**Acceptance criteria**:

- Frontend and backend project manifests exist under `jira-dashboard/frontend/` and `jira-dashboard/backend/`.
- The frontend is configured for React 18 and Vite; the backend is configured for Node.js and Express.
- The root Python calculator files and behavior are unchanged.
- No Jira calls, real credentials, Jira-backed UI, or shared Jira-data cache are added before T0.7.

### T1.3 — Add repeatable development and quality commands

**Depends on**: T1.2

**Acceptance criteria**:

- Documented commands exist for installing dependencies, running frontend/backend tests, linting/formatting, and building both applications.
- The commands run from a clean checkout using the documented toolchain.
- A failing test, lint, or build exits unsuccessfully rather than reporting success.

### T1.4 — Configure local PostgreSQL 15 with Docker

**Depends on**: T1.1

**Acceptance criteria**:

- The documented Docker configuration starts PostgreSQL 15 in the approved development environment.
- Database credentials are supplied through local environment configuration; committed examples contain placeholders only.
- Startup/readiness and shutdown can be verified without requiring a Jira connection.

### T1.5 — Establish backend runtime and migration foundation

**Depends on**: T1.2, T1.4

**Acceptance criteria**:

- Backend startup validates required environment configuration and reports invalid/missing values explicitly.
- Health/readiness behavior distinguishes an unavailable required database from a healthy service.
- The selected migration tool can apply a versioned migration to a clean PostgreSQL 15 database.
- No Jira-specific schema or data is added before the persistence decision gate in Phase 3.

### T1.6 — Document local setup and secret handling

**Depends on**: T1.2–T1.5

**Acceptance criteria**:

- Setup instructions document prerequisites, frontend/backend startup, database startup, tests, and builds.
- Environment variable names and placeholder examples are documented without real credentials.
- A clean-checkout setup walkthrough succeeds.

**Milestone M1**: T1.1–T1.6 are accepted; the isolated project can be built and tested locally without Jira access.

## Phase 2 — Domain Model, Jira Adapter, and Authorization Boundary

**Entry gate**: M0 and M1 accepted.

### T2.1 — Define validated application-owned domain models

**Depends on**: T0.7, T1.2

**Acceptance criteria**:

- Models cover configured Jira scope, sprint, issue, status mapping, filter selection, and refresh result using confirmed source fields.
- Invalid or unmapped provider values produce explicit validation results and cannot silently become Done or fresh success.
- Unit tests cover valid and invalid representative values.

### T2.2 — Implement viewer identity and authorization boundary

**Depends on**: T0.1, T0.2, T2.1

**Acceptance criteria**:

- The backend establishes viewer identity using the approved mechanism and rejects unauthenticated or unauthorized requests.
- Jira visibility is applied per viewer as specified; the browser cannot select or impersonate another viewer.
- Tests demonstrate that data visible to one test identity is not returned to a less-privileged identity.
- The implementation does not introduce an unapproved application role model.

### T2.3 — Implement the server-side Jira adapter

**Depends on**: T0.3, T2.1, T2.2

**Acceptance criteria**:

- Jira requests use the confirmed API version and server-side credentials/identity flow.
- Provider calls are isolated behind the backend integration boundary and return application-owned models.
- Jira credentials are absent from frontend bundles, source control, and logs.
- Adapter contract tests use controlled responses and do not require live Jira by default.

### T2.4 — Implement complete sprint and issue retrieval

**Depends on**: T0.3, T2.3

**Acceptance criteria**:

- Sprint and issue queries follow the confirmed project/board scope and include required past/current/future records.
- Pagination is followed until completion; tests detect truncated or repeated pages.
- Required status, assignee, due date, priority, issue type, project, sprint, and timeline fields are mapped as approved.
- Missing optional fields remain missing and are not fabricated.

### T2.5 — Implement explicit provider failure behavior

**Depends on**: T0.5, T0.3, T2.3

**Acceptance criteria**:

- Timeout, rate-limit, authorization, transient, permanent, and partial-result cases are classified according to the approved integration contract.
- Any retry behavior is bounded and limited to approved retryable failures.
- Incomplete pagination or partial retrieval is surfaced as incomplete and cannot be mistaken for a complete successful result.
- Logs/errors omit credentials and sensitive Jira content.

### T2.6 — Verify Jira adapter and authorization contracts

**Depends on**: T2.2–T2.5

**Acceptance criteria**:

- Automated tests cover normalization, pagination completeness, status mapping, unavailable fields, API errors, and permission-denied data.
- Cross-viewer tests cover at least one issue visible to one identity but not another.
- Tests pass with controlled responses; any live Jira test is explicitly authorized and isolated.

**Milestone M2**: Backend Jira reads are complete, normalized, server-side, and permission-safe under the approved access design.

## Phase 3 — Persistence and Refresh Pipeline

**Entry gate**: M2 accepted; persistence, cache isolation, retention/deletion, and scheduler behavior from the phase-specific decisions in `spec/plan.md` are approved.

### T3.1 — Define the approved persistence model

**Depends on**: M0, T2.1

**Acceptance criteria**:

- The specification states what PostgreSQL stores and why, including whether Jira issues/sprints are persisted.
- The data model identifies source keys, viewer/access partitioning if needed, refresh metadata, and deletion/retention behavior.
- Security review confirms stored data and query paths cannot widen a viewer's Jira visibility.

### T3.2 — Create versioned PostgreSQL migrations

**Depends on**: T3.1, T1.5

**Acceptance criteria**:

- Migrations create the approved schema from an empty PostgreSQL 15 database and can be verified after application.
- Migration status is versioned and reviewable; no manual undocumented schema step is required.
- Migration tests cover clean initialization and the repository's supported upgrade path.

### T3.3 — Implement permission-safe persistence and cleanup

**Depends on**: T2.2, T3.1, T3.2

**Acceptance criteria**:

- Reads/writes enforce the approved data-isolation policy for every viewer and scheduled process.
- Retention and deletion rules are implemented for removed/out-of-scope Jira records and revoked access as approved.
- Tests prove that rows from one permission scope cannot be queried by another.

### T3.4 — Implement idempotent synchronization

**Depends on**: T2.4–T2.5, T3.3

**Acceptance criteria**:

- Replaying the same complete source result does not create duplicates or unintended changes.
- A failed or partial fetch cannot replace a known-good result as if the refresh completed successfully.
- Source identifiers and approved mappings are preserved.
- Tests cover repeat runs, partial pages, transaction failure, and recovery.

### T3.5 — Implement independent scheduled refresh

**Depends on**: T0.5, T3.4

**Acceptance criteria**:

- The scheduler runs independently of dashboard sessions and meets the approved daily cadence/time zone.
- Overlapping runs, restart, missed runs, retry policy, and outage handling match the approved specification.
- Scheduled access does not bypass or weaken viewer-specific permission handling.
- Scheduler tests demonstrate the required cadence behavior and failure/recovery outcomes.

### T3.6 — Implement user-triggered refresh and refresh status

**Depends on**: T0.5, T3.4

**Acceptance criteria**:

- An authorized user can request a refresh through the approved backend flow.
- The result distinguishes success, failure, and partial completion and reports the last successful refresh accurately.
- Concurrent user and scheduled triggers follow the approved overlap policy.
- Tests verify that stale data is never labelled current after a failed or partial refresh.

**Milestone M3**: Persistence and daily/on-demand refresh satisfy approved isolation, idempotency, completeness, and failure semantics.

## Phase 4 — Dashboard API and Calculations

**Entry gate**: M3 accepted; filter, aggregation, issue-inclusion, status, and API error semantics are approved.

### T4.0 — Resolve dashboard interaction and presentation requirements

**Depends on**: M0; may be decided while Phases 1–3 are in progress.

**Acceptance criteria**:

- Filter cardinality, combination, reset behavior, option population, and effect on every displayed metric are specified.
- Required summary metrics and their formulas/empty-data behavior are enumerated, or the specification limits the promise to already-defined metrics.
- Timeline date range, ordering, overlap, missing dates, timezone, state, and interaction behavior are specified.
- Issue identification and display decisions include required identifiers/title/link, sorting, and large-result handling.
- Supported browsers/viewports and accessibility expectations are specified.
- Loading, first-run, not-configured, empty, stale, partial-refresh, unauthorized, and provider-error states are specified.
- The decisions are reflected in `spec/specification.md` and acceptance scenarios are testable.

### T4.1 — Define and document dashboard API contracts

**Depends on**: T4.0, M2

**Acceptance criteria**:

- Request/response schemas cover authorized scope, filter choices, sprint summaries, timeline, issue details, and refresh status as required.
- Error responses distinguish validation, authorization, provider, persistence, and partial-data failures.
- API documentation agrees with the implemented schemas.

### T4.2 — Implement authorized dashboard read endpoints

**Depends on**: T2.2, T3.3, T4.1

**Acceptance criteria**:

- Each endpoint validates input and applies viewer visibility before returning data.
- Unknown or unauthorized scopes are explicitly rejected or returned as the approved empty result; unrelated data is never substituted.
- Route tests cover authorized, unauthenticated, unauthorized, malformed, and provider/database failure cases.

### T4.3 — Implement status grouping and completion metrics

**Depends on**: T0.4, T2.1, T4.0–T4.1

**Acceptance criteria**:

- Metrics use the approved status mapping, issue population, and per-sprint/multi-sprint rules.
- Completion equals the approved completed issue count divided by total included issue count, with the approved display precision.
- Zero-issue scopes are not applicable; unmapped statuses follow their explicit rule.
- Unit tests cover boundary counts, empty sprints, filters, and multi-sprint aggregation.

### T4.4 — Implement filters consistently across results

**Depends on**: T0.4, T4.0–T4.3

**Acceptance criteria**:

- Sprint, project, assignee, and issue-type filters implement the approved selection cardinality and combination semantics.
- The same selected scope applies to issue lists, filter-dependent summaries, status distributions, and completion values.
- A selection matching no issues returns an explicit empty result without unrelated issues or misleading metrics.
- Tests cover every filter independently and the approved combinations.

### T4.5 — Verify API/data contract against fixtures

**Depends on**: T4.2–T4.4

**Acceptance criteria**:

- Controlled fixtures verify response schemas, permission filtering, required fields, metrics, and filter results.
- Expected and actual issue/sprint counts match the fixture's known complete source set.
- Tests pass without depending on live Jira.

**Milestone M4**: The frontend can consume stable, authorized API responses whose filters and metrics are verified.

## Phase 5 — React Dashboard Experience

**Entry gate**: M4 accepted; timeline, summary metrics, issue identification, external-user experience, browser/accessibility, and loading/error decisions are approved.

### T5.1 — Implement dashboard layout and sprint summaries

**Depends on**: M4 and approved UX decisions

**Acceptance criteria**:

- The React 18 dashboard presents the approved sprint summary metrics, timeline, status distribution, and completion value.
- Historical, active, and future sprints appear according to the confirmed default scope.
- The layout responds to the approved viewport/browser requirements.

### T5.2 — Implement issue details and filter controls

**Depends on**: T5.1, T4.4

**Acceptance criteria**:

- Available status, assignee, due date, and priority are displayed without invented values.
- Required filters expose available options and follow the approved selection/combination behavior.
- Issue identification, sorting, linking, and large-result handling follow the approved UX requirements.
- No Jira issue mutation or administrative controls are exposed.

### T5.3 — Implement load, refresh, and failure states

**Depends on**: T3.6, T4.2, T5.1

**Acceptance criteria**:

- Opening the dashboard and manual refresh trigger the approved backend refresh flow.
- Loading, first-run/no-data, empty-filter, stale-data, partial-refresh, unauthorized, and provider-error states are distinguishable.
- Failed or partial refresh data is never described as current or successful.
- Frontend tests cover success and each approved failure/state transition.

### T5.4 — Verify access and accessibility behavior

**Depends on**: T0.1, T0.2, T5.1–T5.3

**Acceptance criteria**:

- Authorized external users receive the approved functionality and data scope.
- UI behavior does not allow access beyond backend-enforced Jira permissions.
- Filters and data displays satisfy the approved keyboard, screen-reader, and non-color status requirements.
- Automated or documented checks cover the agreed browser and viewport matrix.

### T5.5 — Add frontend component and integration tests

**Depends on**: T5.1–T5.4

**Acceptance criteria**:

- Tests cover summary rendering, timeline data, issue fields, filter changes, refresh requests, and failure/empty states.
- Tests verify metric display matches API data and do not rely on a live Jira service.
- Frontend build and test commands pass from a clean checkout.

**Milestone M5**: All in-scope user stories are demonstrable against controlled data with consistent filters, metrics, and access behavior.

## Phase 6 — End-to-End Verification and Release Readiness

**Entry gate**: M5 accepted; release decisions, deployment target, and governance responsibilities are documented.

### T6.0 — Confirm deployment and operational readiness contract

**Depends on**: M0; final verification may occur during Phase 6.

**Acceptance criteria**:

- The deployment target and required network paths to Jira Server and PostgreSQL are documented.
- The production/runtime environment for the independent scheduler is identified.
- Approved backup, retention, recovery, support, and operational ownership expectations are documented.
- Deployment decisions do not conflict with the approved viewer-permission model or constitution.

### T6.1 — Run clean-environment build and database verification

**Depends on**: M1, M3, M5

**Acceptance criteria**:

- Frontend/backend builds, static checks, and automated suites pass from a clean checkout.
- PostgreSQL 15 starts through the approved Docker setup and migrations succeed on a clean database.
- Setup does not depend on undocumented local state or real committed secrets.

### T6.2 — Run end-to-end feature acceptance tests

**Depends on**: T6.1

**Acceptance criteria**:

- Tests cover historical/current/future sprint display, every required filter, status mapping, fields, empty sprints, refresh, and error recovery.
- Displayed sprint and issue counts match a known complete fixture, including paginated source results.
- FR-001–FR-019 and SC-001–SC-009 are traced to test evidence or an explicitly approved deferral.

### T6.3 — Run authorized Jira integration validation

**Depends on**: T0.3, T2.6, T6.2

**Acceptance criteria**:

- Authorized integration tests pass against the confirmed Jira Server/API version and configured project scope.
- Returned historical, active, and future sprint data is compared with a known Jira source-of-truth count.
- Provider access, pagination, mappings, and network behavior match the approved contract.

### T6.4 — Run security and permission-isolation checks

**Depends on**: T2.6, T3.3, T4.2, T5.4

**Acceptance criteria**:

- Tests cover unauthenticated access, cross-viewer data leakage, external-stakeholder policy, input validation, and error disclosure.
- A build/log review finds no Jira credentials in the client bundle, source-controlled files, or logs.
- Any discovered permission leak blocks release until corrected and re-tested.

### T6.5 — Verify scheduler and recovery operations

**Depends on**: T3.5, T3.6

**Acceptance criteria**:

- The scheduler operates with no dashboard session and satisfies the approved cadence.
- Restart, downtime, missed run, Jira outage, duplicate trigger, partial pagination, and recovery cases are exercised.
- Refresh status remains truthful; stale or partial data is not represented as fresh successful data.

### T6.6 — Complete operational and governance readiness

**Depends on**: T0.6, T6.0–T6.5

**Acceptance criteria**:

- Team-lead ownership and configuration review through the approved Jira governance process are documented and demonstrated.
- Deployment connectivity, environment setup, approved backup/retention behavior, and support/recovery instructions are verified.
- Remaining limitations have an explicit owner and approval; no open acceptance-critical issue is hidden.

**Milestone M6**: Release candidate meets all approved acceptance criteria, permission tests pass, and deployment/operations are verified.

## Requirement Traceability

| Requirements | Task coverage |
|---|---|
| FR-001–FR-003 | T1.1–T1.6, T2.2–T2.3 |
| FR-004–FR-010 | T0.3–T0.4, T2.1–T2.6, T4.3–T5.2 |
| FR-011–FR-014 | T0.5, T3.1–T3.6, T5.3, T6.5 |
| FR-015–FR-016 | T0.1–T0.2, T2.2, T3.3, T5.4, T6.4 |
| FR-017 | T0.6, T1.6, T6.6 |
| FR-018–FR-019 | T2.3, T2.6, T4.2, T5.2, T6.4 |
| SC-001–SC-004 | T2.4, T4.3–T4.5, T5.1–T5.2, T6.2–T6.3 |
| SC-005–SC-007 | T0.5, T3.5–T3.6, T5.3, T6.5 |
| SC-008–SC-009 | T0.1–T0.3, T6.3–T6.4 |
