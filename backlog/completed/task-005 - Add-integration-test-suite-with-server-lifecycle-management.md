---
id: TASK-005
title: Add integration test suite with server lifecycle management
status: Done
assignee: []
created_date: '2026-02-26 18:06'
updated_date: '2026-02-26 18:23'
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
- [x] #1 pytest marker `integration` registered in pyproject.toml
- [x] #2 test_smoke.py refactored to use integration marker and TestClient (no manual server needed)
- [x] #3 Integration tests can run against a real or test database
- [x] #4 task test:integration in taskfile handles server start/stop automatically
- [x] #5 Server health check wait loop before test execution
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Changes\n\n### pyproject.toml\n- Add `[tool.pytest.ini_options]` section with `markers` for `unit`, `integration`, `e2e`, and `property` test categories\n\n### tests/conftest.py\n- Add `_load_env_file()` helper to load `app/.env` when present (respects existing env vars)\n- Add `integration_client` fixture that provides a FastAPI `TestClient`, skipping gracefully when env vars or DB are unavailable\n\n### tests/test_smoke.py\n- Replace `requests`-based smoke test with `TestClient`-based integration test\n- Add `@pytest.mark.integration` marker\n- Split into `TestHealthz` class with `test_status_code` and `test_response_body` methods\n- No longer requires a running server (uses in-process TestClient)\n\n### Pre-existing (no changes needed)\n- `taskfiles/pytest.yml` already implements `test:integration` with server start/defer-stop/wait lifecycle\n- `taskfile.yml` already delegates `test:integration` to `pytest:test:integration`"
<!-- SECTION:FINAL_SUMMARY:END -->
