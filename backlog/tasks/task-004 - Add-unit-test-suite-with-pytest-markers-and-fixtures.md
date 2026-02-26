---
id: TASK-004
title: Add unit test suite with pytest markers and fixtures
status: In Progress
assignee: []
created_date: '2026-02-26 18:06'
updated_date: '2026-02-26 18:08'
labels:
  - testing
dependencies: []
references:
  - tests/conftest.py
  - tests/test_main.py
  - tests/test_meetup_query.py
  - pyproject.toml
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Set up unit test infrastructure: pytest markers (`@pytest.mark.unit`), shared fixtures in conftest.py, and reorganize existing tests (test_main.py, test_meetup_query.py) under unit test markers. Unit tests must run in isolation with no external dependencies (no DB, no network, no running server). Add `[tool.pytest.ini_options]` to pyproject.toml with marker registration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 pytest marker `unit` registered in pyproject.toml
- [ ] #2 Existing tests in test_main.py and test_meetup_query.py marked as unit tests
- [ ] #3 Unit tests pass with `pytest -m unit` and require no external services
- [ ] #4 conftest.py provides shared fixtures for mocking external deps (DB, API, Slack)
- [ ] #5 task test:unit in taskfile runs unit tests via .venv
<!-- AC:END -->
