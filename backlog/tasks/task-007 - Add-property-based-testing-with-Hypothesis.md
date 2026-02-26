---
id: TASK-007
title: Add property-based testing with Hypothesis
status: To Do
assignee: []
created_date: '2026-02-26 18:06'
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
- [ ] #1 pytest marker `property` registered in pyproject.toml
- [ ] #2 Property tests for format_response with varied GraphQL response shapes
- [ ] #3 Property tests for sort_csv/sort_json ordering invariants
- [ ] #4 Property tests for JWT token roundtrip encode/decode
- [ ] #5 task test:property in taskfile runs property-based tests via .venv
- [ ] #6 Hypothesis profiles configured (ci profile with max_examples=200, dev with 50)
<!-- AC:END -->
