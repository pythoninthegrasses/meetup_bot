---
id: TASK-013
title: Add IP whitelisting and cookie-based session auth
status: To Do
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-03-17 02:09'
labels:
  - auth
dependencies: []
references:
  - app/main.py
priority: medium
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Two auth improvements: (1) populate public_ips in IPConfig so external IPs can bypass bearer auth, and (2) store the user session in a browser cookie instead of keeping it only in memory, so users don't need to re-authenticate on every request.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 IPConfig.public_ips is configurable (env var or config file) and tested
- [ ] #2 User session is persisted in a secure, httponly cookie
- [ ] #3 Existing bearer token auth still works alongside cookie auth
- [ ] #4 Tests cover both cookie-based and IP-whitelisted auth paths
<!-- AC:END -->
