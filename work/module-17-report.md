# Module 17 Completion Report

## Specification Contents
# Feature Specification: Jira Sprint Dashboard

- **Feature Branch**: Not assigned (specification only)
- **Created**: 2026-11-03
- **Updated**: 2026-11-04
- **Status**: Draft — pre-implementation decisions remain
- **Input**: `project_spec.md` and the Module 08 requirements report

## Full Product Vision

The eventual product is a separate, read-only web application for team members, project stakeholders, and organization-authorized external stakeholders to review Jira sprint progress and delivery status. The full product is intended to include all sprints in the approved project scope by default, required filters, issue-count progress and available issue details, and refreshed Jira data on dashboard use as well as through an independent daily schedule.

This specification covers only the Jira sprint dashboard described in `project_spec.md`; it does not define Confluence automation. The full product remains not implementation-ready until its blocking access, Jira contract, and metric decisions are resolved or explicitly accepted out of scope.

### Prototype Scope Baseline

The approved prototype is narrower than the full product vision. The **Prototype Scope Decisions** below are authoritative for prototype work and take precedence over broader future-product language in the user stories, functional requirements, quality requirements, success criteria, assumptions, and open questions. Those broader sections describe the future product; they do not authorize prototype implementation of excluded capabilities.

For this prototype, use invented local mock data only. Do not connect to Jira or an identity provider, access real user data, serve dashboard data through an API, persist Jira-like records, or imply that mock data is current. The only approved fixture behavior is the status mapping described in G-05; no issue-level or aggregate display is approved by this baseline. G-01 remains an explicit blocker for any future real Jira access, and no Jira-owner or security-owner approval is implied.

Decisions confirmed only for the prototype are listed in G-01 through G-14. Findings G-15 through G-23 and other unanswered production questions remain unresolved or deferred as stated; this baseline does not decide them or convert them into approved out-of-scope product policy.

## Prototype Scope Decisions

The following decisions were confirmed by the product owner during the clarification review. They limit the prototype only; they do not remove the corresponding capabilities from the future product vision unless explicitly stated.

| Review item | Confirmed prototype decision |
|---|---|
| G-01 — Identity and Jira permission enforcement | Use controlled mock Jira fixtures only. Do not implement live Jira access, real user-data access, or an identity/authorization model. T0.1 remains blocked; no Jira or security-owner approval is implied. |
| G-02 — External stakeholders | Real external-user access is out of scope. No external-user population or issue-visibility permission is approved. |
| G-03 — Jira Server/API contract | Live Jira integration is out of scope; the prototype must not connect to a real Jira instance. |
| G-04 — Project, board, and sprint discovery | Live scope discovery and source-of-truth completeness acceptance are out of scope. Synthetic sample data may be used, but no representative fixture contents have been approved. |
| G-05 — Status mapping | For fixture data, map statuses directly to To Do, In Progress, or Done. Never treat an unmapped status as Done. Do not represent blocked as a separate category unless it is explicitly present in fixture data. |
| G-06 — Issue population and completion semantics | Completion-metric edge cases are deferred. A completion percentage is not a prototype acceptance behavior; the simple formula remains a future requirement unless its scope is later defined. |
| G-07 — API contract | API-backed dashboard data flow is out of scope. Do not implement Jira or identity API endpoints; any prototype data must be local mock data. |
| G-08 — Screen-level UI requirements | Screen/layout acceptance criteria are out of scope. This does not approve a production dashboard design. |
| G-09 — PostgreSQL data model and retention | Do not persist Jira sprint or issue records. PostgreSQL 15 remains binding for any application data that is in scope, in accordance with the constitution. |
| G-10 — Additional summary metrics | No additional sprint-summary metrics are required for the prototype. This does not restore the deferred completion percentage. |
| G-11 — Sprint timeline | Timeline display and behavior are out of scope. |
| G-12 — Interactive filters | Interactive sprint, project, assignee, and issue-type filters are out of scope for the prototype. |
| G-13 — Initial load and manual refresh | Refresh behavior is out of scope: no refresh controls, live refresh, or claim that prototype data is current. |
| G-14 — Scheduled refresh | Scheduled refresh is out of scope. FR-012 and SC-005 are deferred, not satisfied by the prototype. |

