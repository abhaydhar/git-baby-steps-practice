# Implementation Plan: Jira Sprint Dashboard

- **Status**: Draft plan; implementation is gated on the decisions below.
- **Scope**: Implement the Jira sprint dashboard in `spec/specification.md`. Confluence automation is a separate scope and is not included here.
- **Constitution**: All phases must comply with `spec/constitution.md` (React 18/Vite, Node.js/Express, PostgreSQL 15 via Docker, server-side integrations, explicit failures, and verified changes).

## Plan Outcome

Deliver a read-only dashboard that meets the feature specification's functional requirements FR-001–FR-019 and success criteria SC-001–SC-009. The existing `jira-dashboard/` directory is only an empty skeleton; it has no package manifests or working application. This plan includes bootstrapping and validation of that project.

No schedule estimates are assigned because deployment, Jira access, and operational constraints have not been confirmed.

## Implementation Gates

### Gate 0 — Resolve P0 blockers before Jira data flows

Update the specification with approved answers for the following before implementing authorization, Jira data access, persistence of Jira data, synchronization, or user-facing issue data:

1. **Identity and authorization**: How a dashboard visitor authenticates; how the backend applies that viewer's Jira project, issue-security, and relevant field visibility; and how unauthorized access is denied. Resolve viewer delegation and whether scheduled synchronization can preserve viewer-specific permissions. A shared service-account cache must not widen access.
2. **External access**: Which external stakeholders are eligible, what “full dashboard access” means, and whether they can see issue-level data or only summaries. Resolve the conflict between source requirements for full access and the unresolved data policy.
3. **Jira contract and scope**: Jira Server URL/version/API, network access, configured project or board scope, sprint discovery and field mappings, and required API capabilities.
4. **Metric semantics**: Status mapping, treatment of unmapped/blocked work, included issue population (including sub-tasks and issues in multiple sprints), definition of completion, aggregation across selected sprints, and percentage precision.
5. **Refresh contract**: What users see during refresh and after failures, treatment of cached data, definition of a successful/partial run, schedule window/time zone, retries and missed-run recovery, and how the daily job remains compatible with per-viewer Jira permissions.
6. **Feature boundary**: Confirm this plan covers the Jira dashboard only and whether “blocked” work is in scope. Create a separate specification and plan for any Confluence automation.

**Exit condition**: P0 findings C-01–C-03 and G-01–G-06, G-10 in `spec/clarify.md` are resolved or explicitly accepted as out of scope, acceptance criteria are testable, and the resulting design remains compliant with the constitution. If Jira-native per-viewer visibility cannot be reconciled with the selected authentication and scheduled-refresh model, stop and revise the product/authentication design before proceeding.

### Phase-specific decision gates

Resolve each decision before the phase that depends on it; unrelated open questions need not block safe setup.

| Gate | Review findings | Required decision before proceeding |
|---|---|---|
| Application bootstrap | G-15 | Choose compatible Node.js, Express, Vite, test, and migration tool versions; define where Docker/PostgreSQL is required. |
| Jira integration | G-01–G-06, G-13, G-18 | Confirm viewer identity/visibility, Jira API contract, project/sprint discovery, status and issue-count rules, permitted fields, pagination, rate limits, retries, and partial-result behavior. |
| Persistence and scheduler | G-10–G-13, G-18 | Decide what data PostgreSQL stores, permission-safe isolation, retention/deletion, refresh success/failure states, schedule window/time zone, and recovery/concurrency policy. |
| Dashboard API and UX | G-07–G-09, G-16–G-19 | Define filter selection and combination, metrics, timeline behavior, issue identification/navigation, accessibility/browser targets, and loading/empty/error states. |
| Release acceptance | G-14, G-20–G-22 | Define configuration governance, measurable completeness and access tests, deployment evidence, feature boundary, and any approved deferrals. |

## Phases and Milestones

### Phase 0 — Requirements and integration decisions

**Tasks**

