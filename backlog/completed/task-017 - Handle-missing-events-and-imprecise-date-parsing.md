---
id: TASK-017
title: Handle missing events and imprecise date parsing
status: Done
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-03-21 00:35'
labels:
  - bug
dependencies: []
references:
  - app/meetup_query.py
priority: medium
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Two related data quality issues in meetup_query.py: (1) When a group has no upcoming events, format_response falls through to city comparison on a None/empty response instead of gracefully returning empty. (2) sort_json uses heuristics to determine the year when dates are in 'ddd M/D h:mm a' format (no year), which can produce incorrect years near year boundaries.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 format_response returns empty DataFrame when group has no upcoming events without errors
- [x] #2 sort_json derives year from the original ISO 8601 dateTime field instead of guessing
- [x] #3 Tests cover empty event lists and year-boundary date parsing
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Commit b1ffb41 fixes both issues in meetup_query.py:

1. **format_response** now catches `TypeError` alongside `KeyError` and uses `.get()` for safer navigation of `memberEvents`, `groupByUrlname`, and `events` fields. Null intermediate API fields return an empty DataFrame instead of crashing.

2. **sort_json** and **prepare_events** year-derivation logic improved: when parsing year-less `'ddd M/D h:mm a'` dates, if assigning the current year produces a date more than 6 months in the past, it bumps to the next year. This correctly handles Dec/Jan year boundaries.

7 new unit tests cover empty event lists, null API fields, and year-boundary date parsing for both ISO 8601 and human-readable formats.
<!-- SECTION:FINAL_SUMMARY:END -->
