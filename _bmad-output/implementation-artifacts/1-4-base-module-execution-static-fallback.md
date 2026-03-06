# Story 1.4: Base Module Execution (Static Fallback)

Status: completed

## Story

As a Red Teamer,
I want to type `run` to execute a loaded module against my configured target,
So that I can test basic, static payload injections against an endpoint.

## Acceptance Criteria

1. **Given** I have set a valid TARGET and loaded a basic prompt injection module
2. **When** I type `run`
3. **Then** the `BaseModule.run()` method executes, sending an HTTP request to the target
4. **And** the raw response is printed to the console (pre-textual dashboard implementation).

## Tasks / Subtasks

- [x] Task 1: Implement LLM Mocking for Offline Development
  - [x] Subtask 1.1: Update `LLMClient` to handle missing API keys gracefully by returning mock responses.
- [x] Task 2: Refine Scoring Engine
  - [x] Subtask 2.1: Add `CRITICAL_SUCCESS_PATTERNS` to `ScoringEngine` for high-confidence detection of successful attacks (e.g., "pwned").
- [x] Task 3: Verify End-to-End Execution
  - [x] Subtask 3.1: Create `tests/test_execution.py` to verify full integration from Engine to Module to Scorer.
- [x] Task 4: Console Output Integration
  - [x] Subtask 4.1: Ensure `do_run` in `SKConsole` displays results clearly using `rich.Panel`.

## Dev Notes

### Technical Requirements
- Execution must handle multiple payloads if no specific payload is set.
- Mocking ensures the framework is usable in development environments without external connectivity.

### Architecture Compliance
- `BaseModule` orchestration is verified.
- `SKEngine.run_module` correctly bridges the console and the exploit logic.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Fixed `ScoringStatus.PARTIAL` issue by introducing `CRITICAL_SUCCESS_PATTERNS`.
- Verified mock responses trigger correctly in absence of API keys.

### Completion Notes List

- `run` command is fully functional for static modules.
- Users see a professional summary panel after execution.

### File List
- `src/utils/llm_client.py`
- `src/utils/scoring.py`
- `src/cli/console.py`
- `tests/test_execution.py`
