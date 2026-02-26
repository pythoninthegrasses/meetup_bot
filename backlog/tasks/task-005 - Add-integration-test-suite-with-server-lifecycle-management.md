---
id: TASK-005
title: Add integration test suite with server lifecycle management
status: To Do
assignee: []
created_date: '2026-02-26 18:06'
labels:
  - testing
dependencies: []
references:
  - tests/test_smoke.py
  - taskfile.yml
  - taskfiles/
  - ~/git/mt/taskfile.yml
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create integration test suite that tests component interactions (FastAPI routes with real TestClient, database interactions with test DB). Migrate test_smoke.py into integration tests. Add taskfile tasks for starting the server, running integration tests, and stopping the server. Server lifecycle should be managed automatically via taskfile (start in background, wait for healthy, run tests, stop).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pytest marker `integration` registered in pyproject.toml
- [ ] #2 test_smoke.py refactored to use integration marker and TestClient (no manual server needed)
- [ ] #3 Integration tests can run against a real or test database
- [ ] #4 task test:integration in taskfile handles server start/stop automatically
- [ ] #5 Server health check wait loop before test execution
<!-- AC:END -->
