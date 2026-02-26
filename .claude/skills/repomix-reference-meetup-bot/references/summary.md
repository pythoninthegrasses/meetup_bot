This file is a merged representation of a subset of the codebase, containing specifically included files and files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where comments have been removed, content has been compressed (code blocks are separated by ⋮---- delimiter).

# Summary

## Purpose

This is a reference codebase organized into multiple files for AI consumption.
It is designed to be easily searchable using grep and other text-based tools.

## File Structure

This skill contains the following reference files:

| File | Contents |
|------|----------|
| `project-structure.md` | Directory tree with line counts per file |
| `files.md` | All file contents (search with `## File: <path>`) |
| `tech-stack.md` | Languages, frameworks, and dependencies |
| `summary.md` | This file - purpose and format explanation |

## Usage Guidelines

- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes

- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/*
- Files matching these patterns are excluded: **/.env, **/.key, **/.pem, **/*.pxd, backlog/**, docs/**, tests/**, .coverage, .claude, .editorconfig, .gitignore, .markdownlint.jsonc, .serena, .vscode, AGENTS.md, CLAUDE.local.md, CLAUDE.md, coverage.json, LICENSE, repomix.config.json5, requirements.txt, uv.lock
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Code comments have been removed from supported file types
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

## Statistics

60 files | 6,581 lines

| Language | Files | Lines |
|----------|------:|------:|
| YAML | 12 | 781 |
| Python | 10 | 748 |
| No Extension | 8 | 222 |
| Markdown | 6 | 381 |
| JSON | 5 | 117 |
| TOML | 4 | 2,790 |
| Shell | 3 | 154 |
| CSV | 2 | 24 |
| Text | 2 | 18 |
| HTML | 1 | 32 |
| Other | 7 | 1,314 |

**Largest files:**
- `gitleaks.toml` (2,618 lines)
- `devbox.lock` (886 lines)
- `app/main.py` (193 lines)
- `README.md` (185 lines)
- `app/meetup_query.py` (181 lines)
- `app/meetup_queries.gql` (147 lines)
- `taskfiles/deno.yml` (134 lines)
- `Makefile` (118 lines)
- `app/schedule.py` (113 lines)
- `taskfiles/docker.yml` (113 lines)