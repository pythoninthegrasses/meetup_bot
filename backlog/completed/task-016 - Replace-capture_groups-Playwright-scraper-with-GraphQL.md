---
id: TASK-016
title: Replace capture_groups Playwright scraper with GraphQL
status: Done
assignee: []
created_date: '2026-02-27 00:54'
updated_date: '2026-03-21 00:07'
labels:
  - refactor
dependencies: []
references:
  - app/capture_groups.py
  - app/meetup_queries.gql
priority: medium
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
capture_groups.py uses Playwright to scrape Meetup's web UI for group urlnames, then writes to CSV. It should also skip groups under the Techlahoma Foundation (currently noted but not implemented). Replace the scraper with the Meetup GraphQL API (keywordSearch query already exists in meetup_queries.gql) and add Techlahoma Foundation filtering.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 capture_groups uses GraphQL keywordSearch instead of Playwright
- [x] #2 Techlahoma Foundation affiliated groups are excluded from results
- [x] #3 Output format (groups.csv with urlname column) is unchanged
- [x] #4 Playwright dependency can be removed from the project
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
All acceptance criteria were already met prior to this session:

1. `app/capture_groups.py` uses GraphQL `groupSearch` query — no Playwright code remains
2. `filter_groups()` excludes Techlahoma Foundation groups via `TECHLAHOMA_PRO_NETWORK_ID`
3. `write_groups_csv()` outputs `groups.csv` with `url,urlname` columns, sorted by urlname
4. No Playwright dependency in `pyproject.toml` or any `.py` files

10 unit tests in `tests/test_unit.py` (TestParseSearchResponse, TestFilterGroups, TestWriteGroupsCsv) all pass.
<!-- SECTION:FINAL_SUMMARY:END -->