These decisions do not resolve the remaining findings in `spec/clarify.md`. In particular, issue identification/presentation, configuration governance, the exact toolchain versions, accessibility/browser targets, release-evidence ownership, and production Jira integration remain undecided or deferred. Do not infer approval for those items from this prototype scope record.

## Scope and Constraints

- The application is a separate web application under `jira-dashboard/`; it must not be mixed into the repository's Python calculator.
- The prototype is mock-only and must not access, expose, or persist real Jira data.
- Prototype data is local and synthetic; it is not served through a dashboard API and must not be represented as current Jira data.
- Prototype exclusions and future product requirements are distinguished in the decision record above. A deferred requirement is not an accepted implementation or acceptance criterion for this prototype.
- The initial product is read-only with respect to Jira issues. It does not create, edit, transition, or administer Jira issues.
- For the future product, the application reads Jira data through the confirmed Jira Server API; Jira calls and privileged credentials remain on the Express backend. This is not a prototype data flow.
- “All sprints” means the complete set discoverable through the confirmed API for the approved project/board scope, including historical, active, and future sprints, verified against a known source of truth. It does not mean every sprint on the Jira instance.
- Confluence automation is a separate feature and requires its own specification and plan.
- Decisions not supplied by the source requirements are recorded as open questions; this document does not approve an identity provider, Jira endpoint, project scope, or external data-sharing policy.

## Future Product User Scenarios & Testing

The following user stories and scenarios describe the future product vision. They are not prototype acceptance criteria where they conflict with the Prototype Scope Baseline or the G-01 through G-14 decisions.

### User Story 1 — Review sprint progress (Priority: P1)

As a team member or project stakeholder, I want to review sprint timelines, defined summary metrics, status distribution, and issue progress so that I can understand what is planned, in progress, complete, and (if approved and defined) blocked.

**Why P1**: A useful view of delivery progress is the dashboard's primary purpose.

**Independent test**: Use a controlled Jira fixture with a known-complete set of configured past, active, and future sprints and issues in each approved status category. Open the dashboard without filters and compare the displayed sprints, summaries, timeline, status distribution, issue-count completion percentage, and available issue details with the fixture's source-of-truth values.

**Acceptance scenarios**:

1. **Given** configured Jira projects contain historical, current, and future sprints, **When** an authorized user opens the dashboard with no filters, **Then** the complete sprint set in the approved scope is represented and its count matches the known source of truth.
2. **Given** a sprint has issues in To Do, In Progress, and Done categories, **When** its progress is displayed, **Then** the dashboard shows those categories, their distribution, and completion percentage using the defined issue-count formula.
3. **Given** issue status, assignee, due date, and priority are available from Jira, **When** an issue is displayed, **Then** those fields are shown. **If** a field is unavailable, the dashboard does not invent a value.
4. **Given** a sprint has no issues, **When** its completion percentage is displayed, **Then** the dashboard shows that the percentage is not applicable rather than dividing by zero.

### User Story 2 — Filter the dashboard (Priority: P1)

As a dashboard user, I want to filter sprint data by sprint, project, assignee, and issue type so that I can focus on the work relevant to my review.

**Why P1**: These four dimensions are explicit dashboard requirements and are needed to navigate across all displayed sprints.

**Independent test**: Use a known fixture with distinguishable values for all four dimensions. Apply each filter independently and verify that displayed issues, status distribution, and completion values correspond to the selected scope. Filter combinations and option-population behavior remain subject to the decisions in the open questions.

**Acceptance scenarios**:

