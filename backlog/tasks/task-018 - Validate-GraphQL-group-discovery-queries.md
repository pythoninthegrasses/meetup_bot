---
id: TASK-018
title: Validate GraphQL group discovery queries
status: To Do
assignee: []
created_date: '2026-02-27 00:54'
labels:
  - qa
dependencies: []
references:
  - app/meetup_queries.gql
  - app/meetup_query.py
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
meetup_queries.gql contains two unused query templates that need QA: (1) a keywordSearch query that returns node IDs for groups — need to verify these match the group IDs used elsewhere, and (2) a workflow to look up a group by ID and fall back to parsing urlname from URL if not found. These queries support the capture_groups GQL migration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Confirm keywordSearch node IDs match groupByUrlname IDs for the same groups
- [ ] #2 Document whether group lookup by ID is possible or if urlname is the only key
- [ ] #3 Update or remove meetup_queries.gql templates based on findings
<!-- AC:END -->
