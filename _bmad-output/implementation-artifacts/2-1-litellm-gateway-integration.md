# Story 2.1: LiteLLM Gateway Integration

Status: completed

## Story

As an Agent Deployer Engine,
I want to route all LLM requests through LiteLLM,
So that users can configure OpenAI, Anthropic, or local Ollama models interchangeably.

## Acceptance Criteria

1. **Given** I configure an `ATTACKER_MODEL` in the console (e.g., `gpt-4o`)
2. **When** the `AgentDeployer` class initiates an attack
3. **Then** the request is successfully routed through the `litellm.completion` asynchronous wrapper
4. **And** the engine receives a standard, normalized response object regardless of the underlying provider.

## Tasks / Subtasks

- [x] Task 1: Add LiteLLM Dependency
  - [x] Subtask 1.1: Add `litellm` to `requirements.txt` and `setup.py`.
- [x] Task 2: Refactor `LLMClient`
  - [x] Subtask 2.1: Replace provider-specific logic with `litellm.acompletion`.
  - [x] Subtask 2.2: Ensure `LLMResponse` remains compatible with the rest of the framework.
- [x] Task 3: Verify Integration
  - [x] Subtask 3.1: Run existing tests to ensure no regressions in mock mode.

## Dev Notes

### Technical Requirements
- Use `litellm.acompletion` for async support.
- Handle model name normalization (e.g., `gemini/` prefix for Google).

### Architecture Compliance
- `LLMClient` remains the single point of entry for all LLM interactions.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Refactored `src/utils/llm_client.py` to use `litellm`.
- Maintained `MOCK_RESPONSES` for offline development.

### Completion Notes List

- All LLM calls now go through LiteLLM.
- Successfully verified with `tests/test_execution.py`.

### File List
- `src/utils/llm_client.py`
- `requirements.txt`
- `setup.py`