1. **Given** the dashboard is loaded, **When** a user filters by sprint, project, assignee, or issue type, **Then** the displayed data is scoped by that filter.
2. **Given** a filter selection matches no issues, **When** the dashboard updates, **Then** it shows an explicit empty result and does not present unrelated issues or misleading completion totals.
3. **Given** filter values are available from the configured Jira data, **When** a user opens a filter, **Then** the available values are presented without requiring the user to enter Jira field identifiers.

### User Story 3 — See refreshed Jira data (Priority: P1)

As a dashboard user, I want data refreshed when I open or refresh the view, and on a scheduled basis, so that the dashboard is not dependent on manual maintenance.

**Why P1**: Both view-triggered and independent daily refresh are explicit requirements.

**Independent test**: With a controllable Jira API test double and scheduler, verify that opening or manually refreshing the dashboard causes a backend refresh request, and that the scheduled process initiates refresh at least once per 24-hour period without a dashboard user session. Verify that success, failure, and partial completion are distinguishable and that stale data is never represented as fresh.

**Acceptance scenarios**:

1. **Given** Jira is reachable, **When** an authorized user opens the dashboard or requests a refresh, **Then** the application requests current data through the backend integration.
2. **Given** no user opens the dashboard, **When** the daily scheduled time arrives, **Then** the backend initiates a Jira data refresh independently.
3. **Given** Jira returns an error or the refresh is incomplete, **When** the dashboard attempts to refresh, **Then** the failure is surfaced and is not reported as a successful refresh.
4. **Given** previously synchronized data is shown after a refresh failure, **When** the dashboard renders it, **Then** the data is not represented as newly refreshed.

### User Story 4 — Access and maintain the dashboard (Priority: P1)

As a team lead, I want dashboard configuration to follow the team's Jira governance process and the dashboard to respect Jira access controls so that stakeholders can use it without bypassing the source system's permissions.

**Why P1**: The requirements make Jira-native visibility and team-lead ownership part of the acceptance criteria.

**Independent test**: Verify that an authorized team member and an authorized external stakeholder can use the dashboard, that access to Jira data does not exceed the approved Jira visibility policy, and that configuration changes can be reviewed through the established governance process.

**Acceptance scenarios**:

1. **Given** a user is authorized under the approved Jira access policy, **When** that user opens the dashboard, **Then** the dashboard is available without introducing a separate application role model.
2. **Given** a user is not permitted to view Jira data under the approved access policy, **When** that user requests the dashboard data, **Then** the application does not expose that data.
3. **Given** an external stakeholder has been authorized under the organization's policy, **When** they use the dashboard, **Then** they can use the dashboard as required by that policy.
4. **Given** the team lead changes dashboard configuration, **When** the change is proposed, **Then** it can be reviewed through the team's normal Jira governance process.

## Future Product Requirements

The functional requirements and success criteria below describe the future product. For the prototype, apply the Prototype Scope Baseline and the implementation scope in `spec/plan.md`; deferred requirements must not be reported as satisfied.

### Functional Requirements

