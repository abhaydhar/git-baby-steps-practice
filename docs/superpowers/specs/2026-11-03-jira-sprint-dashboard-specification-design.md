# Jira Sprint Dashboard Specification Design

## Goal

Translate `project_spec.md` and the Module 08 report into a detailed Spec Kit feature specification at `spec/specification.md`. The specification must be implementable and verifiable without silently resolving the source's open requirements.

## Scope and Format

- Describe the Jira sprint dashboard only. The source requirements do not define Confluence automation.
- Use a Spec Kit feature-spec structure: feature metadata, user stories with independent tests, functional requirements, key entities, success criteria, assumptions, dependencies, and open questions.
- Retain the source behaviors: all configured sprints by default, requested filters and issue metadata, count-based completion percentage, three status categories, timeline and metrics, refresh on view/refresh, and an independent daily scheduled refresh.
- Apply `spec/constitution.md`: React 18/Vite frontend, Node.js/Express backend, PostgreSQL 15 via Docker, server-side provider access, explicit failures, and verification.

## Access and Uncertainty

- Preserve Jira-native access controls without inventing a separate application role model. Use per-viewer Jira permission parity as the conservative requirement; validate whether the target Jira Server version and approved authentication support it.
- Require authorized external stakeholders to have the intended dashboard access under the approved Jira policy, without implying access to data they cannot view in Jira.
- Mark the Jira endpoint/version, API and auth method, field mappings, project scope, external-user policy, hosting, and data-retention details as pre-implementation decisions.
- Do not assume story points, add issue editing, or claim unprovided service-level targets.

## Verification

Check that each source acceptance criterion appears as a testable requirement or success criterion, that unresolved dependencies remain explicit, and that no requirement contradicts the constitution or another section.
