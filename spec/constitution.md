# Jira/Confluence Automation Constitution

This constitution defines the non-negotiable principles for the Jira/Confluence automation project. Product specifications and implementation plans must comply with it. A proposed exception requires an explicit, documented amendment before implementation.

## Core Principles

### 1. The Approved Technology Stack Is Binding

- The frontend MUST use React 18 and Vite.
- The backend MUST use Node.js and Express.
- PostgreSQL 15 MUST be the relational database and MUST be run through Docker as specified by the project.
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