- **FR-001**: The product MUST be a separate web application that retrieves Jira data through the configured Jira Server API. It MUST NOT be mixed into the existing Python calculator project.
- **FR-002**: The frontend MUST use React 18 and Vite. The backend MUST use Node.js and Express. PostgreSQL 15 MUST be used through Docker, in accordance with the project constitution.
- **FR-003**: The browser MUST communicate with the Express backend for Jira data. Jira credentials and privileged provider calls MUST remain server-side.
- **FR-004**: The dashboard MUST display all sprints discoverable in the confirmed Jira project/board scope by default, including historical, active, and future sprints. The integration's completeness must be verified against a known source of truth; an incomplete API response must not be treated as the complete sprint set.
- **FR-005**: The dashboard MUST provide filters for sprint, project, assignee, and issue type.
- **FR-006**: The dashboard MUST provide a sprint timeline, issue completion percentage, status distribution, and the four required filters. Any additional “sprint summary metrics” must be enumerated with formulas and empty-data behavior before implementation; unlisted metrics must not be inferred.
- **FR-007**: For each issue, the dashboard MUST display Jira status, assignee, due date, and priority when the corresponding data is available. It MUST NOT fabricate missing field values.
- **FR-008**: The initial progress categories MUST be To Do, In Progress, and Done. Jira statuses MUST be mapped to these categories using confirmed configuration; unsupported or unmapped statuses MUST NOT be silently classified as Done. Whether “blocked” work is a separate category, a Jira field, or out of scope remains an explicit decision.
- **FR-009**: Completion percentage MUST be calculated as `(completed issues / total issues in the selected sprint scope) * 100`. The calculation MUST use issue counts, not story points. If the denominator is zero, the percentage MUST be presented as not applicable.
- **FR-010**: Story points MUST NOT be assumed or included in progress calculations unless a supported Jira field and an explicit product decision enable a separate story-point feature.
- **FR-011**: Opening the dashboard view and requesting a user-initiated refresh MUST cause the application to request current Jira data through the backend. The user-visible loading and cached/stale-data behavior must follow the approved refresh contract.
- **FR-012**: The backend MUST run a scheduled Jira data refresh at least once per 24-hour period. This schedule MUST operate independently of users opening or refreshing the dashboard.
- **FR-013**: The application MUST use PostgreSQL 15 for application data required by the dashboard and refresh process. Schema changes MUST be managed by reviewable, versioned migrations. The exact persisted fields and retention policy are open decisions.
- **FR-014**: Jira and database failures MUST be surfaced explicitly. A failed or partial refresh MUST NOT be reported as successful, and previously synchronized data MUST NOT be presented as current when its refresh failed.
- **FR-015**: The application MUST authenticate users and use an integration method approved for the confirmed Jira Server version. The backend MUST enforce the approved access policy and preserve Jira-native visibility without introducing an unapproved application-level role model or exposing data beyond the viewer's approved Jira visibility. The method for establishing trusted viewer identity and applying project, issue-security, and relevant field visibility is blocked pending T0.1.
- **FR-016**: Authorized external stakeholders MUST be able to access the dashboard according to the approved organization policy. The exact external-user population and whether issue-level data or only summary data is permitted MUST be confirmed before implementation.
- **FR-017**: A team lead MUST own dashboard maintenance and configuration. Configuration changes MUST be reviewable through the team's normal Jira governance process.
- **FR-018**: The initial product MUST be read-only with respect to Jira issues. It MUST NOT create, edit, transition, or administer Jira issues.
- **FR-019**: Jira-specific integrations MUST be isolated behind backend service or adapter boundaries, and provider responses MUST be mapped into application-owned data structures before being consumed by the rest of the application.

### Key Entities

- **Configured Jira scope**: The confirmed Jira Server instance and set of projects included in the dashboard. The endpoint, project selection, and configuration ownership must be supplied.
- **Sprint**: A sprint returned by Jira, including its source identifier and the confirmed values needed for its name, project association, timeline, and state. Exact Jira field mappings must be confirmed.
- **Issue**: A Jira issue in the configured sprint/project scope. The dashboard needs the source identity and available status, assignee, due date, priority, issue type, project, and sprint data.
- **Status category mapping**: The approved mapping from Jira statuses to To Do, In Progress, and Done. It must be confirmed against the target Jira workflow.
- **Refresh result**: The outcome and time of a scheduled or user-triggered data refresh, sufficient to distinguish a successful refresh from a failed or partial one.
- **Dashboard filter selection**: The selected sprint, project, assignee, and issue type values used to scope the displayed issue set and derived metrics.

### Access, Security, and Data Handling

