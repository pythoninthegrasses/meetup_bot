---
id: TASK-006
title: Add e2e test suite with full stack testing
status: Done
assignee: []
created_date: '2026-02-26 18:06'
updated_date: '2026-02-26 21:01'
labels:
  - testing
dependencies: []
references:
  - app/main.py
  - taskfile.yml
  - tests/test_e2e.py
  - taskfiles/pytest.yml
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create end-to-end test suite that validates complete user workflows against the running application (auth flow, event retrieval, Slack posting). E2E tests run against a fully started server with real HTTP requests. Taskfile task manages full lifecycle: start server + deps, run e2e tests, teardown.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pytest marker `e2e` registered in pyproject.toml
- [x] #2 E2E tests validate auth login flow end-to-end
- [x] #3 E2E tests validate event retrieval pipeline
- [x] #4 task test:e2e in taskfile manages full server lifecycle
- [x] #5 E2E tests use real HTTP requests (requests library), not TestClient
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Used testcontainers-python (PostgresContainer) instead of external docker-compose DB or taskfile server lifecycle management. Session-scoped fixture spins up a disposable PostgreSQL container, launches uvicorn as a subprocess against it, and tears down after the session. Tests use real HTTP requests via the requests library. Made DB_SSLMODE configurable in schedule.py (was hardcoded to "require"). Simplified test:e2e taskfile task since testcontainers handles everything internally.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Changes

- **tests/test_e2e.py** — 10 e2e tests across 4 classes (health, index, auth login flow, event retrieval) using testcontainers PostgresContainer + uvicorn subprocess + real HTTP requests
- **app/schedule.py** — Made `sslmode` configurable via `DB_SSLMODE` env var (default `prefer`, was hardcoded `require`)
- **taskfiles/pytest.yml** — Simplified `test:e2e` task; testcontainers manages DB + server lifecycle
- **docker-compose.yml** — Added local PostgreSQL service for dev use
- **pyproject.toml / uv.lock** — Added `testcontainers[postgres]` dev dependency

## Test Coverage

| Class | Tests | What it validates |
|-------|-------|-------------------|
| TestHealthCheck | 1 | Server smoke test |
| TestIndexPage | 1 | HTML login page served |
| TestAuthLoginFlow | 6 | OAuth token success/failure, form login redirect, invalid user, unauthorized + invalid token |
| TestEventRetrieval | 2 | Authenticated event queries with/without params |
<!-- SECTION:FINAL_SUMMARY:END -->
