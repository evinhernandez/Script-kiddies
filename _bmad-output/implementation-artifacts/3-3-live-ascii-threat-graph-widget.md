# Story 3.3: Live ASCII Threat Graph Widget

Status: backlog

## Story

As a Red Teamer,
I want to watch a dynamic tree graph build itself in real-time as the agent attacks,
So that I can visually understand the attack decision path at a glance.

## Acceptance Criteria

1. **Given** the dashboard is running
2. **When** the `AgentDeployer` pivots to a new strategy or receives a target response
3. **Then** the `rich.Tree` widget in the right pane appends a new node
4. **And** colors it Red `[X]` for blocked or Green `[✓]` for success based on the evaluation engine.

## Tasks / Subtasks

- [ ] Task 1: Create Threat Graph Widget
  - [ ] Subtask 1.1: Implement a custom Textual widget wrapping `rich.Tree`.
- [ ] Task 2: Live Updates
  - [ ] Subtask 2.1: Implement a method to append nodes dynamically based on engine events.

## Dev Notes

### Technical Requirements

### Architecture Compliance

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
