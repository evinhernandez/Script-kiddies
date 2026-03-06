# Story 1.1: Core CLI Scaffold and REPL Loop

Status: completed

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Red Teamer,
I want to launch the `skconsole` and enter an interactive REPL loop,
so that I can interact with the framework without writing standalone python scripts.

## Acceptance Criteria

1. **Given** I have installed the framework via `pip install -e .`
2. **When** I type `skconsole` in my terminal
3. **Then** I am presented with an ASCII welcome screen
4. **And** dropped into an interactive prompt (`sk>`) that supports basic `exit` and `help` commands.

## Tasks / Subtasks

- [x] Task 1: Initialize REPL Environment (AC: 1, 2)
  - [x] Subtask 1.1: Verify `setup.py` entry points map `skconsole` to `src.cli.console:main`.
  - [x] Subtask 1.2: Refactor existing `src/cli/console.py` to use standard `cmd` or `prompt_toolkit` if needed.
- [x] Task 2: Implement ASCII Welcome Screen (AC: 3)
  - [x] Subtask 2.1: Integrate `rich` to print a stylized Matrix-themed ASCII banner upon REPL initialization.
- [x] Task 3: Core Commands (AC: 4)
  - [x] Subtask 3.1: Implement `help` command to list available REPL commands.
  - [x] Subtask 3.2: Implement `exit` and `quit` to safely shut down the prompt.

## Dev Notes

### Technical Requirements
- **NO PRINT STATEMENTS:** Used `rich.console.Console` for all output.
- **Language/Runtime:** Python 3.11+.

### Architecture Compliance
- The REPL logic lives exclusively in `src/cli/console.py`.
- Integrated `rich` for all terminal interactions.
- Resolved `pydantic` v2 migration issues and naming conflicts in the core framework.

### Project Structure Notes
- Changes isolated to `src/cli/console.py`, `src/core/config.py`, `src/utils/logger.py`, and `setup.py`.

### References
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 1]
- [Source: _bmad-output/planning-artifacts/architecture.md#Implementation Patterns & Consistency Rules]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Fixed `pydantic.errors.PydanticImportError` for `BaseSettings`.
- Fixed `TypeError: PrintLogger.msg() got an unexpected keyword argument 'extra'` in `structlog`.
- Renamed `AttackResult` enum in `src/utils/scoring.py` to `ScoringStatus` to resolve conflict with `src/core/engine.py:AttackResult` dataclass.

### Completion Notes List

- `skconsole` now features a stylized Matrix-green ASCII banner.
- All commands use `rich` Tables and Panels for clean, professional output.
- Core loop verified with unit tests in `tests/test_console.py`.

### File List
- `src/cli/console.py`
- `src/core/config.py`
- `src/utils/logger.py`
- `src/agents/deployer.py`
- `setup.py`
- `requirements.txt`
- `tests/test_console.py`
- `tests/test_suite.py`
