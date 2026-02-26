---
id: TASK-012
title: Replace requests + requests-cache with httpx + hishel
status: Done
assignee: []
created_date: '2026-02-26 22:03'
updated_date: '2026-02-26 22:09'
labels:
  - refactor
  - dependencies
dependencies: []
references:
  - app/meetup_query.py
  - app/main.py
  - 'https://hishel.com'
  - 'https://www.python-httpx.org'
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
requests-cache uses global monkey-patching via `install_cache()` at module import time (meetup_query.py:52). This has two problems:

1. **No cache db is being created.** The `install_cache(Path(cache_fn))` call uses a relative path (`raw/meetup_query`) resolved against CWD at import time. Since the server runs from `app/`, the cache file either never materializes or lands in an unexpected location. The endpoint hits the Meetup API on every request with no caching benefit.

2. **Stale data accumulates in output.json.** `export_to_file` appends to `raw/output.json` within a TTL window rather than overwriting. Without a working cache layer, the file accumulates junk entries across requests (observed: null-name entries with test fixture URLs `url1`/`url2` leaking into live responses).

Replace `requests` + `requests-cache` with `httpx` + `hishel` (RFC 9111-compliant HTTP caching):

- `hishel.SyncCacheClient` wraps `httpx` with explicit, non-global caching
- `SyncSqliteStorage` provides SQLite-backed persistence with configurable TTL
- `CacheOptions` supports POST method caching (needed for GraphQL)
- Per-request TTL overrides via extensions metadata
- No monkey-patching — cache is scoped to the client instance
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 requests and requests-cache are removed from dependencies
- [x] #2 httpx and hishel are added as dependencies
- [x] #3 All GraphQL requests (send_request, send_batched_group_request) use a shared hishel SyncCacheClient with SyncSqliteStorage
- [x] #4 Cache storage uses an absolute path that works regardless of CWD
- [x] #5 POST requests to the GraphQL endpoint are cached with a configurable TTL (default 30 minutes)
- [x] #6 Cache db file is confirmed to exist after a request
- [x] #7 The /api/events endpoint returns no stale or duplicate entries from prior requests
- [x] #8 Existing tests pass with the new HTTP client
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Replaced `requests` + `requests-cache` with `httpx` + `hishel` in meetup_query.py.

### Changes
- **pyproject.toml**: Removed `requests`/`requests-cache` from deps, added `httpx`/`hishel`. Removed redundant `httpx` from test extras (now a main dep).
- **app/meetup_query.py**: Replaced `requests`/`requests_cache` imports with `httpx`/`hishel`. Created module-level `http_client` (hishel `SyncCacheClient`) with `SyncSqliteStorage` using an absolute path (`script_dir / cache_fn`). Configured `SpecificationPolicy` with POST method caching and 30-minute default TTL. Updated `send_request` and `send_batched_group_request` to use `http_client.post()` and catch `httpx.HTTPError`.
- **tests/test_meetup_query.py**: Updated all mocks from `requests.post` to `meetup_query.http_client`. Added `test_http_client_exists` to verify the client is properly configured.
- **tests/test_main.py**: Added missing `send_batched_group_request` mock to `test_get_events` to prevent real HTTP calls.
- **tests/conftest.py**: Updated `mock_meetup_api` fixture to mock `meetup_query.http_client` instead of `requests.post`.

All 38 unit tests pass.
<!-- SECTION:FINAL_SUMMARY:END -->
