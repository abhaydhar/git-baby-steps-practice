# Express Environment Test Design

## Goal

Create an isolated npm project at `work/env-test`, install Express, and verify that the package imports successfully.

## Scope

- Initialize the project using npm defaults (`npm init -y`).
- Install Express as a project dependency.
- Do not add application or server source code.
- Do not change files outside `work/env-test`.

## Verification

- Print Node.js and npm versions used for setup.
- Confirm Express appears in the project's dependency manifest.
- Require Express from within the new project and report its installed package version.
- Preserve and report any setup or verification error; do not claim success if a command fails.
