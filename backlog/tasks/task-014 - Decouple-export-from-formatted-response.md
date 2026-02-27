---
id: TASK-014
title: Decouple export from formatted response
status: To Do
assignee: []
created_date: '2026-02-27 00:54'
labels:
  - refactor
dependencies: []
references:
  - app/main.py
  - app/meetup_query.py
  - app/slackbot.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Currently export_to_file calls format_response internally, and slackbot reads from a file on disk rather than receiving structured data. Separate the formatting/filtering step from the I/O step so callers can get structured data without file side effects, and slackbot can accept JSON directly instead of reading from a file.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 format_response returns structured data without writing to disk
- [ ] #2 export_to_file accepts pre-formatted data (no internal format_response call)
- [ ] #3 slackbot can receive JSON data directly instead of reading from file
- [ ] #4 Existing /api/events and /api/slack endpoints work unchanged
<!-- AC:END -->
