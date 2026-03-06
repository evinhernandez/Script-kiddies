# Story 1.2: Module Loading and Introspection

Status: completed

## Story

As a Red Teamer,
I want to use the `use` command to load an exploit module and view its options,
So that I know what parameters I need to configure before attacking.

## Acceptance Criteria

1. **Given** I am in the `skconsole` prompt
2. **When** I type `use prompt_injection`
3. **Then** the prompt changes to reflect the loaded module context (`sk([bold red]prompt_injection[/bold red])> `)
4. **And** typing `show options` displays a table of required parameters (e.g., TARGET, PAYLOAD).

## Tasks / Subtasks

- [x] Task 1: Define Module Option Schema
  - [x] Subtask 1.1: Add `ModuleOption` dataclass to `src/core/engine.py`.
  - [x] Subtask 1.2: Add `get_options()` method to `BaseModule`.
- [x] Task 2: Implement Options in Prompt Injection Module
  - [x] Subtask 2.1: Implement `get_options()` in `PromptInjectionModule` returning TARGET, MODEL, PAYLOAD, and SYSTEM_PROMPT.
- [x] Task 3: Update Console Introspection
  - [x] Subtask 3.1: Update `do_use` to store the module instance.
  - [x] Subtask 3.2: Update `do_show options` to render module-specific options using `rich.Table`.

## Dev Notes

### Technical Requirements
- Modules must be able to declare their own requirements.
- The console must dynamically adapt based on the loaded module.

### Architecture Compliance
- `BaseModule` now provides a standard interface for options.
- `SKConsole` uses this interface to provide transparency to the user.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Added `ModuleOption` to `src/core/engine.py`.
- Updated `SKConsole.do_show` to handle split display of Global vs Module options.

### Completion Notes List

- Prompt correctly reflects loaded module.
- `show options` provides clear required/default visibility for module parameters.

### File List
- `src/core/engine.py`
- `src/modules/prompt_injection/__init__.py`
- `src/cli/console.py`
- `tests/test_console.py`