- Jira API credentials MUST NOT be exposed in the browser, source control, or logs.
- Authentication MUST use an organization-approved identity with only the permissions required for the selected integration model.
- The target access model MUST preserve Jira-native visibility. In particular, a backend service account and a shared database MUST NOT become a path for one dashboard viewer to see issues that viewer cannot access under the approved Jira policy.
- The proposed SSO/service-account approach is not approved by this specification; it requires validation against the confirmed Jira Server version and the per-viewer access requirement. Authentication to the dashboard, trusted identity propagation, Jira permission enforcement, and scheduled-refresh compatibility remain blocked under T0.1.
- External access is not granted by this specification alone. The permitted external population, data fields, issue-level visibility, and any Jira account/permission prerequisites must be approved before exposing dashboard data.
- Data persisted in PostgreSQL, if any, must follow an approved data-minimization, access-isolation, retention, and deletion policy. A shared synchronized dataset must not widen a viewer's Jira visibility.
- Error messages and operational logs MUST avoid disclosing credentials, tokens, or sensitive Jira content.
- Synchronization MUST be safe to retry without creating duplicate side effects. The initial dashboard is read-only, so synchronization MUST NOT modify Jira issues.

### T0.1 Decision Record — Blocked

**Status**: No identity or Jira permission model has been approved. The SSO/service-account proposal remains unvalidated, and Jira Server and identity-provider details are not yet confirmed. Do not implement authorization, retrieve or persist Jira data, or expose Jira data through the dashboard until this decision is approved.

The approved model must document:

- How users authenticate to the dashboard and how the backend obtains and trusts each viewer's identity.
- How project, issue-security, and relevant field visibility are enforced for every data request, and how unauthenticated or unauthorized requests are denied.
- Whether the confirmed Jira Server/API supports viewer-identity delegation and, if so, how delegation is performed and verified.
- How scheduled refresh works without allowing a shared service-account dataset to expose data beyond each viewer's Jira permissions. If this cannot be demonstrated, stop and revise the authentication, persistence, or product design before implementation.

**Unblocking evidence**: Record the confirmed Jira Server/API and identity-provider capabilities, the selected and validated access/scheduled-refresh design, and explicit approval from both the security owner and Jira owner. Until that evidence is recorded, T0.1 remains blocked; this record is not an approval.

### Quality and Verification

- Acceptance scenarios MUST be verified with automated tests using controlled Jira API responses; routine tests MUST NOT depend on a live Jira instance.
- Tests MUST cover status mapping, filter scoping and combinations once defined, completion calculation, unavailable fields, empty sprints, successful refresh, failed/partial refresh, and access-policy behavior.
- Jira adapter tests MUST verify pagination and completeness against a known complete fixture or source-of-truth count, as well as provider error and partial-result handling.
- Access tests MUST include at least two viewer permission levels and demonstrate that data visible to one viewer is not returned to a viewer lacking that Jira visibility. External-user tests must use the approved external-user policy.
- Scheduler tests MUST verify independent operation, failure/recovery behavior, and truthful refresh status against the approved schedule contract.
- Integration tests MUST verify the backend's Jira API boundary and PostgreSQL persistence/migrations. Live Jira tests require an authorized non-production environment.
- Release evidence MUST map every in-scope functional requirement and success criterion to a repeatable test or an explicitly approved deferral.
- The project MUST not claim a response-time, throughput, availability, or data-retention target that has not been agreed and documented.

## Success Criteria

- **SC-001**: With a configured Jira test dataset and known complete source-of-truth sprint set, 100% of configured historical, active, and future sprints in scope appear in the unfiltered dashboard; the count matches the source of truth.
- **SC-002**: Each of the four required filters can be applied independently, and the resulting issue set and metrics match the filtered test dataset.
- **SC-003**: For any non-empty test scope, the displayed completion percentage equals completed issue count divided by total issue count multiplied by 100; for an empty scope it is not applicable.
- **SC-004**: Every available required issue field (status, assignee, due date, priority) is displayed, and unavailable values are not invented.
- **SC-005**: The refresh scheduler initiates at least one refresh in every 24-hour period without requiring a dashboard session.
- **SC-006**: Opening the view and requesting a refresh each initiate a backend refresh request.
- **SC-007**: Failed or partial provider refreshes are observably unsuccessful and are never represented as fresh successful data.
- **SC-008**: Access tests demonstrate that the dashboard does not expose Jira data outside the approved visibility policy, including cross-viewer checks, and that authorized team members and external stakeholders can use it according to the approved policy.
- **SC-009**: An authorized integration test in the approved environment connects to the confirmed Jira Server endpoint and supported API version and retrieves the configured scope according to the approved contract.

