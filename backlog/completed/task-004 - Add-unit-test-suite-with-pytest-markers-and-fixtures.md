---
id: TASK-004
title: Add unit test suite with pytest markers and fixtures
status: Done
assignee: []
created_date: '2026-02-26 18:06'
updated_date: '2026-02-26 19:57'
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
- [x] #1 pytest marker `unit` registered in pyproject.toml
- [x] #2 Existing tests in test_main.py and test_meetup_query.py marked as unit tests
- [x] #3 Unit tests pass with `pytest -m unit` and require no external services
- [x] #4 conftest.py provides shared fixtures for mocking external deps (DB, API, Slack)
- [x] #5 task test:unit in taskfile runs unit tests via .venv
- [x] #6 All unit tests pass with pytest -m unit (no failures)
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
All acceptance criteria verified:
- `unit` marker registered in `[tool.pytest.ini_options]` in pyproject.toml (merged duplicate sections)
- Tests in test_main.py and test_meetup_query.py use `@pytest.mark.unit`
- 18 unit tests pass with `pytest -m unit`, no external services required
- conftest.py provides fixtures: mock_db, mock_slack_client, mock_meetup_api, mock_env, groups_csv_fixture
- `task test:unit` defined in taskfiles/pytest.yml, delegated from root taskfile.yml
- All 18 unit tests pass (0 failures)

Note: Fixed duplicate `[tool.pytest.ini_options]` section in pyproject.toml during verification.
<!-- SECTION:FINAL_SUMMARY:END -->
