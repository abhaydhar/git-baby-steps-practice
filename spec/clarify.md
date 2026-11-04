# Senior Review: Specification Gaps and Clarifications

## Review Summary

The specification defines the Jira Sprint Dashboard's purpose, user stories, principal behaviors, security constraints, and test principles. It is not implementation-ready: authentication and Jira permission preservation are explicitly blocked; external-user policy and the Jira contract remain undecided; and the specification lacks endpoint contracts, screen-level UI behavior, and a concrete persistence model.

This review evaluates [specification.md](./specification.md) against [constitution.md](./constitution.md), and uses [project_spec.md](../project_spec.md) to identify inherited requirement tensions. Priorities indicate implementation risk:

- **P0** — blocks safe access to Jira data or invalidates core product behavior.
- **P1** — must be resolved before implementing the dependent phase.
- **P2** — important for a complete, verifiable release but not an immediate Jira data-access gate.

The specification correctly marks T0.1 as **Blocked**. Recording a blocker is not approval of an identity or authorization design.

## Contradictions and Requirement Tensions

| ID | Priority | Evidence | Finding and clarification needed |
|---|---|---|---|
| C-01 | P0 | `project_spec.md` §2 promises external stakeholders “full dashboard access,” while §8 asks whether they may see summary-only or full Jira issue data. Specification FR-016 and User Story 4 defer access to an unconfirmed policy. | The promise of full access is ambiguous: full feature access, the same configured dashboard data, or full issue details. Define the eligible external population, permissible data, and Jira account/permission prerequisites before enabling external access. |
| C-02 | P0 | Constitution §2 assigns authorization enforcement to the Express backend. Specification FR-015 and Out of Scope prohibit an unapproved application-level authorization model while requiring Jira-native visibility. | These are reconcilable if backend enforcement faithfully applies each viewer's Jira permissions without creating separate app roles. The specification does not yet define the trusted identity flow or how each Jira visibility dimension is applied, so the design remains unimplementable pending T0.1. |
| C-03 | P0 | Specification FR-015 requires per-viewer Jira visibility; FR-012 requires independent scheduled refresh; FR-013 requires PostgreSQL for application data. The access section warns that a shared service account/database must not widen visibility. | A scheduled service-account refresh into shared persistence does not automatically preserve per-viewer Jira permissions. The specification correctly prohibits assuming that it does, but no approved identity/delegation, isolation, or alternative refresh design exists. Demonstrate a compatible design or revise the requirements before implementing Jira access, persistence, or scheduling. |
| C-04 | P1 | `project_spec.md` calculates completion per sprint; FR-009 refers to a “selected sprint scope,” and filters can span projects and sprints. | For multiple selected sprints, the result could be a count-weighted aggregate, an average of sprint percentages, or per-sprint values only. Define the denominator and display behavior for multi-sprint and filtered scopes. |
| C-05 | P1 | User Story 1 mentions blocked work; FR-008 defines only To Do, In Progress, and Done, and calls blocked-work treatment an open decision. | The source promise to show blocked work is not yet resolved by the conditional wording in the story. Decide whether blocked is a distinct category/indicator with an authoritative Jira source and metric treatment, or remove it from this feature's promised outcome. |

## Material Gaps and Unclear Requirements

