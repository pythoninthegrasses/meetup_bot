---
id: TASK-015
title: Fix timezone display to distinguish CST and CDT
status: To Do
assignee: []
created_date: '2026-02-27 00:54'
labels:
  - bug
dependencies: []
references:
  - app/main.py
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The /api/check-schedule endpoint formats times with ZZZ (e.g. "Monday 14:00 CST") but doesn't verify whether the abbreviation reflects the actual DST state. Arrow's ZZZ token should handle this correctly given 'America/Chicago', but the behavior needs to be validated and tested for both standard and daylight saving time periods.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Verify arrow ZZZ output is correct for both CST and CDT with America/Chicago tz
- [ ] #2 Add tests covering schedule time display in both standard and daylight saving periods
- [ ] #3 Document findings if no code change is needed
<!-- AC:END -->
