# Jira/Confluence Automation Constitution

This constitution defines the non-negotiable principles for the Jira/Confluence automation project. Product specifications and implementation plans must comply with it. A proposed exception requires an explicit, documented amendment before implementation.

## Project Context

### Project Purpose and Users

- The initial product defined by `spec/specification.md` is the **Jira Sprint Dashboard**: a separate, read-only web application for reviewing sprint progress, delivery status, and issue details available under the approved Jira visibility policy.
- Its intended users are team members, project stakeholders, and external stakeholders authorized under the organization's approved policy. This audience statement does not itself grant access or resolve the external-user data policy.
- Confluence automation is part of the broader project context but is not included in the Jira Sprint Dashboard feature. It requires its own approved specification and plan.

### Application Structure

- Keep the dashboard isolated under `jira-dashboard/`; do not mix it into the root Python calculator.
- Use the following layout as the default organization. Add folders only when an approved feature needs them.

```text
jira-dashboard/
  frontend/
    public/
    src/
      components/     # Shared presentation components
      features/       # Feature-specific UI and state
      services/       # Backend API clients; no privileged Jira calls
  backend/
    src/
      jobs/           # Scheduled and background work
      middleware/     # Shared request processing and policy enforcement
      routes/         # HTTP route definitions and input validation
      services/       # Domain services and provider adapters
    migrations/       # Versioned database migrations
    tests/            # Backend unit, integration, and contract tests
  docs/               # Dashboard setup and technical documentation
```

- Keep frontend and backend manifests, lockfiles, and runtime configuration in their respective application roots. Keep secrets out of source control; `.env.example` contains names and safe placeholders only.
- Frontend feature code belongs in `src/features`; reusable UI belongs in `src/components`; browser-side services communicate only with the Express API.
- Backend routes delegate business and provider work to `src/services`. Jira-specific code stays behind a backend service/adapter boundary. Background jobs belong in `src/jobs`, and migrations must be versioned under `backend/migrations`.
- Place tests beside their owning project and organize them by the behavior or module under test. Tests for Jira behavior use controlled responses unless an authorized live integration test is explicitly required.

### Coding and Naming Standards

- Use `camelCase` for JavaScript variables and functions, `PascalCase` for React components and classes, and `useCamelCase` names for React hooks.
- Name React component files with `PascalCase.jsx`; name frontend hooks and JavaScript helpers/services with `camelCase.js`. Name backend route, middleware, service, job, and test files with descriptive `kebab-case.js` names; test files use the `.test.js` suffix.
- Keep each module focused on one feature or responsibility. Prefer feature-local UI/state over putting feature-specific code in shared component folders.
- Keep HTTP concerns in routes, shared request concerns in middleware, domain/provider behavior in services, and scheduled work in jobs. Do not duplicate provider-specific response parsing across routes or UI components.
- Follow the repository's configured formatter and linter once established. T1.1/T1.3 must select and document those tools; do not introduce conflicting formatting conventions in individual modules.

## Core Principles

### 1. The Approved Technology Stack Is Binding

- The frontend MUST use React 18 and Vite.
- The backend MUST use Node.js and Express.
- PostgreSQL 15 MUST be the relational database and MUST be run through Docker as specified by the project.
- React and React DOM MUST remain on major version 18; PostgreSQL MUST remain on major version 15. T1.1 MUST select compatible, supported Node.js, Express, Vite, Docker Engine, and Docker Compose versions before bootstrap. Record exact runtime/tool versions and pin application dependencies through manifests, lockfiles, and documented runtime configuration; do not treat an unselected version as approved.
- A change to a required technology or major version MUST be documented and approved through a constitution amendment; it MUST NOT be introduced as an incidental implementation choice.

### 2. Integrations Have Clear Boundaries

- The React application MUST handle presentation and user interaction; it MUST NOT call Jira or Confluence APIs with privileged credentials.
- The Express backend MUST own Jira and Confluence API access, credential handling, authorization enforcement, and integration-specific error handling.
- Jira and Confluence integrations MUST be isolated behind backend service or adapter boundaries. Provider-specific responses MUST be mapped into application-owned data structures before being used by other application layers.
- The application MUST NOT bypass or weaken the approved access controls of Jira or Confluence.

### 3. Security and Data Protection Are Default Requirements

- Secrets MUST NOT be committed to source control, exposed in browser bundles, or written to logs. Local configuration MUST use documented placeholders rather than real credentials.
- Integrations MUST use approved authentication and least-privilege credentials. Authentication choices MUST be confirmed against the target Jira and Confluence environments before implementation.
- Backend routes MUST validate inputs and enforce the approved access policy before exposing or changing data.
- Logs and error responses MUST avoid disclosing credentials, tokens, or sensitive provider data.

### 4. Data Changes Must Be Safe and Traceable

- PostgreSQL schema changes MUST use reviewable, versioned migrations; application behavior MUST NOT depend on undocumented manual database changes.
- External synchronization and automation MUST be designed to avoid duplicate side effects when safely retried.
- Data transformations MUST preserve relevant source identifiers and make mappings explicit. Destructive or irreversible changes MUST require an explicit product requirement and safeguards.
- Provider errors, partial failures, and rejected data MUST be surfaced explicitly; the system MUST NOT report success when an operation has failed.

### 5. Verification Is Part of Delivery

- Automated tests MUST cover changed behavior and the relevant API, authorization, integration, and data-transformation boundaries.
- Changes MUST be checked against their specification acceptance criteria. Tests MUST NOT depend on live Jira or Confluence services unless a test explicitly requires an authorized integration environment.
- A change is complete only after applicable tests and checks pass, or any unavailable verification is clearly reported.

### 6. Work Is Spec-Driven

- Work MUST proceed from clarified requirements and acceptance criteria to a plan, implementation tasks, and verified implementation.
- Unspecified provider versions, field mappings, authentication methods, access policies, and deployment assumptions MUST be confirmed in the relevant specification rather than silently guessed.
- Specifications and plans MUST identify relevant security, data-integrity, and failure-handling behavior.

## Governance

- This constitution takes precedence over conflicting project-level plans and implementation conventions.
- Amendments MUST state the rationale and affected principles. Specifications, plans, and code affected by an amendment MUST be brought into compliance.
- Where a requirement conflicts with this constitution, work MUST pause at that conflict until the requirement is clarified or the constitution is amended.
