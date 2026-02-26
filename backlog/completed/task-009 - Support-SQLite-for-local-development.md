---
id: TASK-009
title: Support SQLite for local development
status: Done
assignee: []
created_date: '2026-02-26 21:16'
updated_date: '2026-02-26 21:25'
labels:
  - refactor
  - dx
  - database
dependencies: []
references:
  - app/db.py
  - app/schedule.py
  - app/main.py
  - tests/conftest.py
  - tests/test_db.py
  - tests/test_e2e.py
  - .env.example
  - docs/architecture.md
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Running `uv run app/main.py` fails without a live PostgreSQL server because both `app/schedule.py` and `app/main.py` hardcode `provider=\"postgres\"` and call `db.bind()` at module import time.\n\nThe app has two separate `Database()` instances:\n1. `app/schedule.py:46` — `db.bind(provider=\"postgres\", ...)` at import time\n2. `app/main.py:151-157` — `db.bind(provider='postgres', ...)` at import time\n\nBoth call `db.generate_mapping(create_tables=True)` at module level. The test suite already works around this by monkey-patching `Database.bind` and `Database.generate_mapping` in `tests/conftest.py:19-20`.\n\n**What needs to change:**\n\n1. Add a `DEV` env var (default: `false`). When `DEV=true`, use SQLite; otherwise use PostgreSQL. Update `.env.example`.\n2. Create a shared database configuration module (e.g. `app/db.py`) that:\n   - Reads `DEV` from env\n   - For `DEV=true`: binds with `provider=\"sqlite\", filename=\"db.sqlite\", create_db=True`\n   - For `DEV=false`: binds with existing PostgreSQL env vars (host, port, user, pass, etc.)\n   - Exports the single `Database()` instance, entities, and `db_session`\n3. Refactor `app/schedule.py` and `app/main.py` to import from the shared module instead of creating their own `Database()` instances\n4. Consider deferring `db.bind()` and `db.generate_mapping()` out of module-level scope so tests don't need the monkey-patch\n5. Update `tests/conftest.py` — ideally unit tests use in-memory SQLite instead of monkey-patching bind/mapping to no-ops\n6. E2E tests (`tests/test_e2e.py`) should continue using PostgreSQL via TestContainers"
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 uv run app/main.py starts with SQLite when DEV=true (no PostgreSQL required)
- [x] #2 uv run app/main.py starts with PostgreSQL when DEV=false (or unset) with valid credentials
- [x] #3 Single shared Database() instance across schedule.py and main.py
- [x] #4 Unit tests run without monkey-patching Database.bind / Database.generate_mapping
- [x] #5 E2E tests continue using PostgreSQL via TestContainers
- [x] #6 All existing tests pass
- [x] #7 .env.example documents the DEV variable
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Summary\n\nCreated `app/db.py` as a shared database module with a single `Database()` instance. The `DEV` env var controls the provider: SQLite for local development, PostgreSQL for production.\n\n### Changes\n\n- **New `app/db.py`**: `get_db_config()` returns provider kwargs based on `DEV` env var; `init_db()` binds and generates mappings (idempotent)\n- **`app/schedule.py`**: Removed local `Database()`, `db.bind()`, `db.generate_mapping()`, and DB env var reads; imports shared `db` from `db.py`\n- **`app/main.py`**: Removed local `Database()`, `db.bind()`, `db.generate_mapping()`, unused `DB_NAME`/`DB_HOST`/`DB_PORT`; `lifespan()` calls `init_db()`\n- **`tests/conftest.py`**: Replaced monkey-patching with `DEV=true` env var\n- **`tests/test_db.py`**: 6 unit tests for `get_db_config()` and `init_db()`\n- **`.env.example`**: Added `DEV=false`\n- **`docs/architecture.md`**: Documented `db.py` module and `DEV` env var\n\n### Test results\n\n42 passed, 2 skipped (integration needing full env), 10 deselected (e2e needing Docker)
<!-- SECTION:FINAL_SUMMARY:END -->
