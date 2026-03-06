# Story 3.1: Textual App Foundation and Split-Pane Layout

Status: in-progress

## Story

As a Red Teamer,
I want the execution phase to launch into a multi-pane terminal dashboard,
So that I can view target status, agent thoughts, and threat trees simultaneously without terminal scrolling clutter.

## Acceptance Criteria

1. **Given** I am in `skconsole`
2. **When** I type `run`
3. **Then** the application instantiates a full-screen `textual.App` overriding the standard REPL
4. **And** the screen is divided into 3 distinct bordered panes (Status, Logs, Threat Graph).

## Tasks / Subtasks

- [ ] Task 1: Initialize TUI Directory
  - [ ] Subtask 1.1: Create `src/cli/ui` directory.
  - [ ] Subtask 1.2: Create `app.py` defining the `SKDashboard` class.
- [ ] Task 2: Implement Layout
  - [ ] Subtask 2.1: Define a 3-pane layout (Header, Left: Status, Middle: Logs, Right: Threat Graph, Footer).
  - [ ] Subtask 2.2: Apply "Cyber-Operator" styling (Neon Cyan borders).
- [ ] Task 3: Integration with Console
  - [ ] Subtask 3.1: Update `SKConsole.do_run` to launch the `SKDashboard`.

## Dev Notes

### Technical Requirements
- Use `textual.containers` for the layout.
- Use `textual.widgets` for the individual panes.

### Architecture Compliance
- TUI must be keyboard navigable.

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
