# Story 2.2: Autonomous Multi-Turn Execution Loop

Status: completed

## Story

As a Red Teamer,
I want the exploit module to use an LLM to dynamically generate payloads based on previous target responses,
So that the attack adapts to basic WAFs or guardrails automatically.

## Acceptance Criteria

1. **Given** I run an agentic exploit module
2. **When** the target rejects the first payload
3. **Then** the `AgentDeployer` feeds the rejection back into the Attacker LLM context
4. **And** generates a new, modified payload for a second attempt
5. **And** halts if the `max_turns` (default 5) limit is reached to prevent runaway costs.

## Tasks / Subtasks

- [x] Task 1: Refine `AgentDeployer` Loop
  - [x] Subtask 1.1: Ensure `chat_history` correctly accumulates interactions.
  - [x] Subtask 1.2: Implement `max_turns` enforcement.
- [x] Task 2: Add Real-time Logging
  - [x] Subtask 2.1: Add structured logging for each turn.
- [x] Task 3: Test Multi-turn logic
  - [x] Subtask 3.1: Create a mock test case where success is only achieved on the second turn.

## Dev Notes

### Technical Requirements
- `AgentDeployer` manages the conversation state between the Attacker LLM and the Target.
- Structured logging provides transparency during multi-turn loops.

### Architecture Compliance
- Agent logic is cleanly isolated in `src/agents/deployer.py`.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

- Verified `chat_history` is passed back to the Attacker LLM.
- Confirmed `max_turns` terminates the loop.

### Completion Notes List

- Autonomous loop is fully functional.
- Verified with `tests/test_agentic.py`.

### File List
- `src/agents/deployer.py`
- `tests/test_agentic.py`
