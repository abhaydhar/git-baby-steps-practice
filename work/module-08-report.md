# Module 08 Completion Report

## Tracked Files
.gitignore
README.md
calculator.py
main.py
project_spec.md

## Spec Commit History
ac17cb6 (HEAD -> main, origin/main, origin/HEAD) .

## project_spec.md Contents
# Jira Sprint Dashboard Requirements

## 1. Purpose

The dashboard must show sprint progress and delivery status for the team's Jira work.

It should help users understand:

- Which work is currently in progress.
- Which work has been completed.
- Which work remains planned or blocked.
- Which sprint or sprints are being reviewed.
- Who owns the work and when it is due.

## 2. Users and Access

### Primary users

- Team members
- Project stakeholders
- External stakeholders identified by the organization

### Access model

- Use Jira native access controls for dashboard visibility.
- External stakeholders must receive full dashboard access.
- The dashboard must not rely on a separate application-level authorization model.

### Maintenance ownership

- A team lead is responsible for maintaining and configuring the dashboard.
- Dashboard configuration changes must be reviewable through the team's normal Jira governance process.

## 3. Sprint Scope

The dashboard must display all sprints by default, including historical and future sprint data.

Users must be able to filter the dashboard by:

- Sprint
- Project
- Assignee
- Issue type

## 4. Dashboard Content

### Displayed issue information

Each issue must show the following information where available:

- Issue status
- Assignee
- Due date
- Priority

The dashboard must not assume story points unless the Jira project has a supported points field and the team chooses to use it.

### Progress representation

The dashboard must display issue completion percentage as:

$$
\text{Completion Percentage} = \frac{\text{Completed Issues}}{\text{Total Issues in Sprint}} \times 100
$$

The initial status categories must be:

- To Do
- In Progress
- Done

### Refresh behavior

The dashboard must automatically refresh Jira data when the dashboard view is opened or refreshed.

#### Data refresh frequency

The dashboard must refresh Jira data at least once every day. The daily refresh must be scheduled and must not depend on a user opening or manually refreshing the dashboard.

## 5. Dashboard Layout

The dashboard must use a timeline and metrics layout with the following components:

- Sprint summary metrics
- Sprint timeline
- Issue completion percentage
- Status distribution
- Filter controls for sprint, project, assignee, and issue type

The dashboard should be suitable for reviewing progress across all displayed sprints, not only the current sprint.

## 6. Technical Approach

### Platform

The dashboard will be implemented as a separate web application that retrieves Jira data through an API.

### Jira environment

The selected target environment is Jira Server. The actual Jira Server URL and version have not yet been confirmed and must be supplied before implementation.

### Authentication

The application must use an approved Jira authentication method. The current proposed method is SSO with a service account, although the selected Jira API authentication method must be validated against the Jira Server version and deployment.

### Data source

The application must read Jira sprint and issue data through Jira Server APIs.

## 7. Acceptance Criteria

The dashboard is complete when:

1. A user can view sprint progress for all configured sprints.
2. A user can filter by sprint, project, assignee, and issue type.
3. The dashboard displays issue status, assignee, due date, and priority.
4. The dashboard displays issued completion percentage.
5. The dashboard distinguishes To Do, In Progress, and Done issues.
6. Jira data refreshes automatically at least once every day.
7. Team members and project stakeholders can access the dashboard through Jira permissions.
8. External stakeholders can access the dashboard according to the approved organization policy.
9. The dashboard is maintained by a team lead.
10. The dashboard can be configured against a confirmed Jira Server endpoint and version.

## 8. Open Requirements and Dependencies

The following information must be confirmed before implementation begins:

- Actual Jira Server URL
- Jira Server version and supported API version
- Jira project and sprint field names
- Issue type, status, assignee, due date, priority, and story-point mappings
- Whether story points are required for progress reporting
- Authorized Jira integration identity and authentication method
- Exact external stakeholder distribution and access policy
- Team lead responsible for dashboard maintenance
- Deployment target and hosting environment for the separate web application
- Whether the dashboard should expose only summary data to external stakeholders or full Jira issue data

## 9. Non-goals

The initial version does not require:

- A custom Jira status taxonomy beyond To Do, In Progress, and Done.
- Detailed risk, owner, and date fields beyond the requested issue metadata.
- Story-point-based progress calculations unless explicitly enabled.
- Full Jira administrative control or issue editing from the dashboard.
