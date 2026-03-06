# Story 1.3: Target Configuration State Management

Status: completed

## Story

As a Red Teamer,
I want to set global and module-specific variables (like TARGET URLs and Auth Tokens),
So that the exploit engine knows where to direct its attacks.

## Acceptance Criteria

1. **Given** I have a module loaded in `skconsole`
2. **When** I type `set TARGET http://localhost:8000/api`
3. **Then** the framework saves that URL into its active session state
4. **And** subsequent `show options` commands reflect the updated TARGET value.

## Tasks / Subtasks

- [x] Task 1: Implement State Storage in Console
  - [x] Subtask 1.1: Add `module_vars` dictionary to `SKConsole`.
  - [x] Subtask 1.2: Ensure `module_vars` is reset when a new module is loaded.
- [x] Task 2: Enhance `set` Command
  - [x] Subtask 2.1: Update `do_set` to check if a variable is module-specific before falling back to global state.
  - [x] Subtask 2.2: Add feedback indicating if a variable was set globally or for the specific module.
- [x] Task 3: Enhance `show options` Command
  - [x] Subtask 3.1: Update `do_show` to reflect currently set values from `module_vars` or `global_vars`.
- [x] Task 4: Propagate State to Execution
  - [x] Subtask 4.1: Update `do_run` to resolve execution parameters using the session state.

## Dev Notes

### Technical Requirements
- Variables are scoped: Module-specific variables override global variables.
- `SKConsole` acts as the transient state manager for the active session.

### Architecture Compliance
- State management is kept simple and isolated within the console layer for now.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Implemented hierarchical variable resolution: `module_vars` -> `global_vars` -> `module.default`.

### Completion Notes List

- User can now configure specific modules without affecting global defaults.
- `show options` provides an accurate view of what will be used during `run`.

### File List
- `src/cli/console.py`
- `tests/test_console.py`
