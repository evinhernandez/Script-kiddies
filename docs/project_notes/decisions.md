# Architectural Decisions (ADRs)

### ADR-001: Standardized LLM Routing with LiteLLM (2026-03-06)
**Context**: We need to support multiple LLM providers (OpenAI, Anthropic, Gemini, local Ollama) without writing custom wrappers for every new model.
**Decision**: Adopt `litellm` as the core routing gateway in `LLMClient`.
**Consequences**: 
- ✅ Unified request/response format.
- ✅ Support for 100+ models with zero code changes.
- ✅ Simplified async handling.

### ADR-002: TUI Framework Choice: Textual (2026-03-06)
**Context**: The framework needs a "cinematic" dashboard for real-time monitoring of autonomous attacks.
**Decision**: Use `textual` for the terminal user interface.
**Consequences**:
- ✅ Rich, multi-pane layouts with CSS-like styling.
- ✅ Async event-driven architecture fits perfectly with LLM calls.
- ✅ Built-in worker support for background engine execution.

### ADR-003: Data Boundaries with Pydantic v2 (2026-03-06)
**Context**: Attack results and module metadata need to be easily serializable for reporting and persistence.
**Decision**: Convert all core data structures to Pydantic `BaseModel` classes.
**Consequences**:
- ✅ Guaranteed runtime type safety.
- ✅ One-line JSON serialization (`model_dump_json`).
- ✅ Clean interface between the Engine, Console, and TUI layers.

### ADR-004: Hierarchical Module Structure (2026-03-07)
**Context**: As the exploit library grows, a flat structure becomes difficult to navigate and maintain.
**Decision**: Adopt a filesystem-based hierarchical structure (`category/subcategory/technique.py`) and auto-generate canonical dotted names.
**Consequences**:
- ✅ Intuitive navigation via Tree-based module browser.
- ✅ Simplified module creation: "New File = New Categorized Exploit".
- ✅ Support for granular technique selection (e.g., `injection.direct.roleplay`).

### ADR-005: Interactive Post-Exploitation Shell (2026-03-07)
**Context**: Red teamers need to follow up successful jailbreaks with manual probing.
**Decision**: Implement a `SESSION_SHELL` within the dashboard that persists the compromised context.
**Consequences**:
- ✅ Real-time interaction with cracked models.
- ✅ Lateral movement support via `/run <module>` within the same session.
- ✅ Eliminates the need to restart the entire attack chain for follow-up questions.
