---
id: TASK-015
title: Fix timezone display to distinguish CST and CDT
status: Done
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-03-21 01:00'
labels:
  - bug
dependencies: []
references:
  - app/main.py
priority: low
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The /api/check-schedule endpoint formats times with ZZZ (e.g. "Monday 14:00 CST") but doesn't verify whether the abbreviation reflects the actual DST state. Arrow's ZZZ token should handle this correctly given 'America/Chicago', but the behavior needs to be validated and tested for both standard and daylight saving time periods.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Verify arrow ZZZ output is correct for both CST and CDT with America/Chicago tz
- [x] #2 Add tests covering schedule time display in both standard and daylight saving periods
- [x] #3 Document findings if no code change is needed
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Findings

Arrow's `ZZZ` token correctly outputs "CST" during standard time and "CDT" during daylight saving time when the Arrow datetime has `America/Chicago` timezone. Verified empirically:
- January 2026: "CST"
- June 2026: "CDT"
- March 8 (DST spring-forward): "CDT"
- November 1 (DST fall-back): "CST"

No code change needed for the ZZZ formatting itself.

## Plan

1. AC #1: Verified — no code change needed
2. AC #2: Add unit tests in `tests/test_unit.py` that assert arrow `ZZZ` produces correct abbreviations for CST and CDT periods, including DST transition boundaries
3. AC #3: Document findings in task notes

## Related issue (out of scope)

`current_time_local` in `app/main.py:49` is computed at module load time, not per-request. This means the check-schedule endpoint uses a stale timestamp. Filed as separate task.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Findings

Arrow's `ZZZ` format token correctly outputs timezone abbreviations based on the actual DST state of the datetime object. When using `America/Chicago`:
- Standard time (Nov-Mar): outputs "CST"
- Daylight saving time (Mar-Nov): outputs "CDT"
- DST transition days: correctly reflects the post-transition state

No code change was needed. The existing `format("dddd HH:mm ZZZ")` calls in `app/main.py:464-465` work correctly.

A separate issue was identified: `current_time_local` is computed at module load time (TASK-020).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified that arrow's `ZZZ` format token correctly distinguishes CST and CDT when using `America/Chicago` timezone. No code change needed.

Added 9 unit tests in `TestArrowTimezoneAbbreviation` covering:
- Standard time months (Jan, Feb, Dec) -> CST
- Daylight saving months (Jun, Jul) -> CDT
- Spring-forward transition day (Mar 8) -> CDT
- Fall-back transition day (Nov 1) -> CST
- Format string shape matching check-schedule endpoint
- UTC-to-local conversion preserving correct abbreviation

Filed TASK-020 for the separate issue of stale module-level time computation in `app/main.py`.
<!-- SECTION:FINAL_SUMMARY:END -->
