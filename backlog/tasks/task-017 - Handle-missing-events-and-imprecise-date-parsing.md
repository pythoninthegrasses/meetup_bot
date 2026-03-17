---
id: TASK-017
title: Handle missing events and imprecise date parsing
status: To Do
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-03-17 02:09'
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
- [ ] #1 format_response returns empty DataFrame when group has no upcoming events without errors
- [ ] #2 sort_json derives year from the original ISO 8601 dateTime field instead of guessing
- [ ] #3 Tests cover empty event lists and year-boundary date parsing
<!-- AC:END -->
