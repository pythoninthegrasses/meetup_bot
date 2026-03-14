---
id: TASK-016
title: Replace capture_groups Playwright scraper with GraphQL
status: In Progress
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-02-27 01:14'
labels:
  - refactor
dependencies: []
references:
  - app/capture_groups.py
  - app/meetup_queries.gql
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
capture_groups.py uses Playwright to scrape Meetup's web UI for group urlnames, then writes to CSV. It should also skip groups under the Techlahoma Foundation (currently noted but not implemented). Replace the scraper with the Meetup GraphQL API (keywordSearch query already exists in meetup_queries.gql) and add Techlahoma Foundation filtering.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 capture_groups uses GraphQL keywordSearch instead of Playwright
- [ ] #2 Techlahoma Foundation affiliated groups are excluded from results
- [ ] #3 Output format (groups.csv with urlname column) is unchanged
- [ ] #4 Playwright dependency can be removed from the project
<!-- AC:END -->
