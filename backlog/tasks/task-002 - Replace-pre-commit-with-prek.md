---
id: TASK-002
title: Replace pre-commit with prek
status: Done
assignee: []
created_date: '2026-02-26 16:56'
updated_date: '2026-02-26 17:55'
labels:
  - tooling
  - dx
dependencies: []
references:
  - 'https://github.com/j178/prek'
  - .pre-commit-config.yaml
  - CLAUDE.md
documentation:
  - 'https://prek.j178.dev'
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the Python-based `pre-commit` tool with `prek` (j178/prek), a Rust-based reimplementation that is faster, dependency-free, and compatible with existing `.pre-commit-config.yaml` configuration.

## Current Setup

The project uses pre-commit with these hooks (`.pre-commit-config.yaml`):

- **gitleaks** (`zricethezav/gitleaks` v8.30.0) - secret detection
- **ruff** (`astral-sh/ruff-pre-commit` v0.15.3) - Python linting with `--fix --exit-non-zero-on-fix`
- **pre-commit-hooks** (`pre-commit/pre-commit-hooks` v6.0.0) - check-added-large-files, check-executables-have-shebangs, check-merge-conflict, check-shebang-scripts-are-executable, check-symlinks, debug-statements, destroyed-symlinks, detect-private-key, end-of-file-fixer, fix-byte-order-marker, mixed-line-ending, requirements-txt-fixer, check-toml, check-yaml, pretty-format-json

## Migration Notes

- prek is a drop-in replacement that reads `.pre-commit-config.yaml` natively
- prek has built-in Rust implementations for `pre-commit-hooks` repo hooks (faster)
- Install via `mise` (preferred): add `prek` to `.tool-versions` or `mise.toml`
- Run `prek install` to set up git hooks
- Run `prek run --all-files` to verify all hooks pass
- Update Taskfile, CLAUDE.md, and CI workflows to reference `prek` instead of `pre-commit`
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 prek is installed via mise and configured as the git hook runner
- [x] #2 All existing hooks (gitleaks, ruff, pre-commit-hooks) pass with prek
- [x] #3 pre-commit Python package is removed from dev dependencies
- [x] #4 Taskfile `pre-commit` task updated to use prek
- [x] #5 CLAUDE.md references updated from pre-commit to prek
- [x] #6 CI workflows updated if applicable
- [x] #7 `prek run --all-files` passes cleanly
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Replaced `pre-commit` with `prek` (j178/prek) across the project:

- prek 0.3.2 installed via mise, git hooks already configured by prek
- All hooks (gitleaks, ruff, pre-commit-hooks) pass with `prek run --all-files`
- `pre-commit` Python package was not in dev dependencies (no removal needed)
- Taskfile `pre-commit` task already used `prek run` (updated in prior session)
- CLAUDE.md reference updated to `prek run --all-files` (prior session)
- AGENTS.md reference updated to `prek run --all-files`
- devbox.json package changed from `pre-commit` to `prek`
- JSON formatting and trailing newline fixes applied by prek hooks
- No CI workflow changes needed (no pre-commit references in workflows)

Commit: cc2098e
<!-- SECTION:FINAL_SUMMARY:END -->
