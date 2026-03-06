# Story 3.2: Async Event Bus (Engine to UI Communication)

Status: backlog

## Story

As the TUI Dashboard,
I want to receive real-time state updates from the `AgentDeployer` without blocking the main rendering thread,
So that the UI remains highly responsive while the LLM makes 10-second API calls.

## Acceptance Criteria

1. **Given** the `textual` dashboard is active and the `AgentDeployer` is running in a background task
2. **When** the agent fires a payload
3. **Then** the engine yields a `PayloadFired` Textual Message
4. **And** the TUI intercepts that message and updates the Agent Logs pane instantly.

## Tasks / Subtasks

- [ ] Task 1: Define Event Schema
  - [ ] Subtask 1.1: Define `AttackFired`, `TargetResponded`, and `ScoreCalculated` messages.
- [ ] Task 2: Instrument Engine
  - [ ] Subtask 2.1: Update `AgentDeployer` to emit events via a callback or event bus.
- [ ] Task 3: Update TUI Handlers
  - [ ] Subtask 3.1: Implement message handlers in `SKDashboard` to update UI components.

## Dev Notes

### Technical Requirements
- Avoid thread-safety issues by using Textual's async message handling.

### Architecture Compliance

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
