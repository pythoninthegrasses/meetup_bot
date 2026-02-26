---
id: TASK-006
title: Add e2e test suite with full stack testing
status: To Do
assignee: []
created_date: '2026-02-26 18:06'
labels:
  - testing
dependencies: []
references:
  - app/main.py
  - taskfile.yml
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create end-to-end test suite that validates complete user workflows against the running application (auth flow, event retrieval, Slack posting). E2E tests run against a fully started server with real HTTP requests. Taskfile task manages full lifecycle: start server + deps, run e2e tests, teardown.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pytest marker `e2e` registered in pyproject.toml
- [ ] #2 E2E tests validate auth login flow end-to-end
- [ ] #3 E2E tests validate event retrieval pipeline
- [ ] #4 task test:e2e in taskfile manages full server lifecycle
- [ ] #5 E2E tests use real HTTP requests (requests library), not TestClient
<!-- AC:END -->
