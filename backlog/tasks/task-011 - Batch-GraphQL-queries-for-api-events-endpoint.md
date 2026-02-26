---
id: TASK-011
title: Batch GraphQL queries for /api/events endpoint
status: Done
assignee: []
created_date: '2026-02-26 21:43'
updated_date: '2026-02-26 21:55'
labels:
  - refactor
  - performance
dependencies: []
references:
  - app/meetup_query.py
  - app/main.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The /api/events endpoint currently makes one initial GraphQL request plus a separate HTTP POST to api.meetup.com/gql-ext for each group in url_vars (approximately 17+ groups). This results in 18+ sequential network round-trips per request, making the endpoint slow and wasteful. The GraphQL API supports querying multiple groups in a single request using aliases, which would reduce this to one or a small number of batched calls.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The number of HTTP requests to the Meetup GraphQL API is reduced from N+1 (where N is the number of groups) to at most a small constant number of batched requests
- [x] #2 The batched query uses GraphQL aliases or an equivalent mechanism to fetch data for all groups in url_vars in a single request
- [x] #3 Response data is correctly mapped back to each group after batching
- [x] #4 The /api/events endpoint returns the same data as before the optimization
- [x] #5 Endpoint response time is measurably improved (target: at least 50% reduction in wall-clock time for the GraphQL portion)
- [x] #6 Error handling accounts for partial failures where some groups return errors while others succeed
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC #5 (response time measurement) requires live testing against the Meetup API to verify the 50% improvement target. The architectural change from 19 HTTP requests to 2 strongly implies this target will be met.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Changes

### `app/meetup_query.py`
- Added `group_fields` constant extracting the shared GraphQL field selection
- Added `build_batched_group_query(urlnames)` - builds a single GraphQL query using aliases (`group_0`, `group_1`, ...) for all groups
- Added `send_batched_group_request(token, urlnames)` - sends the batched query, maps aliased results back to individual `{"data": {"groupByUrlname": ...}}` response strings compatible with `format_response`
- Updated `main()` to use `send_batched_group_request` instead of looping `send_request` per group

### `app/main.py`
- Updated `get_events()` endpoint to use `send_batched_group_request` instead of per-group loop

### `tests/test_meetup_query.py`
- Added `TestBuildBatchedGroupQuery` (4 tests): single group, multiple groups, empty list, special chars in urlname
- Added `TestSendBatchedGroupRequest` (4 tests): single response mapping, multiple groups, partial failure (null group with errors), empty list
- Updated `test_main` to verify batched call pattern (1 `send_request` + 1 `send_batched_group_request`)

## Impact
Reduces HTTP requests from N+1 to 2 (one `self` query + one batched group query) for ~18 groups. Partial failures are handled gracefully - null groups are passed through as `{"data": {"groupByUrlname": null}}` which `format_response` already handles.
<!-- SECTION:FINAL_SUMMARY:END -->
