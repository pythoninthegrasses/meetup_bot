# meetup_bot Project Reference

## General Instructions

- Minimize inline comments
- Retain tabs, spaces, and encoding
- Fix linting errors before saving files.
  - Respect `.markdownlint.jsonc` rules for all markdown files
- If under 50 lines of code (LOC), print the full function or class
- If the token limit is close or it's over 50 LOC, print the line numbers and avoid comments altogether
- Explain as much as possible in the chat unless asked to annotate (i.e., docstrings, newline comments, etc.)

## Context7

Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.

### Libraries

- fastapi/fastapi
- roborev-dev/roborev
- websites/deno
- websites/taskfile_dev_usage

## Build, Lint, and Test Commands

- Full test suite: `task test`
- Unit tests: `task test:unit`
- Integration tests: `task test:integration` (auto server start/stop)
- E2E tests: `task test:e2e` (auto server start/stop)
- Property-based tests: `task test:property`
- Coverage: `task test:cov`
- Single test: `uv run pytest tests/test_filename.py::test_function_name`
- Pass extra args: `task test:unit -- -v -k test_health`
- Linting: `uv run ruff check --fix --respect-gitignore` or `task lint`
- Formatting: `uv run ruff format --respect-gitignore` or `task format`
- Check dependencies: `uv run deptry .` or `task deptry`
- Pre-commit hooks: `prek run --all-files` or `task pre-commit`

### Test Markers

Tests use pytest markers to categorize test types:

- `@pytest.mark.unit` — isolated tests, no external deps
- `@pytest.mark.integration` — component interactions, may need DB/server
- `@pytest.mark.e2e` — full stack with real HTTP requests
- `@pytest.mark.property` — Hypothesis property-based tests

### Test Taskfile Structure

Test tasks are defined in `taskfiles/pytest.yml` and delegated from the root `taskfile.yml`.
Integration and e2e tasks manage server lifecycle automatically (start, health wait, test, stop via `defer`).

## Code Style Guidelines

- **Formatting**: 4 spaces, 130-char line limit, LF line endings
- **Imports**: Ordered by type, combined imports when possible
- **Naming**: snake_case functions/vars, PascalCase classes, UPPERCASE constants
- **Type Hints**: Use Optional for nullable params, pipe syntax for Union
- **Error Handling**: Specific exception types, descriptive error messages
- **File Structure**: Core logic in app/core/, utilities in app/utils/
- **Docstrings**: Use double quotes for docstrings
- **Tests**: Files in tests/, follow test_* naming convention

## GraphQL API Troubleshooting

When debugging GraphQL API issues (particularly for Meetup API):

### 1. Direct GraphQL Testing

- Test queries directly against the GraphQL endpoint using curl before debugging application code
- Example: `curl -X POST "https://api.meetup.com/gql-ext" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"query": "query { self { id name } }"}'`
- Start with simple queries (like `self { id name }`) then gradually add complexity

### 2. API Migration Validation

- Check API documentation for migration guides when encountering field errors
- Common Meetup API changes:
  - `count` → `totalCount`
  - `upcomingEvents` → `memberEvents(first: N)` for self queries
  - `upcomingEvents` → `events(first: N)` for group queries
  - Syntax changes: `field(input: {first: N})` → `field(first: N)`

### 3. Response Structure Analysis

- Add temporary debug logging to inspect actual GraphQL responses
- Check for `errors` array in GraphQL responses, not just HTTP status codes
- Verify field existence with introspection or simple field queries
- Example debug pattern:
  ```python
  response_data = r.json()
  if 'errors' in response_data:
      print('GraphQL Errors:', json.dumps(response_data['errors'], indent=2))
  ```

### 4. Field Validation Process

- Use GraphQL validation errors to identify undefined fields
- Test field names individually: `{ self { fieldName } }`
- Check if field requires parameters (e.g., `memberEvents` requires `first`)
- Validate nested field access patterns

### 5. Token and Authentication Debugging

- Verify token generation is working: `uv run python -c "from app.sign_jwt import main; print(main())"`
- Test tokens directly against GraphQL endpoint outside of application
- Check token expiration and refresh token logic

## Code Review (roborev)

Every commit is automatically reviewed by [roborev](https://www.roborev.io/) via git hooks. Reviews run in the background and findings must be addressed before merging.

Config: `.roborev.toml` (project), `~/.roborev/config.toml` (global)

### CLI Commands

```bash
roborev show                          # List recent reviews
roborev show --job <id>               # View a specific review
roborev show --job <id> --json        # Machine-readable review output
roborev fix                           # Fix all unaddressed reviews
roborev fix <job_id>                  # Fix a specific review
roborev fix --unaddressed --list      # List unaddressed reviews without fixing
roborev refine                        # Fix, re-review, repeat until passing
roborev comment --job <id> "<msg>"    # Add a comment to a review
roborev address <job_id>              # Mark a review as addressed
```

### Agent Skills

| Skill | Purpose |
| ----- | ------- |
| `/roborev-review` | Request a code review for a specific commit |
| `/roborev-review-branch` | Review all commits on the current branch |
| `/roborev-fix` | Discover and fix all unaddressed review findings |
| `/roborev-address` | Fetch a review and make code changes to address findings |
| `/roborev-respond` | Comment on a review and mark it as addressed |
| `/roborev-design-review` | Request a design review for a commit |
| `/roborev-design-review-branch` | Design review for all commits on current branch |

### Workflow

1. **Commit** — roborev automatically reviews in the background
2. **Check** — `roborev show` or `roborev fix --unaddressed --list` to see findings
3. **Fix** — `/roborev-fix` addresses findings, runs tests, comments, and marks addressed
4. **Refine** — `roborev refine` loops fix-and-review in an isolated worktree until passing

When `roborev fix` cannot automatically resolve a finding, create a backlog task with the `roborev` label and reference the job ID.

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:

- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and finalization
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->
