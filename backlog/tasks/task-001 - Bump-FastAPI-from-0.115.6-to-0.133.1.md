---
id: TASK-001
title: Bump FastAPI from >=0.115.6 to >=0.133.1
status: To Do
assignee: []
created_date: '2026-02-26 16:25'
labels:
  - dependencies
dependencies: []
references:
  - 'https://github.com/fastapi/fastapi/pull/14964'
  - pyproject.toml
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update FastAPI dependency in pyproject.toml from >=0.115.6 to >=0.133.1. This is a routine dependency bump covering ~18 minor versions. Notable changes include Rust-powered JSON serialization via Pydantic (0.131.0) and deprecation of ORJSONResponse/UJSONResponse. Test suite should be reviewed and updated before upgrading to ensure compatibility.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Review and update test suite for compatibility with FastAPI 0.133.1 before upgrading
- [ ] #2 Bump fastapi dependency to >=0.133.1 in pyproject.toml
- [ ] #3 All existing tests pass after upgrade
- [ ] #4 Verify /token, /healthz, /, and /auth/login endpoints work correctly
<!-- AC:END -->
