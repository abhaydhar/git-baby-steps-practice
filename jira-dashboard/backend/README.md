# Backend

## Local PostgreSQL

From `jira-dashboard/`, create a local environment file, replace the password with a random local-only value, and start PostgreSQL:

```powershell
Copy-Item .env.example .env
# Edit .env and set POSTGRES_PASSWORD.
docker compose up -d
docker compose ps
```

The database uses PostgreSQL 15, listens only on `127.0.0.1:5432`, and stores data in the `postgres_data` Docker volume. Keep `.env` local; do not commit it.

To run the backend with the local database, set `DATABASE_URL` to use the same credentials as `.env`:

```powershell
$env:DATABASE_URL = "postgresql://jira_dashboard:<password>@127.0.0.1:5432/jira_dashboard"
```

Then start the backend as described below. `GET /ready` reports whether PostgreSQL accepts a query.

## Run

Use the Node.js version in `.nvmrc`, then install dependencies and start the server:

```powershell
npm install
npm start
```

The server listens on port `3001` by default. Set `PORT` to use another port.

## Health endpoints

- `GET /health` returns `200` with `{"status":"ok"}` when the process responds.
- `GET /ready` returns `200` only when PostgreSQL accepts a query. It returns `503` when `DATABASE_URL` is unset or PostgreSQL is unavailable. The response does not expose database connection details.

These are operational endpoints only. No Jira or dashboard-data API is implemented.

## Tests

```powershell
npm test
```
