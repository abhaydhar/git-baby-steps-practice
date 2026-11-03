# Jira/Confluence Automation Constitution Design

## Goal

Create a Spec Kit constitution at `spec/constitution.md` for the Jira/Confluence automation project using the user-specified stack: React 18 with Vite, Node.js with Express, and PostgreSQL 15 via Docker.

## Principles

- Treat the named technology versions as binding; record and approve any proposed change before implementation.
- Keep the React client focused on presentation and user interaction. Keep vendor credentials, authorization decisions, and Jira/Confluence API calls in the Express backend.
- Isolate Jira and Confluence integrations behind backend adapters and map provider responses into application-owned models.
- Keep secrets out of source, client bundles, logs, and committed configuration; use least-privilege access and explicit authorization checks.
- Manage PostgreSQL schema changes through reviewable, versioned migrations. Make external synchronization safe to retry and avoid silent data loss.
- Require focused automated tests for behavior, API boundaries, authorization, integrations, and data transformations; validate changes against acceptance criteria.
- Handle provider failures explicitly, apply bounded retries only to transient errors, and log operational events without exposing secrets or sensitive content.
- Use a spec-first workflow: clarify requirements, define acceptance criteria, plan, break work into tasks, implement, and verify. Amend this constitution only through an explicit documented decision.

## Scope

The constitution is project guidance, not an implementation plan. It does not choose deployment hosting, CI provider, authentication protocol, scheduling service, or additional libraries.