## Assumptions

- The source of truth is the Jira Sprint Dashboard specification in `project_spec.md`, reproduced in `work/module-08-report.md`.
- The application reads Jira data and displays it; issue editing and full Jira administration are out of scope.
- “All sprints” means all sprints discoverable through the confirmed API for the approved project/board scope, verified against a known complete source of truth; it does not mean every project or sprint on the Jira instance.
- The count-based completion formula is authoritative; story points do not change it.
- A dashboard view refresh and the independent scheduled refresh are both required.
- Jira-native visibility is required. Per-viewer Jira permission parity is the conservative interpretation until the authentication and integration design is confirmed.
- The project constitution governs the technology stack and security, data-integrity, and testing principles.

## Out of Scope

- Confluence automation or Confluence data.
- Creating, editing, transitioning, or administering Jira issues.
- A custom Jira status taxonomy beyond To Do, In Progress, and Done.
- Story-point reporting or story-point-based completion calculations by default.
- A separate application-level role or authorization system.
- Unspecified deployment, hosting, identity-provider, or performance targets.

## Dependencies and Open Questions

The following decisions MUST be resolved before implementation begins:

1. What is the Jira Server base URL, version, supported API version, and required network path from the development and deployment environments?
2. Which Jira projects are in scope, and which sprint, project, issue type, status, assignee, due-date, and priority fields are authoritative?
3. How are Jira workflow statuses mapped to To Do, In Progress, and Done? Is blocked work a distinct category or indicator? How should unmapped statuses be handled in category metrics?
4. Which approved authentication method supports the required Jira-native, per-viewer visibility? Is the proposed SSO/service-account approach compatible, or must the integration use viewer identity/delegation? T0.1 is blocked until this is validated and approved as recorded above.
5. What exact policy applies to external stakeholders, including whether they may see issue-level data or only dashboard summaries?
6. Who is the responsible team lead, what does dashboard configuration include, and which Jira governance workflow reviews those changes?
7. Where will the application and its daily scheduler be hosted, and how will that environment reach Jira Server and PostgreSQL?
8. What database retention and synchronization completeness policy is required?
9. What Jira fields provide sprint start/end dates and state for the timeline, and what timezone should the timeline use?
10. Are filter selections single-value or multi-value, and how should multiple filter dimensions combine?
11. Are sub-tasks included in the issue-count denominator, and what is the exact definition of a “completed issue” beyond the configured Done category?
12. Is story-point reporting required in a later scope, and if so, which supported Jira field should it use?
13. Which sprint summary metrics, beyond completion percentage and status distribution, are required? If none are required, may “summary metrics” be limited to those explicitly listed?
14. What issue identifier/title/link, sort order, and large-result behavior are required for users to identify and navigate displayed issues?
15. Which browsers, viewport sizes, and accessibility expectations are required for acceptance?

## Constitution Alignment

This feature specification follows `spec/constitution.md`: React 18/Vite, Node.js/Express, PostgreSQL 15 via Docker, server-side provider integration, explicit failure handling, versioned database migrations, testable acceptance criteria, and spec-driven implementation. Any change to these constraints requires an explicit constitution amendment.

## Commit History
f5606f4 feat: complete prototype per specification.
b3e3fcb .
7fb5669 .
c298717 .
1ea8b5d docs: design Jira dashboard implementation plan
b2f5fa6 .
657b8c7 docs: design Jira dashboard specification
6f550fb docs: design Jira/Confluence constitution
e12906a chore: project skeleton for prototype
27a017a docs: specify Jira dashboard skeleton
e9e0f0e docs: specify Express environment test
9831966 .
617e278 docs: specify batch document workflows
e390774 .
e846734 commit
adb1901 .
3c9b7c8 .
aeeb5fc a
1ec1697 b
7f07602 d
8d07970 d
9578162 commiye
2fea62c state jira workflow
d68e1c4 commit instructions
b4edaf6 s
ac17cb6 .
37ad522 s
429b829 commit
dd87bf2 third commit
78f8a79 second commit
c2ed77e first commit

