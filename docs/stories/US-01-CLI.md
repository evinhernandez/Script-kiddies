# User Story: US-01-CLI
**Title:** Implement the `skconsole` foundational loop.

**As a** Red Teamer,
**I want** an interactive command-line interface,
**So that** I can easily load modules and set target variables without writing custom scripts.

## Acceptance Criteria:
1.  Running `skconsole` drops the user into an interactive prompt (e.g., `sk> `).
2.  Typing `help` shows available commands.
3.  Typing `exit` or `quit` safely exits the program.
4.  User can use `set TARGET <url>` to define a global variable.
5.  Typing `show options` displays currently set variables.

## Technical Notes:
*   Use the standard library `cmd` module for the initial MVP to keep dependencies low, or `prompt_toolkit` if richer auto-complete is desired immediately.
*   Place this in `src/scriptkiddies/cli/console.py`.
*   Ensure the entry point in `pyproject.toml` is mapped correctly (e.g., `skconsole = "scriptkiddies.cli.console:main"`).