| ID | Priority | Evidence | Gap / clarification needed |
|---|---|---|---|
| G-01 | P0 | FR-015; T0.1 decision record; User Story 4 | Define dashboard authentication, how the backend obtains and trusts viewer identity, enforcement of project/issue-security/field visibility on every request, unauthorized behavior, and whether confirmed Jira Server/API supports viewer delegation. Record technical validation and explicit Jira- and security-owner approval. Until then, T0.1 and Gate 0 remain blocked. |
| G-02 | P0 | FR-016; SC-008; `project_spec.md` §§2, 8 | Identify eligible external stakeholders; define “full dashboard access”; specify issue-level versus summary visibility and required Jira accounts/permissions. Without this, external-access acceptance tests cannot be defined. |
| G-03 | P0 | FR-001, FR-004; open question 1 | Supply the Jira Server URL, version, supported API, network reachability, and any required plugin/API capabilities. No real integration or live acceptance test can be implemented without this contract. |
| G-04 | P0 | FR-004; Key Entities; open questions 2 and 9 | Define configured projects/boards and sprint discovery, including source fields/API for sprint identity, association, dates, and state. Specify handling of archived, deleted, parallel, cross-project, or removed sprints as applicable. A known-complete source-of-truth fixture is required to verify completeness. |
| G-05 | P0 | FR-008; Key Entities; open question 3 | Define status-to-category mappings, ownership/configuration, and treatment of unmapped statuses in issue display, status distribution, and completion totals. Resolve whether “blocked” is represented by status, field, or another source. |
| G-06 | P0 | FR-009; User Story 1; open question 11 | Define the issue population: parent/sub-task inclusion, issues in multiple sprints, removed issues, and cross-project issues. Define completion (Done category versus resolution), denominator treatment for unmapped statuses, and rounding/precision. |
| G-07 | P1 | FR-003, FR-005, FR-011, FR-014, FR-015, FR-019; phase/API requirements are absent | Specify the Express API contract: endpoint paths and methods; request parameters/body; response schemas for authorized scope, filter choices, sprint summaries/timeline, issue details, and refresh state; error/status responses; pagination; and how trusted viewer identity reaches the API. Current text establishes browser → Express → Jira at a high level but not what data goes where. Do not select a contract that bypasses T0.1 or exposes Jira credentials. |
| G-08 | P1 | FR-005–FR-007, FR-011, FR-014; User Stories 1–3 | Specify the user-visible screen(s) and major regions: dashboard layout, filters, sprint summary/timeline, status/progress, issue list/details, and refresh/status information. Decide whether configuration requires a UI or remains outside the application. Include navigation and responsive behavior once the supported viewport/browser scope is set. |
| G-09 | P1 | FR-013; Key Entities; open question 8 | The key entities are conceptual, not a database model. Decide what PostgreSQL actually stores and document entities/tables, fields, source identifiers, relationships/keys, permission partitioning, refresh metadata, and indexes/constraints as needed. Define retention, cleanup when scope/access changes, and whether Jira issues/sprints are cached. Keep the model behind the permission-safe persistence gate. |
| G-10 | P1 | FR-006; User Story 1; open question 13 | “Sprint summary metrics” is not enumerated beyond completion percentage and status distribution. List each additional metric with formula, aggregation level, filters, and zero/empty behavior, or explicitly limit the requirement to the metrics already defined. |
| G-11 | P1 | FR-006; open question 9 | Define timeline date sources, range, ordering, overlap, state representation, timezone, selection interaction, and handling of missing/invalid dates. |
| G-12 | P1 | FR-005; User Story 2; SC-002; open question 10 | Define single/multi-select cardinality, AND/OR combination, reset behavior, unassigned/empty options, and whether options come from full authorized scope or current results. Specify that issue lists and all derived metrics use consistent filter scope. |
| G-13 | P0 | FR-011–FR-014; SC-005–SC-007; User Story 3 | Define initial-load and manual-refresh behavior: when data is considered loaded, whether cached data can display during refresh, how stale data is labelled or hidden, last successful refresh, and user-visible outcomes for failure/partial completion. |
| G-14 | P1 | FR-012; SC-005; T0.1 | Define schedule time zone/window, attempt versus successful complete refresh, retry/backoff, missed-run recovery, outage behavior, overlap/concurrency policy, and operation during downtime. Ensure scheduled identity is compatible with the approved viewer-permission model. |
| G-15 | P1 | FR-014, FR-019; Quality and Verification | Define pagination termination/completeness, provider rate-limit handling, timeout limits, retryable versus permanent errors, and what constitutes partial success across projects/sprints. Current text requires explicit failure and completeness checks but does not state these operational rules. |
| G-16 | P1 | FR-007; open question 14; User Stories 1–2 | An issue is difficult to identify with only status, assignee, due date, and priority. Define required issue key/title/link, sorting/grouping, large-result handling (pagination/virtualization), and whether links may navigate to Jira under the viewer's permissions. |
| G-17 | P1 | FR-017; User Story 4; open question 6 | Define “dashboard configuration,” who may propose/approve changes, where configuration lives, and the Jira governance evidence required. Decide whether changes use an in-app UI or a reviewed file/operational process; do not imply an unapproved application role. |
| G-18 | P1 | FR-002; Constitution §1; open question 1/plan bootstrap gate | The constitution fixes React/React DOM 18 and PostgreSQL 15, and delegates exact Node.js, Express, Vite, Docker Engine/Compose versions to T1.1. The specification names some technologies but not exact versions or deployment scope for Docker. Record the approved exact versions and supported environments in the toolchain decision before bootstrap; this is a deliberate pending decision, not a reason to guess versions here. |
| G-19 | P1 | FR-016; Access, Security, and Data Handling; FR-013 | Define which Jira fields may be displayed, persisted, and logged; sensitive-data restrictions; data minimization; and deletion/revocation behavior. Jira permission parity alone does not establish approval to copy every visible field into a separate database. |
| G-20 | P1 | FR-006–FR-007, FR-014; User Stories 1–3 | Specify first-run/not-configured, loading, no-data, inaccessible project, no-filter-results, stale, partial-refresh, unauthorized, and provider/database-error screen states. Existing requirements cover some empty and failed-refresh cases but not the complete UX contract. |
| G-21 | P2 | No corresponding measurable requirements; open question 15 | Define supported browsers/viewports and accessibility expectations for keyboard use, screen readers, focus, timeline/chart alternatives, and non-color status cues, or explicitly defer them. |
| G-22 | P2 | SC-001; Quality and Verification | SC-001 now correctly requires a known source-of-truth sprint set, but the fixture/source, its provenance, and expected historical/active/future counts are not identified. Provide a controlled, representative fixture and expected values; keep live Jira checks authorized and separate. |
| G-23 | P2 | Quality and Verification; SC-008–SC-009; FR-017 | Acceptance criteria require access, integration, and release evidence, but do not specify where the requirement-to-test/approved-deferral matrix is maintained or who signs it. Define an evidence artifact and owners before release acceptance. |

