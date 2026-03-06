# Story 5.2: Markdown and JSON Export

Status: backlog

## Story

As a Security Auditor,
I want to export my attack results to Markdown and JSON files,
So that I can include them in professional penetration testing reports.

## Acceptance Criteria

1. **Given** an attack has completed in the `skconsole` or headless mode
2. **When** the attack finishes
3. **Then** the framework optionally saves a `.json` and a `.md` file to the `exports/` directory.
4. **And** the Markdown file contains a clean, human-readable summary of the attack path.

## Tasks / Subtasks

- [ ] Task 1: Create Export Directory
  - [ ] Subtask 1.1: Ensure `exports/` directory exists.
- [ ] Task 2: Implement JSON Exporter
  - [ ] Subtask 2.1: Implement `AttackResult.export_json(path)`.
- [ ] Task 3: Implement Markdown Exporter
  - [ ] Subtask 3.1: Create a template for Markdown reports.
  - [ ] Subtask 3.2: Implement `AttackResult.export_markdown(path)`.
- [ ] Task 4: Console Integration
  - [ ] Subtask 4.1: Add `--export` flag to `sk attack` command.

## Dev Notes

### Technical Requirements

### Architecture Compliance

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