- Confirm and document all Gate 0 decisions with the product owner, Jira administrator, security owner, team lead, and external-stakeholder policy owner as applicable.
- Update `spec/specification.md` to replace unresolved alternatives with the approved behavior; retain only genuine future-scope questions.
- Establish a Jira test instance or controlled integration environment and non-production credentials with the approved least-privilege model.
- Confirm Docker/PostgreSQL availability in the development environment. Validate deployment-specific availability at the deployment decision gate.

**Milestone M0 — Implementation-ready specification**

- Identity/access behavior, Jira API contract and scope, metric semantics, external-user policy, and refresh behavior are documented well enough to build the authorized Jira read boundary.
- Each in-scope user story and success criterion has a repeatable verification method.
- No open P0 contradiction or decision blocks implementation.
- Persistence/retention, detailed UI behavior, configuration governance, and production deployment decisions remain phase-specific gates if not required to safely implement the Jira read boundary.

### Phase 1 — Application foundation

**Dependencies**: None for the safe bootstrap tasks listed here. This phase may run in parallel with Phase 0 only for reversible setup that does not make Jira calls, persist Jira data, or implement an access model.

**Tasks**

- Bootstrap independent frontend and backend Node.js projects inside `jira-dashboard/`, preserving the existing repository's Python calculator boundary.
- Pin compatible dependency/runtime versions, keeping React 18 and PostgreSQL 15 as required by the constitution.
- Add development scripts, formatting/linting, unit-test runners, and a repeatable build for each application.
- Add Docker configuration for PostgreSQL 15 appropriate to the confirmed environments; keep credentials in environment configuration and commit placeholders only.
- Add backend configuration validation, structured error handling, health/readiness endpoints, and a versioned migration workflow.
- Document local setup, required environment variables, and safe secret handling.
- Do not add a Jira adapter, real credentials, Jira-backed UI, or shared Jira-data cache before Gate 0.

**Milestone M1 — Reproducible local baseline**

- A clean checkout can install dependencies, start the frontend/backend and PostgreSQL, apply migrations, run tests, and build without relying on undocumented machine state.
- No secret values are committed or sent to the frontend bundle.

### Phase 2 — Domain model, Jira adapter, and authorization boundary

**Dependencies**: M0, M1.

**Tasks**

- Define application-owned types and validation for configured Jira scope, sprint, issue, status-category mapping, filter selection, and refresh result.
- Implement the server-side Jira adapter using only the confirmed API and field mappings.
- Implement the approved viewer identity/permission propagation and authorization boundary before returning or persisting issue data.
- Handle Jira pagination and complete sprint/issue discovery; validate and map required fields without fabricating missing values.
- Define timeout, rate-limit, retryable/permanent error, and partial-result handling consistent with the approved refresh contract.
- Add adapter contract tests with controlled Jira responses, including malformed/unmapped statuses and inaccessible issues.
- Add pagination/completeness, API throttling, timeout, and transient/permanent failure tests against the confirmed Jira API contract.

**Milestone M2 — Safe and complete Jira read boundary**

- Backend integration tests prove source data is normalized correctly, paginated results are complete, and provider credentials remain server-side.
- Authorization tests show one viewer cannot retrieve another viewer's unauthorized Jira data.
- Jira errors and partial results are surfaced as failures, not success-shaped responses.

### Phase 3 — Persistence and refresh pipeline

**Dependencies**: M2.

**Entry gate**: Resolve the persistence and scheduler decisions in the phase-specific gate table, including the permission-safety of stored Jira data, retention/deletion, and what constitutes a successful complete refresh. Do not persist shared Jira data or enable the scheduled job until these decisions are approved.

**Tasks**

- Implement versioned PostgreSQL migrations for the approved minimum data model: configuration, synchronized sprint/issue data if approved, and refresh status/audit metadata.
- Enforce the approved data-isolation strategy in storage and queries; do not use a shared cache unless its permission-safety is established.
- Implement idempotent synchronization with explicit transaction and completeness semantics so a partial fetch cannot replace a known-good dataset as if it were complete.
- Implement the scheduled refresh at the approved cadence and time zone, independent of dashboard sessions; prevent overlapping jobs and support restart/missed-run recovery as specified.
- Implement user-triggered refresh using the same safeguards and report the last successful refresh accurately.
- Add tests for migrations, idempotency, pagination, partial failures, retries, concurrent triggers, scheduling, recovery, and data retention/deletion rules.
- Ensure a service-account scheduled job does not silently become the authorization source for interactive viewers; test the approved viewer-isolation behavior.

