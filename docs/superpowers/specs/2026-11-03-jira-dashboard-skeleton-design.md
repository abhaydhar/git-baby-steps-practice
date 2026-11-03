# Jira Dashboard Skeleton Design

## Goal

Create a blank React frontend and Node.js backend folder skeleton for the Jira sprint dashboard without implementing application behavior.

## Placement

Create a separate `jira-dashboard/` directory at the repository root. The repository currently contains a Python calculator, so the web application must not mix its files into that project's root.

## Structure

```text
jira-dashboard/
├── frontend/
│   ├── public/
│   │   └── .gitkeep
│   └── src/
│       ├── components/.gitkeep
│       ├── features/.gitkeep
│       ├── services/.gitkeep
│       └── App.jsx
├── backend/
│   ├── src/
│   │   ├── routes/.gitkeep
│   │   ├── services/.gitkeep
│   │   ├── jobs/.gitkeep
│   │   ├── middleware/.gitkeep
│   │   └── server.js
│   └── tests/.gitkeep
├── docs/.gitkeep
├── .env.example
├── .gitignore
└── README.md
```

## Constraints

- All files are empty placeholders; no application code, package manifests, dependencies, or configuration values are added.
- Do not alter files outside `jira-dashboard/`, except this design record.
- Verify the resulting directory and file list.
