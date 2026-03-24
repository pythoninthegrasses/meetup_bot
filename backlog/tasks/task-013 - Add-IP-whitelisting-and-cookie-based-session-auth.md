---
id: TASK-013
title: Add IP whitelisting and cookie-based session auth
status: Done
assignee:
  - Claude
created_date: '2026-02-27 00:54'
updated_date: '2026-03-20 23:34'
labels:
  - auth
dependencies: []
references:
  - app/main.py
priority: medium
ordinal: 2500
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Two auth improvements: (1) populate public_ips in IPConfig so external IPs can bypass bearer auth, and (2) store the user session in a browser cookie instead of keeping it only in memory, so users don't need to re-authenticate on every request.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 IPConfig.public_ips is configurable (env var or config file) and tested
- [x] #2 User session is persisted in a secure, httponly cookie
- [x] #3 Existing bearer token auth still works alongside cookie auth
- [x] #4 Tests cover both cookie-based and IP-whitelisted auth paths
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

### AC #1: IPConfig.public_ips configurable via env var
- Add `PUBLIC_IPS` env var (comma-separated) read via `decouple.config`
- Pass into `IPConfig(public_ips=...)` at initialization
- Empty/unset means no public IPs (current default)

### AC #2: Cookie-based session persistence
- After successful login at `/token` and `/auth/login`, set `session_token` httponly cookie with the JWT
- Modify `get_current_user` to check cookie fallback when no Bearer token present
- Cookie attrs: httponly, secure (HTTPS), samesite=lax, max_age from TOKEN_EXPIRE

### AC #3: Bearer token still works alongside cookie
- `get_current_user` checks Bearer first, falls back to cookie — no breaking changes
- `ip_whitelist_or_auth` unchanged

### AC #4: Tests
- Unit: IPConfig with PUBLIC_IPS env var, is_ip_allowed with public IPs, get_current_user cookie extraction
- E2E: login sets cookie, subsequent cookied request works, bearer still works
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
All 4 ACs implemented and tested. 12 new unit tests + 4 new e2e tests. 88 total tests passing.
<!-- SECTION:NOTES:END -->
