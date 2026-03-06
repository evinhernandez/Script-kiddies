# Story 4.2: Headless CLI Execution Mode

Status: backlog

## Story

As an Automation Script,
I want to run `sk attack prompt_injection --target google`,
So that I can integrate SK Framework into CI/CD pipelines without human interaction.

## Acceptance Criteria

1. **Given** I am in a standard bash terminal
2. **When** I run `sk attack <module> [options]`
3. **Then** the framework executes the attack using the Click-based CLI (not the REPL)
4. **And** prints the final JSON result to stdout.

## Tasks / Subtasks

- [ ] Task 1: Expand Click CLI
  - [ ] Subtask 1.1: Update `src/cli/main.py` to include the `attack` command.
  - [ ] Subtask 1.2: Implement argument parsing for module options (e.g., `--target`, `--payload`).
- [ ] Task 2: Non-Interactive Engine Runner
  - [ ] Subtask 2.1: Create a runner that bypasses the TUI and prints results to terminal.

## Dev Notes

### Technical Requirements
- Click's `command` and `option` decorators.

### Architecture Compliance

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
