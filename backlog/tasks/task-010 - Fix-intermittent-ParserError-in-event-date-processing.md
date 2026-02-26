---
id: TASK-010
title: Fix intermittent ParserError in event date processing
status: Done
assignee: []
created_date: '2026-02-26 21:43'
updated_date: '2026-02-26 21:48'
labels:
  - bug
dependencies: []
references:
  - app/meetup_query.py
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The /api/events endpoint intermittently raises a ParserError with the message "date column is already in correct format" during event processing in app/meetup_query.py. The current handling silently catches the error and prints a message, but the root cause is that the date column sometimes arrives already parsed (as a Timestamp) and sometimes as a raw string. This non-determinism likely stems from pandas type inference or caching behavior, and the try/except block masks the real issue rather than handling both input formats reliably.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The date column is reliably converted to ISO 8601 format regardless of its input type (raw string or pre-parsed Timestamp)
- [x] #2 The ParserError catch-all in app/meetup_query.py is replaced with explicit type checking that handles both formats
- [x] #3 The /api/events endpoint returns consistent date formats across repeated calls with the same input data
- [x] #4 Unit tests cover both code paths: raw string dates and already-parsed Timestamp dates
- [x] #5 No silent pass on ParserError — unexpected parsing failures raise or log at an appropriate level
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Changes

### `app/meetup_query.py`
- Replaced the `try/except ParserError` catch-all in `sort_json` with explicit type checking
- `pd.Timestamp` values: converted via `strftime('%Y-%m-%dT%H:%M:%S')`
- String values in `ddd M/D h:mm a` format: parsed with `arrow.get()`, year defaulting to 0001 is replaced with current year
- String values in ISO 8601 or other arrow-parseable formats: handled via fallback `arrow.get(value)`
- Unparseable strings and unexpected types: logged with descriptive error/warning messages, set to `None` (handled downstream by `errors='coerce'`)
- Fixed trailing whitespace formatting issue (pre-existing)

### `tests/test_meetup_query.py`
- `test_sort_json_with_string_dates`: validates human-readable string dates are correctly parsed, year-corrected, and sorted
- `test_sort_json_with_timestamp_dates`: validates pre-parsed Timestamp dates (from pandas type inference) are handled correctly
- `test_sort_json_consistent_output_both_formats`: validates both input formats produce identical output
<!-- SECTION:FINAL_SUMMARY:END -->
