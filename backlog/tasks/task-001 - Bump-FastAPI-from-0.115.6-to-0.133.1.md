---
id: TASK-001
title: Bump FastAPI from >=0.115.6 to >=0.133.1
status: In Progress
assignee: []
created_date: '2026-02-26 16:25'
updated_date: '2026-03-21 01:19'
labels:
  - dependencies
dependencies:
  - TASK-004
  - TASK-005
  - TASK-006
  - TASK-007
references:
  - 'https://github.com/fastapi/fastapi/pull/14964'
  - pyproject.toml
priority: low
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update FastAPI dependency in pyproject.toml from >=0.115.6 to >=0.133.1. This is a routine dependency bump covering ~18 minor versions. Notable changes include Rust-powered JSON serialization via Pydantic (0.131.0) and deprecation of ORJSONResponse/UJSONResponse. Test suite should be reviewed and updated before upgrading to ensure compatibility.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Review and update test suite for compatibility with FastAPI 0.133.1 before upgrading
- [x] #2 Bump fastapi dependency to >=0.133.1 in pyproject.toml
- [x] #3 All existing tests pass after upgrade
- [x] #4 Verify /token, /healthz, /, and /auth/login endpoints work correctly
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Upgraded from FastAPI 0.115.14 to 0.135.1 (resolved from >=0.133.1). Relaxed python-multipart upper bound from <0.0.10 to uncapped. No code changes required — all APIs used (TestClient, Form, Depends, CORSMiddleware, etc.) remained stable. New transitive dep: annotated-doc 0.0.4.
<!-- SECTION:NOTES:END -->
