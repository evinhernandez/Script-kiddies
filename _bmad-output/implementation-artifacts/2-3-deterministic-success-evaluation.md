# Story 2.3: Deterministic Success Evaluation

Status: completed

## Story

As a Red Teamer,
I want the engine to independently verify if an attack succeeded by searching for a leaked secret,
So that I don't have to rely on the Attacker LLM hallucinating its own success.

## Acceptance Criteria

1. **Given** an autonomous attack loop is running
2. **When** the target responds
3. **Then** the `AgentDeployer` checks the response string against a predefined expected regex or secret (e.g., 'SK-ALPHA-99')
4. **And** immediately halts the loop and flags 'SUCCESS' if the string is found.

## Tasks / Subtasks

- [x] Task 1: Update `AgentDeployer` Success Detection
  - [x] Subtask 1.1: Support passing `expected_flag` to `deploy()`.
  - [x] Subtask 1.2: Ensure loop terminates immediately upon deterministic success.
- [x] Task 2: Update Module Options
  - [x] Subtask 2.1: Add `EXPECTED_FLAG` option to relevant modules.

## Dev Notes

### Technical Requirements
- Refactored `ScoringEngine` to support literal `expected_flag` matching.
- Immediate termination of `AgentDeployer` loop upon success.

### Architecture Compliance
- Logic is maintained within `ScoringEngine` for consistency.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Fixed `FLAG_PATTERN` limitation by adding literal check.

### Completion Notes List

- Deterministic success verified via `tests/test_agentic.py`.

### File List
- `src/utils/scoring.py`
- `src/agents/deployer.py`
- `src/modules/system_prompt_extraction/__init__.py`
- `tests/test_agentic.py`
