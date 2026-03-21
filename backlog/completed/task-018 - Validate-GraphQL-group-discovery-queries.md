---
id: TASK-018
title: Validate GraphQL group discovery queries
status: Done
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-03-21 01:06'
labels:
  - qa
dependencies: []
references:
  - app/meetup_queries.gql
  - app/meetup_query.py
priority: low
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
meetup_queries.gql contains two unused query templates that need QA: (1) a keywordSearch query that returns node IDs for groups — need to verify these match the group IDs used elsewhere, and (2) a workflow to look up a group by ID and fall back to parsing urlname from URL if not found. These queries support the capture_groups GQL migration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Confirm keywordSearch node IDs match groupByUrlname IDs for the same groups
- [x] #2 Document whether group lookup by ID is possible or if urlname is the only key
- [x] #3 Update or remove meetup_queries.gql templates based on findings
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Findings

### AC#1: keywordSearch IDs match groupByUrlname IDs
Verified for three overlapping groups:
- `pythonistas`: `35460866` (match)
- `okcwebdevs`: `33258520` (match)
- `okccoffeeandcode`: `24875064` (match)

The `groupSearch` query returns 37 results for "programming" in the OKC area (topicCategoryId 546). IDs are consistent across query types.

### AC#2: Group lookup by ID
- `group(id: $id)` — works, returns full group data
- `node(id: $id)` — does NOT exist in Meetup's GraphQL schema (ValidationError)
- `groupByUrlname(urlname: $urlname)` — works (already in use)

Both `group(id:)` and `groupByUrlname(urlname:)` are valid lookup keys.

### AC#3: meetup_queries.gql updates
- Fixed stale `self` query to use `memberEvents(first: 10)` with `totalCount` (was using deprecated `upcomingEvents`/`count`)
- Fixed `groupByUrlname` query to use `events(first: 3)` with `totalCount` (was using deprecated `upcomingEvents`/`count`)
- Added `group(id:)` query template with documentation
- Added comments to `groupSearch` noting ID consistency and that `node(id:)` is not available
<!-- SECTION:FINAL_SUMMARY:END -->
