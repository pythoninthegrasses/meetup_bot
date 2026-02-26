---
id: TASK-008
title: Fix deprecation warnings in test suite
status: Done
assignee: []
created_date: '2026-02-26 21:01'
updated_date: '2026-02-26 21:08'
labels:
  - tech-debt
  - deprecation
dependencies: []
references:
  - 'app/main.py:306'
  - 'https://fastapi.tiangolo.com/advanced/events/'
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Running `task test:e2e` produces 3 deprecation warnings that should be resolved:

1. **passlib `crypt` module** (`.venv/lib/python3.11/site-packages/passlib/utils/__init__.py:854`): passlib imports the `crypt` stdlib module which is deprecated in 3.12 and removed in 3.13. This blocks Python version upgrades. Options: replace passlib with a maintained alternative (e.g. `bcrypt` directly, `argon2-cffi`, or `pwdlib`), or pin/patch passlib.

2. **`on_event("startup")` in `app/main.py:306`**: FastAPI's `@app.on_event("startup")` decorator is deprecated. Migrate to the lifespan context manager pattern per FastAPI docs.

3. **FastAPI internal `on_event` deprecation** (`.venv/lib/python3.11/site-packages/fastapi/applications.py:4495`): This is a downstream effect of #2 — fixing the app code will eliminate this warning.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Migrate app/main.py from @app.on_event('startup') to lifespan context manager pattern
- [x] #2 Replace or update passlib to eliminate crypt module deprecation warning
- [x] #3 Running `task test:e2e` produces zero deprecation warnings
- [x] #4 All existing tests continue to pass
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Changes

### Replace passlib with direct bcrypt usage (`app/main.py`)
- Removed `from passlib.context import CryptContext` import, replaced with `import bcrypt`
- Removed `pwd_context = CryptContext(...)` instance
- `verify_password()` now uses `bcrypt.checkpw()` directly
- `get_password_hash()` now uses `bcrypt.hashpw()` directly

### Migrate startup event to lifespan context manager (`app/main.py`)
- Added `asynccontextmanager` and `AsyncIterator` imports
- Created `lifespan()` async context manager with the user-creation logic from the old `startup_event()`
- Passed `lifespan=lifespan` to `FastAPI()` constructor
- Removed `@app.on_event("startup")` decorator and `startup_event()` function

### Dependency cleanup
- Removed `passlib[bcrypt]` from `pyproject.toml` dependencies
- Updated `uv.lock` (passlib removed)
- Removed passlib from `requirements.txt`
- Updated `docs/architecture.md` dependency table

### Tests
- Added `tests/test_deprecation.py` with 7 tests covering:
  - Password hashing correctness (hash format, verify correct/incorrect)
  - No passlib import in main.py source
  - No `on_event` usage in main.py source
  - App has lifespan context configured
  - No crypt deprecation warnings during password operations
- All 36 tests pass with `-W error::DeprecationWarning`
<!-- SECTION:FINAL_SUMMARY:END -->
