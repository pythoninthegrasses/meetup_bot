---
id: TASK-020
title: Fix stale module-level current_time_local in main.py
status: To Do
assignee: []
created_date: '2026-03-21 00:58'
labels:
  - bug
dependencies: []
references:
  - 'app/main.py:49-51'
  - 'app/main.py:435-472'
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
`current_time_local` (line 49), `current_time_utc` (line 50), and `current_day` (line 51) in `app/main.py` are computed once at module load time. The `/api/check-schedule` endpoint uses these values, so it always reflects the server startup time rather than the actual request time. This causes incorrect time comparisons and stale timezone abbreviations if the server runs across a DST boundary.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 current_time_local, current_time_utc, and current_day are computed per-request in endpoints that use them
- [ ] #2 Existing tests continue to pass
- [ ] #3 Add test verifying time values reflect request time, not server startup time
<!-- AC:END -->
