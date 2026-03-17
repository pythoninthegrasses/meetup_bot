---
id: TASK-007
title: Add property-based testing with Hypothesis
status: Done
assignee: []
created_date: '2026-02-26 18:06'
updated_date: '2026-02-26 20:01'
labels:
  - testing
dependencies: []
references:
  - tests/test_meetup_query.py
  - app/meetup_query.py
  - app/sign_jwt.py
  - pyproject.toml
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add property-based tests using Hypothesis for data-driven validation. Target functions with complex input handling: format_response parsing, sort_csv/sort_json ordering invariants, schedule time calculations, JWT token encoding/decoding roundtrips. Hypothesis is already in test dependencies.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 pytest marker `property` registered in pyproject.toml
- [x] #2 Property tests for format_response with varied GraphQL response shapes
- [x] #3 Property tests for sort_csv/sort_json ordering invariants
- [x] #4 Property tests for JWT token roundtrip encode/decode
- [x] #5 task test:property in taskfile runs property-based tests via .venv
- [x] #6 Hypothesis profiles configured (ci profile with max_examples=200, dev with 50)
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added tests/test_property.py with 11 property-based tests using Hypothesis:

- **format_response** (4 tests): self-response returns DataFrame with correct columns, filters by location, group-response variant, malformed responses handled without crashing
- **sort_csv** (2 tests): output sorted by date invariant, duplicate removal by eventUrl
- **sort_json** (2 tests): output sorted by date invariant, duplicate removal by eventUrl
- **JWT roundtrip** (3 tests): encode/decode preserves claims, expired tokens rejected, wrong issuer rejected

Hypothesis profiles configured: `ci` (max_examples=200), `dev` (max_examples=50, loaded by default).

Pre-existing: `property` marker in pyproject.toml, `task test:property` in taskfiles/pytest.yml.
<!-- SECTION:FINAL_SUMMARY:END -->