## Commit Count
31

## Project Files
.github/copilot-instructions.md
.gitignore
.mcp.json
AGENTS.md
README.md
backlog.md
calculator.py
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-27e1ec7b-9c9f-4f07-8cfd-94ea9ede2bce.json
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-5015a557-21c8-4bc2-8d13-349a51cc02e9.json
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-61fbfeb5-c3aa-42d9-9f20-5bcedc36b3ca.json
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-905279c3-b8a5-4918-826f-83ef14b5408c.json
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-d70f8ae1-bc3a-457f-9539-1b84df25ee46.json
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-db9de20b-5640-45da-9df5-af72a3cd116f.json
docs/codemie/analytics/codemie-analytics-abhay-dhar-epam-com-ea8b8fb6-1043-4a9d-8f62-0b313cad9f32.json
docs/superpowers/specs/2026-11-02-batch-document-workflows-design.md
docs/superpowers/specs/2026-11-02-express-env-test-design.md
docs/superpowers/specs/2026-11-03-jira-confluence-constitution-design.md
docs/superpowers/specs/2026-11-03-jira-dashboard-implementation-plan-design.md
docs/superpowers/specs/2026-11-03-jira-dashboard-skeleton-design.md
docs/superpowers/specs/2026-11-03-jira-sprint-dashboard-specification-design.md
instructions/calculate-compound-interest.agent.md
instructions/calculate-sprint-velocity-ins.agent.md
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/main.agent.md
instructions/update-stale-open-tickets.agent.md
instructions/validate-instructions.agent.md
instructions/write-tests.agent.md
jira-dashboard/.env.example
jira-dashboard/.gitignore
jira-dashboard/README.md
jira-dashboard/backend/.nvmrc
jira-dashboard/backend/README.md
jira-dashboard/backend/package-lock.json
jira-dashboard/backend/package.json
jira-dashboard/backend/src/jobs/.gitkeep
jira-dashboard/backend/src/middleware/.gitkeep
jira-dashboard/backend/src/routes/.gitkeep
jira-dashboard/backend/src/server.js
jira-dashboard/backend/src/services/.gitkeep
jira-dashboard/backend/tests/.gitkeep
jira-dashboard/backend/tests/server.test.js
jira-dashboard/compose.yaml
jira-dashboard/docs/.gitkeep
jira-dashboard/frontend/.nvmrc
jira-dashboard/frontend/README.md
jira-dashboard/frontend/index.html
jira-dashboard/frontend/package-lock.json
jira-dashboard/frontend/package.json
jira-dashboard/frontend/public/.gitkeep
jira-dashboard/frontend/src/App.css
jira-dashboard/frontend/src/App.jsx
jira-dashboard/frontend/src/components/.gitkeep
jira-dashboard/frontend/src/features/.gitkeep
jira-dashboard/frontend/src/main.jsx
jira-dashboard/frontend/src/services/.gitkeep
main.py
project_spec.md
reports/action-items.md
reports/example.md
reports/instruction-srp-audit.md
reports/instructions.md
reports/markdown-validation.md
reports/template.md
spec/analyze.md
spec/checklist.md
spec/clarify.md
spec/constitution.md
spec/plan.md
spec/specification.md
spec/tasks.md
tests/test_document_tools.py
tools/compound_interest.py
tools/extract_action_items.py
tools/sprint-velocity.py
tools/validate_markdown.py
weekly-status-report.md
work/jira-dashboard-requirements.md
work/module-03-report.md
work/module-08-report.md
work/module-09-report.md
work/module-10-report.md
work/module-12-report.md
work/module-13-report.md
work/module-14-report.md
work/module-15-report.md
work/module-16-report.md
