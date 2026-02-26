---
id: TASK-003
title: Replace Node.js with Deno via mise
status: In Progress
assignee: []
created_date: '2026-02-26 17:10'
updated_date: '2026-02-26 17:16'
labels:
  - infra
  - deno
  - mise
dependencies: []
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the Node.js runtime with Deno for all JS/TS tooling in the project.

**Current state:**
- `.tool-versions` declares `nodejs 24.5.0`
- `package.json` has commitlint and cz-conventional-changelog dependencies
- `package-lock.json` exists with Node.js dependency tree
- `taskfiles/deno.yml` already exists with Deno-based task definitions (vite, playwright, etc.)
- `devbox.json` references `nodejs`

**Work required:**
1. Install Deno via mise (`mise use deno@latest`) and remove Node.js from `.tool-versions`
2. Migrate commitlint and commitizen (cz-conventional-changelog) to Deno-compatible alternatives or run via `deno run -A npm:`
3. Remove `package.json`, `package-lock.json`, and `node_modules/` once all deps are migrated
4. Update `devbox.json` to replace `nodejs` with `deno`
5. Update `.pre-commit-config.yaml` if any hooks depend on Node.js
6. Wire up `taskfiles/deno.yml` into `taskfile.yml` (replace `taskfiles/poetry.yml` or Node-based includes)
7. Verify all task commands work with Deno runtime
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Node.js removed from .tool-versions
- [ ] #2 Deno installed via mise and declared in .tool-versions
- [ ] #3 package.json and package-lock.json removed
- [ ] #4 commitlint and commitizen work under Deno
- [ ] #5 All task commands in taskfile.yml pass
- [ ] #6 devbox.json updated to reference deno instead of nodejs
- [ ] #7 Pre-commit hooks function without Node.js
<!-- AC:END -->
