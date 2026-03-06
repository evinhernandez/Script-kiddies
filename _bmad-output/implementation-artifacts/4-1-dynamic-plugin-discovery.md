# Story 4.1: Dynamic Plugin Discovery

Status: in-progress

## Story

As a Developer,
I want to add a new python file to `src/modules/` and have it automatically appear in `show modules`,
So that I can extend the framework without modifying the core engine code.

## Acceptance Criteria

1. **Given** I create a new directory `src/modules/my_exploit/`
2. **When** I add an `__init__.py` that defines a `BaseModule` subclass
3. **Then** restarting `skconsole` and typing `show modules` reveals the new exploit.

## Tasks / Subtasks

- [ ] Task 1: Refine Plugin Loader
  - [ ] Subtask 1.1: Ensure `src/core/plugin_loader.py` uses `importlib` to walk the directory tree.
  - [ ] Subtask 1.2: Support multi-level categories (e.g., `src/modules/jailbreak/dan.py`).
- [ ] Task 2: Documentation
  - [ ] Subtask 2.1: Create a `MODULE_GUIDE.md` for developers.

## Dev Notes

### Technical Requirements
- Use `pkgutil` or `importlib.util`.

### Architecture Compliance

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
