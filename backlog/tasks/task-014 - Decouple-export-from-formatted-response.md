---
id: TASK-014
title: Decouple export from formatted response
status: Done
assignee:
  - Claude
created_date: '2026-02-27 00:54'
updated_date: '2026-03-21 00:01'
labels:
  - refactor
dependencies: []
references:
  - app/main.py
  - app/meetup_query.py
  - app/slackbot.py
priority: medium
ordinal: 3750
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Currently export_to_file calls format_response internally, and slackbot reads from a file on disk rather than receiving structured data. Separate the formatting/filtering step from the I/O step so callers can get structured data without file side effects, and slackbot can accept JSON directly instead of reading from a file.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 format_response returns structured data without writing to disk
- [x] #2 export_to_file accepts pre-formatted data (no internal format_response call)
- [x] #3 slackbot can receive JSON data directly instead of reading from file
- [x] #4 Existing /api/events and /api/slack endpoints work unchanged
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

### 1. `export_to_file` accepts pre-formatted DataFrame (AC #2)
- Add optional `df` parameter to `export_to_file()`
- If `df` is provided, skip the internal `format_response()` call
- If `df` is None (backward compat for `meetup_query.main()`), call `format_response()` as before

### 2. `slackbot` can receive JSON data directly (AC #3)
- Add `fmt_events(events: list[dict])` to `slackbot.py` — same logic as `fmt_json` but takes data directly
- Keep `fmt_json()` for backward compatibility (`slackbot.main()` still uses it)

### 3. Refactor `main.py` endpoints for in-memory data flow (AC #4)
- `get_events()`: Call `format_response()` directly, collect DataFrames, concat, sort/dedupe in memory, return structured data
- `post_slack()`: Use return value from `get_events()`, pass to `fmt_events()` instead of reading file

### 4. Update tests
- `test_export_to_file` — test passing a pre-formatted DataFrame
- Add `test_fmt_events` — test new function with in-memory data
- `test_get_events` — remove file mocks, verify in-memory flow
- `test_post_slack` — verify `fmt_events` called instead of `fmt_json`
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Changes Made

### app/meetup_query.py
- `export_to_file()`: Added optional `df` parameter. When provided, skips internal `format_response()` call.
- `prepare_events(df)`: New function extracted from `sort_json()` logic — deduplicates, normalizes dates, sorts, filters past events, formats dates. Returns `list[dict]` in memory.

### app/slackbot.py
- `fmt_events(events)`: New function that formats a list of event dicts into Slack message strings (extracted from `fmt_json`).
- `fmt_json()`: Refactored to delegate to `fmt_events()` for backward compatibility.

### app/main.py
- `get_events()`: Collects DataFrames from `format_response()` calls, concatenates them, passes to `prepare_events()`. No file I/O.
- `post_slack()`: Uses return value from `get_events()` and passes directly to `fmt_events()`. No file reading.

### tests/test_unit.py
- Added: `test_export_to_file_with_preformatted_df`, `test_fmt_events`, `test_fmt_events_empty`, `test_prepare_events_deduplicates_and_sorts`, `test_prepare_events_empty`
- Updated: `test_get_events`, `test_post_slack`, `test_post_slack_passes_auth_to_get_events` to reflect in-memory data flow
<!-- SECTION:NOTES:END -->
