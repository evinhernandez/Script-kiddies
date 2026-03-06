# Product Requirements Document (PRD)

## 1. Core Workflows
### The Red Team Loop
1. User starts `skconsole`.
2. User types `show modules` and selects one (`use exploit/llm/prompt_injection/extract_system_prompt`).
3. User configures the module (`set TARGET http://localhost:8000/chat`).
4. User executes (`run`).
5. The framework instantiates an Attacker Agent via `AgentDeployer`.
6. The Agent interacts with the TARGET dynamically until the goal is met or max iterations are reached.
7. Results are logged and presented to the user.

## 2. Functional Requirements
*   **CLI Interface:** Must support auto-complete for commands (`use`, `set`, `show`, `run`, `exit`).
*   **Target Interface:** Must support generic HTTP/JSON endpoints that accept text and return text.
*   **LLM Integration:** Must use `litellm` (or similar) so red teamers can use local (Ollama) or remote (OpenAI/Anthropic) models as the Attacker Agent.
*   **Module System:** Exploit modules must be easy to author (just a Python class inheriting from `BaseExploit`).

## 3. Non-Functional Requirements
*   **Extensibility:** Adding a new module should require no core framework changes.
*   **Zero-Config Start:** A default attacker model should be configurable via env vars.