**Milestone M3 — Reliable, permission-safe refresh**

- Scheduled refresh runs independently and satisfies the approved daily cadence.
- Successful, failed, and partial runs are distinguishable; stale data is never labelled current.
- Repeated synchronization does not create duplicates or expose data across users.

### Phase 4 — Dashboard API and calculations

**Dependencies**: M3.

**Entry gate**: Resolve filter combination, metric aggregation, issue inclusion/completion rules, status/blocked-work mapping, and API error/partial-data semantics. Ensure all issue lists, filter choices, and metrics use the same authorized and selected data scope.

**Tasks**

- Add Express read endpoints for dashboard scope, filter choices, sprint summaries, timeline data, issue details, and refresh status as required by the final API contract.
- Validate all request parameters and apply the approved Jira visibility constraints on every relevant request.
- Implement status grouping and count-based completion using the approved issue inclusion and aggregation rules; handle zero-issue and unmapped-status cases explicitly.
- Apply sprint, project, assignee, and issue-type filters consistently to displayed issues and all derived metrics.
- Define stable API response schemas and error responses; document the endpoints for the frontend.
- Add route/service tests for authorization, filters, aggregation, empty results, unavailable fields, and error states.

**Milestone M4 — Verifiable dashboard data contract**

- API responses match the approved schema and selected scope.
- Filtered issue lists and metrics agree with controlled fixtures.
- Completion percentage matches the agreed formula and precision; empty scopes are represented as not applicable.

### Phase 5 — React dashboard experience

**Dependencies**: M4.

**Entry gate**: Resolve timeline behavior, required summary metrics, issue identification/navigation, external-user experience, browser/accessibility targets, and loading/empty/stale/error states. Do not infer the meaning of “full dashboard access” from authorization alone.

**Tasks**

- Implement the dashboard page with sprint summary metrics, timeline, status distribution, completion percentage, and issue details.
- Implement sprint, project, assignee, and issue-type filters using the approved selection and combination rules.
- Trigger refresh on dashboard open and provide the specified manual refresh behavior.
- Implement loading, empty, not-configured, stale-data, partial-refresh, unauthorized, and provider-error states without implying freshness after a failed refresh.
- Ensure authorized external stakeholders receive the agreed experience and data scope.
- Meet the agreed browser, responsive-layout, and accessibility requirements; provide text labels in addition to color-coded status.
- Add component and frontend integration tests for rendering, filtering, refresh behavior, keyboard/accessibility behavior, and error states.

**Milestone M5 — Feature-complete dashboard**

- All in-scope user stories are demonstrable against controlled data.
- Every user-visible metric and filter reflects the same selected data scope.
- No Jira issue mutation or administrative controls are present in the initial read-only product.

### Phase 6 — End-to-end verification and release readiness

**Dependencies**: M5.

**Tasks**

- Run the full frontend/backend test suites, migrations against a clean PostgreSQL 15 instance, production builds, and static checks.
- Run end-to-end tests for all sprint categories and dates, filter combinations, empty sprints, status/field mapping, refresh, and failure recovery.
- Perform authorized integration tests against the confirmed Jira Server/API version and verify historical, active, and future sprint completeness.
- Compare returned sprint and issue counts with a known complete Jira fixture/source of truth, including paginated responses.
- Perform security tests for unauthenticated access, cross-viewer data leakage, external-stakeholder policy, secrets in bundles/logs, input validation, and error disclosure.
- Validate the scheduler while no dashboard user is active and exercise restart, missed-run, duplicate-trigger, Jira outage, and partial-pagination cases.
- Verify configuration governance, operational documentation, environment setup, backup/retention behavior, and deployment connectivity.
- Demonstrate scheduler recovery after downtime and Jira outages, and verify that stale, partial, or unauthorized data cannot be presented as fresh successful data.
- Trace each FR-001–FR-019 and SC-001–SC-009 to implementation evidence and record any approved deferrals.

