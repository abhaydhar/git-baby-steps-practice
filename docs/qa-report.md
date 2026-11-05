# QA Report — Jira Sprint Dashboard Prototype

- **Assessment date**: 2026-11-05
- **Application URL**: `http://127.0.0.1:5173/`
- **Scope**: Browser inspection and smoke checks performed during this session. The implementation is an explicitly mock-only placeholder; it is not the future Jira-integrated product.

## Summary

The single-page frontend loads and renders its mock-only notice. The browser reported no JavaScript errors or warnings, but did report a missing favicon (`/favicon.ico`, HTTP 404). Backend endpoint tests and the frontend production build passed. The backend was reachable during an earlier smoke check in this session (`/health` returned 200 and `/ready` returned 503); it is not currently listening. Docker Desktop's engine is stopped, so PostgreSQL did not start and live database connectivity could not be verified.

**Current status**: Frontend build and browser rendering pass. Backend unit tests pass, but the backend service is currently stopped. PostgreSQL/Compose runtime verification is blocked by the stopped Docker engine. One low-impact browser resource issue remains: favicon 404.

## Pages Visited

| Page | URL | Result |
|---|---|---|
| Jira Sprint Dashboard — Prototype | `http://127.0.0.1:5173/` | Loaded successfully in Chrome; full-page screenshot captured and shown in the session. This was the only application page/route found. |

No additional application routes or pages were present to visit.

## Visible Elements Tested

Inspected using the Chrome accessibility snapshot and page screenshot:

| Element | Visible content / behavior | Result |
|---|---|---|
| Link | “Sprintboard home”, links to `/` | Present; points back to the same main page. |
| Prototype label | “Prototype” | Present. |
| Local-preview label | “Local preview” | Present. |
| Main heading | “Jira Sprint Dashboard” | Present. |
| Introductory text | “A starting point for a clearer view of sprint work. This prototype is not connected to Jira and does not display Jira data.” | Present; accurately states the mock-only boundary. |
| Notice heading | “Mock-only preview” | Present. |
| Notice text | “No Jira connection, account access, or sprint data is active. Nothing here represents current project information.” | Present. |
| Footer | “Dashboard prototype” and “Local preview only” | Present. |
| Buttons | None | No buttons are implemented. |
| Forms and inputs | None | No forms or input controls are implemented. |

The page has no login, Jira data, sprint list, issue details, filters, refresh control, or other dashboard interactions. These absences are consistent with the currently approved placeholder scope.

## Checks and Results

| Check | Result | Evidence |
|---|---|---|
| Frontend HTTP response | **Pass** | `GET http://127.0.0.1:5173/` returned HTTP 200. |
| Browser rendering | **Pass** | Chrome showed the application title, main heading, mock-only notice, and footer. |
| Main frontend network assets | **Pass** | Document, Vite client, React entry point, app JavaScript, and stylesheet returned HTTP 200. |
| Browser JavaScript console | **Pass with resource issue** | No JavaScript errors or warnings were reported. One resource-load error is recorded below. |
| Backend automated tests | **Pass** | `npm test` in `jira-dashboard/backend/`: 3 passed, 0 failed. Tests cover `/health` and `/ready` response behavior using injected database-check outcomes. |
| Frontend production build | **Pass** | `npm run build` in `jira-dashboard/frontend/`: Vite 8.3.5 completed successfully. |
| Backend smoke check (earlier in this session) | **Partial** | While the server was running, `/health` returned `200 {"status":"ok"}`. `/ready` returned HTTP 503 because PostgreSQL was unavailable. |
| Backend current availability | **Unavailable** | At the latest check, port 3001 was not listening; `/health` and `/ready` could not be reached. |
| Docker Compose configuration | **Configuration valid; runtime blocked** | `docker compose config --quiet` succeeded. `docker compose up` failed because the Docker Desktop Engine API was unavailable; Docker Desktop reported `stopped`. |
| PostgreSQL connectivity | **Not verified / unavailable** | TCP port 5432 did not accept a connection. No live database query was completed. |

## Bugs and Issues Found

| ID | Severity | Issue | Evidence | Status |
|---|---|---|---|---|
| QA-001 | Low | The browser requests `/favicon.ico`, but the application does not provide it. | Chrome Network panel showed `GET http://127.0.0.1:5173/favicon.ico` returned HTTP 404; the console reported “Failed to load resource: the server responded with a status of 404 (Not Found).” | **Open** |
| QA-002 | Environment blocker | Docker Desktop Engine is stopped, preventing PostgreSQL from starting. | `docker desktop status` reported `stopped`; `docker compose up` returned a Docker Engine API error; port 5432 refused the connection. | **Blocked by environment** |
| QA-003 | Environment/runtime status | Backend is not currently running, so its live endpoints cannot presently be used. | Latest check found no listener on port 3001. Earlier in this session, `/health` passed and `/ready` correctly reported the missing database with 503. | **Not running** |

No JavaScript runtime errors or warnings were found. QA-002 and QA-003 describe environment/service availability, not a confirmed application-code defect.

## Fixes Applied

No code fixes were applied as part of these QA checks. The missing favicon remains open. The Docker Engine blocker could not be resolved from this session; Compose configuration is valid, but the service could not be started or tested.

## Current Status and Follow-up

- The frontend is running at `http://127.0.0.1:5173/` and its production build passes.
- The main placeholder page is visually verified and explicitly indicates that it is not connected to Jira.
- Backend tests pass, but the backend process is currently stopped.
- PostgreSQL is not running; live backend readiness and database access remain unverified until Docker Desktop's Engine is running.
- Add or configure a favicon if desired, then reload the page and verify `/favicon.ico` returns successfully and the console is clear.
- After starting Docker Desktop, run `docker compose up -d --wait` from `jira-dashboard/`, start the backend with a matching `DATABASE_URL`, and confirm `/ready` returns 200 before treating database connectivity as verified.