## Constitution Alignment

- **Aligned:** The feature remains a separate React/Vite + Express application; provider calls stay server-side; Jira integrations are isolated; PostgreSQL migrations, explicit failure handling, and verification are required. The specification clearly excludes Confluence for this feature, matching the constitution's separate-spec requirement.
- **No direct stack contradiction found:** React 18 and PostgreSQL 15 match the constitution. Exact Node.js, Express, Vite, and Docker versions are intentionally assigned to T1.1 by the constitution, so they remain a bootstrap decision rather than an invented requirement.
- **Security is a blocker, not an approved design:** FR-015 and the T0.1 record state the needed outcome but do not yet demonstrate how Jira visibility will be preserved. No Jira authorization/data implementation is safe until T0.1 is resolved.

## Items Addressed Since the Previous Review

- The Jira-dashboard-only boundary and separate Confluence specification are now explicit; the earlier scope ambiguity is resolved.
- Sprint completeness is now checked against a known source of truth, and the quality section explicitly calls for pagination/completeness, cross-viewer, and scheduler tests. These are improvements, though the actual fixture and evidence artifacts remain open (G-22/G-23).
- The blocked-work phrase is now conditional and FR-008 marks its treatment as open; a product decision is still required (C-05/G-05).
- The T0.1 identity decision is explicitly recorded as blocked; this makes the gate visible but does not resolve it.

## Recommended Clarification Order

1. Resolve T0.1 identity, viewer permission enforcement, and scheduled-refresh compatibility with Jira and security owners.
2. Resolve external-user eligibility and data policy.
3. Confirm Jira Server/API, network path, project/board scope, fields, sprint discovery, and a complete controlled fixture.
4. Finalize status, blocked-work, issue-population, completion, and multi-sprint metric semantics.
5. Approve refresh, persistence, isolation, retention, and deletion policy before storing Jira data or enabling scheduled synchronization.
6. Define API contracts, screen behavior, filters, metrics, timeline, and issue presentation before implementing their dependent API/UI work.
7. Record toolchain versions, configuration governance, accessibility/browser targets, and release evidence artifacts.

## Source Wording Note

The source acceptance criterion “The dashboard displays issued completion percentage” appears to contain a typo; the specification interprets it as “issue completion percentage.” Confirm only if the source author intended a different metric.
