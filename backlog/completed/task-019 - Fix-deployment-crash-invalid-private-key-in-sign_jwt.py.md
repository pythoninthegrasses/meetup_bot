---
id: TASK-019
title: 'Fix deployment crash: invalid private key in sign_jwt.py'
status: Done
assignee: []
created_date: '2026-03-16 23:02'
updated_date: '2026-03-20 23:11'
labels:
  - deployment
  - dokploy
dependencies: []
references:
  - 'app/sign_jwt.py:50'
  - 'app/main.py:23'
  - 'app/meetup_query.py:16'
  - CLAUDE.local.md
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Gunicorn workers crash on startup with `ValueError: Invalid private key` in `sign_jwt.py:50`.

**Stack trace summary:**
- `main.py:23` imports `meetup_query`
- `meetup_query.py:16` imports `sign_jwt.main`
- `sign_jwt.py:50` calls `serialization.load_pem_private_key()` which raises `ValueError: Invalid private key`

Both workers (pid 12, 13) fail to boot, causing gunicorn master to shut down.

**Likely causes:**
1. The `MEETUP_PRIVATE_KEY` env var is missing or empty on the Dokploy deployment
2. The private key value has been corrupted (e.g., newlines stripped, base64 encoding issues when pushed via `ic --env prod env`)
3. The key is being loaded at module level (import time), so any env var issue is fatal with no graceful error handling

**Environment:**
- Host: 85.31.233.80 (Dokploy)
- Logs from: 2026-03-16T22:59:21Z

**Investigation steps:**
1. Check if the private key env var is set: `ic --env prod exec web` and inspect env
2. Verify the key format — PEM keys need literal newlines, not `\n` escape sequences
3. Compare the deployed key value against the local `.env` value
4. If the key is correct but mangled, consider base64-encoding it and decoding at runtime
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Gunicorn workers start successfully without ValueError on Dokploy
- [x] #2 Private key is correctly loaded from environment in the deployed container
- [x] #3 sign_jwt.py handles missing/invalid key gracefully at import time (log error instead of crash)
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Wrapped module-level key loading in `app/sign_jwt.py` with try/except so invalid or missing keys log an error and set `private_key`/`public_key` to `None` instead of crashing gunicorn workers with `ValueError`. Added None guards in `sign_token()` (returns `None`) and `verify_token()` (returns `False`). Added 3 unit tests in `TestSignJwtGracefulKeyFailure`. Commit: `2327d5e`.
<!-- SECTION:FINAL_SUMMARY:END -->
