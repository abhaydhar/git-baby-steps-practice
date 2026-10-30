# Jira Sprint Dashboard Implementation Backlog

## Decisions Applied

- **Release scope:** Include external stakeholder access and full Jira issue details.
- **Phasing:** Execute the phases in strict order: Setup → Core Features → Integration → Testing → Documentation.
- **Story points:** Treat story points as optional and enable them only after the Jira field is confirmed and the team approves the behavior.
- **Target platform:** Separate web application backed by Jira Server APIs.
- **Initial status taxonomy:** To Do, In Progress, and Done.

## Phase 1: Setup

### 1.1 Confirm the Jira environment

- [ ] Confirm the Jira Server URL and supported API version ([GitHub issue #1](https://github.com/abhaydhar/jira-confluence-automation/issues/1)). **[MCP: jira]**
- [ ] Record the Jira Server version in the project configuration and release notes ([GitHub issue #2](https://github.com/abhaydhar/jira-confluence-automation/issues/2)). **[MCP + Custom skill]**
- [ ] Confirm the Jira project key, project identifier, and sprint fields ([GitHub issue #3](https://github.com/abhaydhar/jira-confluence-automation/issues/3)). **[MCP: jira]**
- [ ] Confirm the field mappings for status, assignee, due date, priority, issue type, and any optional story points ([GitHub issue #4](https://github.com/abhaydhar/jira-confluence-automation/issues/4)). **[MCP: jira]**
- [ ] Identify the Jira API endpoints required for sprints and issues ([GitHub issue #5](https://github.com/abhaydhar/jira-confluence-automation/issues/5)). **[MCP: jira]**
- [ ] Confirm whether the dashboard must retrieve only summary data or full issue details for external users ([GitHub issue #6](https://github.com/abhaydhar/jira-confluence-automation/issues/6)). **[Custom skill]**

### 1.2 Confirm access and ownership

- [ ] Identify the team lead responsible for dashboard maintenance ([GitHub issue #7](https://github.com/abhaydhar/jira-confluence-automation/issues/7)). **[Custom skill]**
- [ ] Define the authorized Jira integration identity and authentication method ([GitHub issue #8](https://github.com/abhaydhar/jira-confluence-automation/issues/8)). **[MCP + Custom skill]**
- [ ] Verify the integration identity has permission to read the required sprints and issues ([GitHub issue #9](https://github.com/abhaydhar/jira-confluence-automation/issues/9)). **[MCP: jira]**
- [ ] Define internal and external stakeholder groups ([GitHub issue #10](https://github.com/abhaydhar/jira-confluence-automation/issues/10)). **[Custom skill]**
- [ ] Obtain approval for external stakeholder access through Jira permissions ([GitHub issue #11](https://github.com/abhaydhar/jira-confluence-automation/issues/11)). **[Custom skill]**
- [ ] Document the application-level authorization boundary and confirm that Jira native access controls are authoritative ([GitHub issue #12](https://github.com/abhaydhar/jira-confluence-automation/issues/12)). **[Custom skill]**

### 1.3 Establish the application foundation

- [ ] Select the web framework and frontend runtime ([GitHub issue #13](https://github.com/abhaydhar/jira-confluence-automation/issues/13)). **[Custom skill]**
- [ ] Define the repository structure for frontend, backend, configuration, tests, and documentation ([GitHub issue #14](https://github.com/abhaydhar/jira-confluence-automation/issues/14)). **[Custom skill]**
- [ ] Add a versioned configuration file for Jira endpoint, authentication, project, and refresh settings ([GitHub issue #15](https://github.com/abhaydhar/jira-confluence-automation/issues/15)). **[Custom skill]**
- [ ] Add environment-variable handling for secrets and non-secret configuration ([GitHub issue #16](https://github.com/abhaydhar/jira-confluence-automation/issues/16)). **[Custom skill]**
- [ ] Add a structured logging configuration and a consistent error-handling policy ([GitHub issue #17](https://github.com/abhaydhar/jira-confluence-automation/issues/17)). **[Custom skill]**
- [ ] Add dependency version constraints and a reproducible install process ([GitHub issue #18](https://github.com/abhaydhar/jira-confluence-automation/issues/18)). **[Custom skill]**
- [ ] Create a local development configuration that does not contain real credentials ([GitHub issue #19](https://github.com/abhaydhar/jira-confluence-automation/issues/19)). **[Custom skill]**

### 1.4 Define the implementation contract

- [ ] Define the Jira API response model for sprint summaries and issue details ([GitHub issue #20](https://github.com/abhaydhar/jira-confluence-automation/issues/20)). **[MCP + Custom skill]**
- [ ] Define the normalized dashboard data model ([GitHub issue #21](https://github.com/abhaydhar/jira-confluence-automation/issues/21)). **[Custom skill]**
- [ ] Define the behavior for missing assignees, due dates, priorities, and statuses ([GitHub issue #22](https://github.com/abhaydhar/jira-confluence-automation/issues/22)). **[Custom skill]**
- [ ] Define the behavior for empty, malformed, or partially unavailable Jira responses ([GitHub issue #23](https://github.com/abhaydhar/jira-confluence-automation/issues/23)). **[Custom skill]**
- [ ] Define the default filter values and the behavior when no sprint is selected ([GitHub issue #24](https://github.com/abhaydhar/jira-confluence-automation/issues/24)). **[Custom skill]**

## Phase 2: Core Features

### 2.1 Dashboard layout and navigation

- [ ] Add a dashboard page with a sprint summary metrics section. **[Custom skill]**
- [ ] Add a sprint timeline section that displays all configured sprints. **[Custom skill]**
- [ ] Add an issue completion percentage metric. **[Custom skill]**
- [ ] Add a status distribution visualization for To Do, In Progress, and Done. **[Custom skill]**
- [ ] Add responsive layout behavior for desktop and mobile viewports. **[Custom skill]**
- [ ] Add navigation or links to the dashboard and its configuration documentation. **[Custom skill]**

### 2.2 Sprint and issue display

- [ ] Display all sprints by default, including historical and future sprints. **[Custom skill]**
- [ ] Display the sprint name, project, status, start date, and end date when available. **[Custom skill]**
- [ ] Display issue status, assignee, due date, and priority where available. **[Custom skill]**
- [ ] Display the issue key, summary, and project identifier. **[Custom skill]**
- [ ] Render users without an assignee, due date, or priority as a clear unavailable value. **[Custom skill]**
- [ ] Add a visible indicator for blocked work and distinguish it from the initial To Do, In Progress, and Done categories. **[Custom skill]**

### 2.3 Progress calculations

- [ ] Calculate completion percentage as completed issues divided by total issues in the selected sprint. **[Custom skill]**
- [ ] Define whether completed means a Jira issue status equal to Done. **[MCP + Custom skill]**
- [ ] Exclude issues outside the selected sprint and filters from the calculation. **[Custom skill]**
- [ ] Handle zero-issue sprints without producing divide-by-zero errors. **[Custom skill]**
- [ ] Display the completed, total, and remaining issue count for the selected scope. **[Custom skill]**
- [ ] Add optional story-point calculations only after the Jira story-point field and team decision are confirmed. **[MCP + Custom skill]**

### 2.4 Filtering

- [ ] Add filters for sprint, project, assignee, and issue type. **[Custom skill]**
- [ ] Add a reset filter action that restores all configured sprints. **[Custom skill]**
- [ ] Preserve filter selections when the dashboard is refreshed. **[Custom skill]**
- [ ] Support multiple projects and assignees when the UI design requires multi-select behavior. **[Custom skill]**
- [ ] Show the active filter state and a clear indication of the number of matching issues. **[Custom skill]**

### 2.5 External stakeholder experience

- [ ] Define the external dashboard view as the same dashboard view governed by Jira permissions. **[Custom skill]**
- [ ] Ensure external users receive the approved summary and issue data according to policy. **[Custom skill]**
- [ ] Add an explicit access-denied state when Jira permissions do not allow access. **[MCP + Custom skill]**
- [ ] Ensure full issue details are hidden when the organization policy permits only summary data. **[Custom skill]**
- [ ] Document the external stakeholder data-access matrix. **[Custom skill]**

## Phase 3: Integration

### 3.1 Jira API client

- [ ] Implement the Jira Server API client using the confirmed endpoint and API version. **[MCP + Custom skill]**
- [ ] Add request timeout, retry, and rate-limit handling. **[Custom skill]**
- [ ] Map Jira API responses into the normalized dashboard data model. **[MCP + Custom skill]**
- [ ] Add API error handling that reports a useful message without exposing credentials. **[Custom skill]**
- [ ] Add a health check that verifies connectivity and required Jira permissions. **[MCP: jira]**

### 3.2 Sprint and issue retrieval

- [ ] Retrieve all configured sprints, including historical and future sprint data. **[MCP: jira]**
- [ ] Retrieve the issue metadata required for status, assignee, due date, priority, and issue type. **[MCP: jira]**
- [ ] Apply the selected sprint, project, assignee, and issue-type filters. **[MCP + Custom skill]**
- [ ] Support pagination when Jira returns more than the configured page size. **[MCP + Custom skill]**
- [ ] Handle Jira API field names and aliases using the approved mapping configuration. **[MCP + Custom skill]**

### 3.3 Authentication and authorization

- [ ] Configure Jira SSO and service-account authentication using the approved method. **[MCP + Custom skill]**
- [ ] Validate that the integration identity can read the expected projects and sprints. **[MCP: jira]**
- [ ] Apply Jira native access controls to dashboard content. **[MCP + Custom skill]**
- [ ] Reject unauthorized access through a clear error or access-denied response. **[Custom skill]**
- [ ] Ensure secrets are never rendered in logs, browser responses, or client-side configuration. **[Custom skill]**

### 3.4 Scheduled refresh

- [ ] Implement an automated scheduled refresh that runs at least once every day. **[Custom skill]**
- [ ] Ensure refresh is not dependent on a user opening or manually refreshing the dashboard. **[Custom skill]**
- [ ] Store refresh timestamps and the last successful data source time. **[Custom skill]**
- [ ] Log refresh failures and successful refresh counts. **[Custom skill]**
- [ ] Add retry behavior for transient Jira API failures. **[Custom skill]**
- [ ] Provide a manual refresh action for troubleshooting and validation. **[MCP + Custom skill]**

### 3.5 Deployment integration

- [ ] Confirm the approved hosting environment and deployment target. **[Custom skill]**
- [ ] Add deployment configuration for the backend and frontend. **[Custom skill]**
- [ ] Configure the application to read Jira credentials from the deployment environment. **[Custom skill]**
- [ ] Add a deployment health check and startup validation. **[MCP + Custom skill]**
- [ ] Verify that the deployed application can reach the confirmed Jira Server endpoint. **[MCP: jira]**

## Phase 4: Testing

### 4.1 Unit tests

- [ ] Test the completion-percentage calculation for normal, empty, and zero-total cases. **[Custom skill]**
- [ ] Test issue status grouping for To Do, In Progress, and Done. **[Custom skill]**
- [ ] Test filtering by sprint, project, assignee, and issue type. **[Custom skill]**
- [ ] Test missing optional Jira fields and malformed values. **[MCP + Custom skill]**
- [ ] Test pagination and partial API responses. **[MCP + Custom skill]**
- [ ] Test error handling and retry behavior. **[Custom skill]**

### 4.2 Integration tests

- [ ] Test the Jira API client against the confirmed Jira Server environment. **[MCP: jira]**
- [ ] Test sprint retrieval and issue retrieval with representative Jira data. **[MCP: jira]**
- [ ] Test the authentication flow and permission failures. **[MCP: jira]**
- [ ] Test scheduled refresh behavior and the last-refresh timestamp. **[MCP + Custom skill]**
- [ ] Test dashboard rendering with real Jira data copied from a validated test project. **[MCP + Custom skill]**

### 4.3 End-to-end tests

- [ ] Verify that team members can view the dashboard through Jira permissions. **[MCP + Custom skill]**
- [ ] Verify that external stakeholders receive the approved data scope. **[MCP + Custom skill]**
- [ ] Verify that users without access receive an access-denied result. **[MCP + Custom skill]**
- [ ] Verify that filters update the metrics, timeline, and issue list. **[Custom skill]**
- [ ] Verify that the dashboard works across supported desktop and mobile screen sizes. **[Custom skill]**
- [ ] Verify that no Jira credentials are exposed in the browser or logs. **[Custom skill]**

### 4.4 Quality and release validation

- [ ] Run the full automated test suite. **[Custom skill]**
- [ ] Run static analysis and formatting checks. **[Custom skill]**
- [ ] Run dependency and security scanning. **[Custom skill]**
- [ ] Validate the deployed application against the confirmed Jira Server version. **[MCP: jira]**
- [ ] Confirm that no known functional or security defects remain open for release. **[Custom skill]**
- [ ] Perform a release candidate smoke test in the target environment. **[MCP + Custom skill]**

## Phase 5: Documentation

### 5.1 User documentation

- [ ] Document how to access the dashboard. **[Custom skill]**
- [ ] Document all dashboard filters and their behavior. **[Custom skill]**
- [ ] Document the meaning of completion percentage and status categories. **[Custom skill]**
- [ ] Document how external stakeholder access is governed. **[Custom skill]**
- [ ] Document how to report a dashboard access or data issue. **[Custom skill]**

### 5.2 Operations documentation

- [ ] Document Jira endpoint, version, project, field mappings, and API permissions. **[MCP + Custom skill]**
- [ ] Document the scheduled refresh frequency and troubleshooting steps. **[Custom skill]**
- [ ] Document the deployment target, startup requirements, and rollback process. **[Custom skill]**
- [ ] Document the team lead responsible for maintenance and configuration reviews. **[Custom skill]**
- [ ] Document secret-management and credential-rotation instructions. **[Custom skill]**

### 5.3 Maintenance and governance

- [ ] Define the review process for dashboard configuration changes. **[Custom skill]**
- [ ] Define the process for updating Jira field mappings after Jira upgrades. **[MCP + Custom skill]**
- [ ] Define the process for adding or removing projects, sprints, and stakeholder groups. **[Custom skill]**
- [ ] Add a release checklist for deployment and post-deployment validation. **[Custom skill]**
- [ ] Add a known-issues log and a decision log for open requirements. **[Custom skill]**

### 5.4 Final delivery

- [ ] Confirm the final acceptance criteria against implemented behavior. **[Custom skill]**
- [ ] Attach test results and deployment evidence to the release record. **[Custom skill]**
- [ ] Publish the user and operations documentation. **[Custom skill]**
- [ ] Complete a final review with the team lead and project stakeholders. **[Custom skill]**
- [ ] Mark the implementation as complete only after all required acceptance criteria pass. **[Custom skill]**

## Priority Order

1. Confirm Jira endpoint, version, mappings, identity, and access policy.
2. Build the normalized data model and Jira API integration.
3. Implement sprint metrics, timeline, filters, and issue details.
4. Add scheduled refresh and authorization enforcement.
5. Run integration, end-to-end, security, and quality tests.
6. Publish user, operations, governance, and maintenance documentation.

## Definition of Done

A task is complete only when:

- The implementation or documentation change is present in the repository.
- Automated validation is run for code changes.
- Relevant acceptance criteria are verified.
- Errors and missing data are handled explicitly.
- Secrets and credentials are not committed or exposed.
- The work is reviewed by the responsible team lead or reviewer.

---

## MCP Server vs Custom Skill Breakdown

### Legend
- **[MCP: jira]** - Use existing Jira MCP server (`https://mcp.epam.com/mcp/jira`)
- **[Custom skill]** - Requires custom skill/implementation
- **[MCP + Custom skill]** - Combination: MCP provides data/validation, custom skill implements logic

### Summary by Phase

**Phase 1: Setup**
- MCP-only tasks: 7 (environment checks, field confirmations, permission validation)
- MCP + Custom skill: 3 (authentication, data model design, configuration)
- Custom-only tasks: 12 (application foundation, business decisions, documentation)

**Phase 2: Core Features**
- MCP-only tasks: 0
- MCP + Custom skill: 3 (status definitions, story points, access control)
- Custom-only tasks: 20 (all UI/UX implementation)

**Phase 3: Integration**
- MCP-only tasks: 6 (sprint retrieval, issue retrieval, health checks, endpoint verification)
- MCP + Custom skill: 10 (API client, data mapping, auth configuration, pagination)
- Custom-only tasks: 7 (error handling, retry logic, scheduled refresh, deployment)

**Phase 4: Testing**
- MCP-only tasks: 3 (Jira API testing, integration tests)
- MCP + Custom skill: 7 (test data validation, E2E tests, smoke tests)
- Custom-only tasks: 8 (unit tests, quality checks, test framework)

**Phase 5: Documentation**
- MCP-only tasks: 0
- MCP + Custom skill: 2 (Jira configuration docs, field mapping updates)
- Custom-only tasks: 18 (all user, operations, governance documentation)

### Total Task Distribution
- **MCP-only tasks**: 16 (13% of tasks)
- **MCP + Custom skill**: 25 (21% of tasks)
- **Custom-only tasks**: 65 (54% of tasks)
- **Business decision tasks** (subset of custom): ~12 (10% of tasks)

### Critical MCP Dependencies
The Jira MCP server is **essential** for:
1. Environment and configuration discovery (Phase 1.1)
2. Authentication and permission validation (Phases 1.2, 3.3)
3. Real-time data retrieval for sprints and issues (Phase 3.2)
4. Integration and end-to-end testing (Phase 4)
5. Post-deployment validation (Phase 4.4)

### Recommended Approach
1. **Start with MCP tasks** in Phase 1.1 to gather Jira environment information
2. **Use MCP output** to inform custom skill implementations (data models, API clients)
3. **Leverage MCP for testing** throughout Phases 4.1-4.4
4. **Build custom skills** for all business logic, UI, and infrastructure tasks