**Milestone M6 — Release candidate accepted**

- All acceptance tests pass in the approved environment, or each remaining limitation has an explicit owner and approval.
- Access-control tests demonstrate no visibility beyond the approved Jira policy.
- The scheduled refresh, database migrations, deployment configuration, support/maintenance ownership, and recovery procedures are documented and verified.

## Cross-Phase Quality Controls

- Keep Jira API calls and credentials in the Express backend; never place provider credentials in Vite-exposed variables or browser code.
- Use versioned, reviewable database migrations and preserve Jira source identifiers in normalized models.
- Test external-service behavior with controlled responses by default; reserve live Jira tests for the authorized integration environment.
- Treat provider, database, authorization, and partial-refresh errors explicitly. Do not silently substitute empty or stale data as fresh success.
- Keep commits and changes within `jira-dashboard/` unless a separately approved documentation or constitution change is required.
- Do not add Confluence workflows, issue mutations, story-point calculations, or unspecified operational targets as part of this plan.

## Requirement Traceability

| Specification area | Planned phases |
|---|---|
| FR-001–FR-003: application boundaries and server-side integration | 1–2 |
| FR-004–FR-010: sprint/issue data, filters, categories, and metrics | 2, 4–5 |
| FR-011–FR-014: refresh, persistence, and failure behavior | 3–5 |
| FR-015–FR-016: Jira access and external stakeholders | 0, 2–6 |
| FR-017: team-lead ownership and configuration governance | 0, 1, 6 |
| FR-018–FR-019: read-only scope and integration boundaries | 2, 4–6 |
| SC-001–SC-004: sprint completeness, filters, metrics, and issue fields | 2, 4–6 |
| SC-005–SC-007: scheduled/on-open refresh and failure reporting | 3–6 |
| SC-008–SC-009: approved access policy and confirmed Jira deployment | 0, 2, 6 |

## Clarification Review Traceability

| Review findings | Plan treatment |
|---|---|
| C-01–C-04, G-01–G-03 | Resolve access, identity, and external-user data policy at Gate 0; verify per-viewer isolation in Phases 2, 3, and 6. |
| C-05, C-07, G-22 | Confirm Jira-only feature boundary at Gate 0; keep Confluence separate; define per-sprint and multi-sprint calculations before Phase 4. |
| C-06, G-04–G-06 | Resolve blocked/unmapped statuses, sprint scope, issue population, and completion semantics before Jira integration and calculations. |
| G-07–G-09, G-16–G-17 | Resolve filter, metric, timeline, issue navigation, browser, and accessibility behavior before Phase 5. |
| G-10–G-13, G-18–G-19 | Resolve refresh, persistence, data handling, failure, and empty/loading state behavior before Phases 3–5. |
| G-14–G-15 | Resolve configuration governance and toolchain/environment choices in Phases 0–1; verify governance before release. |
| G-20–G-21 | Strengthen fixture completeness, access-control, pagination, scheduler-recovery, and end-to-end tests in Phase 6. |

## Key Risks

- **Permission leakage through shared persistence**: Mitigate by finalizing viewer identity and cache isolation in M0 and testing cross-viewer access before release.
- **Jira Server/API limitations**: Mitigate by confirming exact version and required sprint endpoints before selecting the adapter contract.
- **Daily refresh conflicts with per-viewer permissions**: Resolve the identity/scheduling model together in M0; do not assume one service-account dataset is safe for every user.
- **Incomplete or inconsistent Jira data**: Define paging, status mapping, issue inclusion, and partial-refresh behavior before metrics and persistence are implemented.
- **Unavailable Docker or deployment connectivity**: Verify the engine and network path during M0/M1; do not treat Docker CLI availability alone as proof that PostgreSQL can run.
- **Unbounded initial UI scope**: Keep the first release read-only and limited to the required dashboard, filters, metrics, and issue fields.
