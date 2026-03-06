---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: ['prd.md', 'product-brief-Script-kiddies-2026-03-05.md', 'ux-design-specification.md', 'project-memory/03_architecture.md']
workflowType: 'architecture'
project_name: 'Script-kiddies'
user_name: 'ehernandez'
date: '2026-03-05'
lastStep: 8
status: 'complete'
completedAt: '2026-03-05 13:44:30'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._


## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
The system is divided into two major architectural domains: the `skconsole` (a reactive Terminal UI using `textual`) and the `AgentDeployer` (an asynchronous LLM execution engine). The architecture must support dynamic module loading at runtime without recompilation.

**Non-Functional Requirements:**
High emphasis on Portability (zero heavy C++ dependencies), Reliability (graceful network timeouts and token limits), and Security (strict decoupling of secrets and PII redaction on output).

**Scale & Complexity:**
- Primary domain: CLI Application / Headless Engine
- Complexity level: High (Concurrency, Reactive UI, Multi-turn LLM state)
- Estimated architectural components: 4 core modules (CLI/UI, Core Engine, Plugin Loader, Utilities/Targeting)

### Technical Constraints & Dependencies
- Pure Python implementation relying heavily on `asyncio` to prevent UI thread blocking during network I/O.
- Must use `rich` and `textual` for the UI layer.
- Must use an LLM gateway wrapper (e.g., `litellm`) to ensure local/remote model interoperability.

### Cross-Cutting Concerns Identified
- **Event Bus / Pub-Sub:** A mechanism is required to pipe state changes from the deep backend `AgentDeployer` up to the visual Threat Graph widget without tight coupling.
- **Unified Error Handling:** WAF blocks, LLM timeouts, and parse errors must gracefully degrade into static payload fallbacks rather than raising fatal exceptions.


## Starter Template Evaluation

### Primary Technology Domain
Python CLI Application / Headless API Backend (Brownfield)

### Starter Options Considered
1.  **`textual init` Boilerplate:** The official generator for new Textual apps. (Rejected as a full overwrite because we already have a functional repository structure and `SKEngine`).
2.  **Custom Brownfield Integration:** Adapting the official Textual structural patterns into our existing `src/` directory while keeping our `AgentDeployer` decoupled. (Selected)

### Selected Starter: Custom Brownfield Integration (Textual Standard Pattern)

**Rationale for Selection:**
Since the `Script-kiddies` repository is already initialized with a `setup.py`, core engine logic (`src/core/engine.py`), and a basic CLI entry point, overriding it with a generic template would destroy progress. Instead, we will adopt the official Textual application architecture pattern and inject it into our existing structure.

**Initialization / Structural Pattern:**
```bash
# We will create this structure for the TUI module:
src/cli/tcss/
    dashboard.tcss       # Textual CSS for styling
src/cli/ui/
    app.py               # Main textual.App class
    widgets/             # Custom widgets (ThreatGraph, AgentLog)
```

**Architectural Decisions Provided by this Foundation:**

**Language & Runtime:**
Python 3.11+ leveraging heavy `asyncio` for non-blocking UI rendering.

**Styling Solution:**
Textual CSS (`.tcss`). We will explicitly separate visual styling (colors, layout grids) from Python component logic to keep the codebase clean.

**Build Tooling:**
Maintained via the existing `setup.py` (and potentially migrating to `pyproject.toml` with `hatch` or `poetry` later).

**Testing Framework:**
`pytest`. Textual provides an `app.run_test()` async context manager that allows us to simulate keystrokes and validate the TUI without rendering it to a real terminal.

**Code Organization:**
Strict decoupling. The `textual.App` (in `src/cli/ui/`) will communicate with the `AgentDeployer` (in `src/agents/`) strictly via `asyncio.Queue` or native Textual `Message` events to prevent the LLM network calls from blocking the UI thread.

**Development Experience:**
We will utilize the `textual-dev` CLI (`textual run --dev src/cli/main.py`) to enable live CSS reloading and real-time console debugging during development.


## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- TUI Framework: `textual` (v8.0+) + `rich`
- AI Gateway Library: `litellm` (v1.82+)
- Data Validation/Serialization: `pydantic` (v2.x)
- Async Communication: Textual Native `Message` Event System

**Important Decisions (Shape Architecture):**
- Output Formats: SARIF, Markdown, JSON (powered by Pydantic models)
- Plugin Discovery: Python standard library `importlib` and `pkgutil` for scanning `src/modules/`.

**Deferred Decisions (Post-MVP):**
- Enterprise SSO/Auth integration.
- Web UI Dashboard implementation.

### Data Architecture

- **Data Modeling:** `pydantic` (v2.x)
- **Rationale:** Pydantic provides strict type validation, Rust-backed performance, and automatic JSON schema generation. This is crucial for ensuring the `AttackResult` and `ThreatNode` data structures can be reliably exported to SARIF and JSON without writing manual serializers.
- **Affects:** The core engine, output formatting, and plugin development (module authors must return Pydantic models).

### API & Communication Patterns

- **LLM Gateway:** `litellm` (v1.82.0+)
- **Rationale:** LiteLLM abstracts away the differences between OpenAI, Anthropic, Gemini, and local Ollama models. The `AgentDeployer` only needs to write against the OpenAI-compatible schema, drastically reducing the complexity of supporting new models.
- **Affects:** `AgentDeployer` and the underlying network request logic.

### Frontend (TUI) Architecture

- **UI Framework:** `textual` (v8.0.2)
- **State Management / Communication:** Textual Native `Message` Event System
- **Rationale:** To prevent the TUI from freezing during 30-second LLM network calls, the `AgentDeployer` will run as an asynchronous worker task. As it progresses, it will yield or emit `textual.message.Message` events (e.g., `class AttackFired(Message)`). The UI components (like the Threat Graph) will use `@on(AttackFired)` decorators to reactively update the screen. This ensures the UI remains butter-smooth and responsive to user input (like pressing 'ESC' to cancel) while the attack runs in the background.

### Decision Impact Analysis

**Implementation Sequence:**
1.  **Data Layer:** Define the `BaseModule`, `AttackResult`, and `ThreatNode` Pydantic models.
2.  **Engine Layer:** Build the `AgentDeployer` using `litellm` and `asyncio`.
3.  **UI Foundation:** Scaffold the `textual.App` and the split-pane dashboard.
4.  **Integration:** Wire the `AgentDeployer` to the `textual` Message bus so the Threat Graph updates dynamically.

**Cross-Component Dependencies:**
- The **UI Layer** is entirely dependent on the **Data Layer** (Pydantic models) to render correctly. The `textual` widgets should receive complete Pydantic objects, not raw dictionaries.
- The **Plugin Modules** must strictly return the defined Pydantic `AttackResult` so the UI doesn't crash trying to parse unexpected data.


## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:**
3 areas where AI agents could make different choices (Structure, Naming, Logging).

### Naming Patterns

**Code Naming Conventions:**
- **Classes:** PascalCase. All exploit modules MUST end with `Module` (e.g., `RAGPoisoningModule`). All Textual widgets MUST end with `Widget` (e.g., `ThreatGraphWidget`).
- **Files/Modules:** snake_case. (e.g., `rag_poisoning.py`).
- **Pydantic Models:** All properties MUST use `snake_case` (e.g., `payload_used`, not `payloadUsed`).

### Structure Patterns

**Project Organization:**
Strict Domain-Driven separation within the `src/` directory:
- `src/cli/`: Strictly for the `textual` App, UI widgets, and `cmd` REPL logic. No LLM execution logic here.
- `src/core/`: Strictly for the `AgentDeployer`, `BaseModule`, and `Target` network connection logic. No UI rendering logic here.
- `src/modules/`: Strictly for the standalone exploit classes that inherit from `BaseModule`.

### Communication Patterns

**Event System Patterns:**
- **Textual Messages:** The core engine will yield state objects. The `textual` App will wrap these in `textual.message.Message` classes. Message classes must follow the naming convention `[Noun][PastTenseVerb]` (e.g., `AttackStarted`, `PayloadSent`, `GoalAchieved`).

### Process Patterns

**Error Handling & Logging Patterns:**
- **NO PRINT STATEMENTS:** AI Agents are explicitly forbidden from using standard `print()` statements anywhere in the codebase. Using `print()` will break the `textual` TUI renderer.
- **Structured Logging:** All `AgentDeployer` and network logic must use `structlog` (which is already in the project dependencies). The UI layer will subscribe to the `structlog` output to render the 'Agent Thoughts' pane.

### Enforcement Guidelines

**All AI Agents MUST:**
- Run `ruff check --fix` and `black` before committing any python code.
- Ensure all new exploit modules inherit from `src.core.engine.BaseModule`.
- Never use `print()`.

**Anti-Patterns (What to Avoid):**
- **Avoid:** Writing LLM prompting logic directly inside a `textual` Widget class.
- **Avoid:** Using `camelCase` in Python variables or Pydantic fields.


## Project Structure & Boundaries

### Complete Project Directory Structure
```text
Script-kiddies/
├── setup.py                  # Package configuration & entry points
├── pyproject.toml            # Build system & formatting tools (ruff/black)
├── requirements.txt          # Production dependencies (textual, litellm, pydantic)
├── requirements-dev.txt      # Development dependencies (pytest)
├── README.md
├── docs/                     # General documentation
├── project-memory/           # BMAD Project Memory & Sprints
├── _bmad-output/             # BMAD Planning Artifacts
├── src/
│   ├── __init__.py
│   ├── cli/                  # UI and Command Line Interface
│   │   ├── __init__.py
│   │   ├── main.py           # Entry point for `sk` command
│   │   ├── console.py        # `prompt_toolkit` / `cmd` REPL for `skconsole`
│   │   ├── app.py            # `textual` App instantiation
│   │   ├── tcss/             # Textual CSS styling
│   │   │   └── dashboard.tcss
│   │   └── widgets/          # Custom UI components
│   │       ├── __init__.py
│   │       ├── threat_graph.py
│   │       └── agent_log.py
│   ├── core/                 # Core Engine & Framework Logic
│   │   ├── __init__.py
│   │   ├── engine.py         # Module loader and execution router
│   │   ├── target.py         # Network target abstraction
│   │   └── models.py         # Pydantic schemas (AttackResult, ThreatNode)
│   ├── agents/               # Autonomous LLM Engine
│   │   ├── __init__.py
│   │   └── deployer.py       # `AgentDeployer` class (LiteLLM async loop)
│   └── modules/              # Exploit Plugins
│       ├── __init__.py
│       ├── base.py           # `BaseModule` abstract class
│       └── prompt_injection/
│           ├── __init__.py
│           └── agentic_extraction.py
└── tests/
    ├── conftest.py
    ├── cli/
    ├── core/
    └── modules/
```

### Architectural Boundaries

**API Boundaries:**
- The `AgentDeployer` is the ONLY component authorized to make external LLM API calls via `litellm`.
- The `Target` class is the ONLY component authorized to make external HTTP requests to the system under test.

**Component Boundaries:**
- **UI to Engine:** The `textual.App` (UI) invokes the `AgentDeployer` via an `asyncio.create_task` wrapper.
- **Engine to UI:** The `AgentDeployer` yields `textual.message.Message` events. The UI strictly listens to these events; the UI never polls the engine synchronously.

**Data Boundaries:**
- All data passed between `src/modules/`, `src/core/`, and `src/cli/` MUST be strongly typed `pydantic` models defined in `src/core/models.py`. Raw dictionaries are strictly prohibited at the boundary layer.

### Requirements to Structure Mapping

**Feature/Epic Mapping:**
- **Cinematic TUI (FR1-7):** `src/cli/`
- **Metasploit Loop (FR8-11):** `src/cli/console.py`
- **Autonomous Engine (FR19-23):** `src/agents/deployer.py`
- **Dynamic Plugin Loader (FR12):** `src/core/engine.py` scanning `src/modules/`

**Cross-Cutting Concerns:**
- **Structured Logging (NFR7):** Implemented globally using `structlog`, instantiated in `src/cli/main.py` and utilized throughout `src/core/` and `src/agents/`.
- **Target Authentication (FR14-17):** Handled by `src/core/target.py` and passed down from the `skconsole` state.


## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
The selection of `textual`, `litellm`, and `pydantic` forms a highly cohesive stack. `textual` natively supports asynchronous execution, mapping perfectly to `litellm`'s async wrappers, allowing the `AgentDeployer` to run without blocking the UI rendering loop.

**Pattern Consistency:**
The strict Domain-Driven folder structure (`src/cli`, `src/core`, `src/modules`) directly supports the architectural decision to decouple the Engine from the UI, ensuring that AI Agents don't accidentally leak `rich` styling logic into the deep backend targets.

**Structure Alignment:**
The project tree explicitly reserves space for the `textual` CSS (`.tcss`) and defines the clear boundaries needed for dynamic module loading.

### Requirements Coverage Validation ✅

**Epic/Feature Coverage:**
The Cinematic TUI is covered by the `textual` architecture, the Autonomous Loop is covered by the decoupled `AgentDeployer` utilizing `litellm`, and the "Holy F***" moment is enabled by the `rich.tree` dynamic event streaming.

**Functional Requirements Coverage:**
All 31 FRs from the PRD are architecturally supported. The dynamic plugin loader (FR12) is explicitly handled in `src/core/engine.py`, and the Metasploit loop (FR8-11) is mapped to `src/cli/console.py`.

**Non-Functional Requirements Coverage:**
The "Drink Our Own Champagne" security NFRs are supported by the use of strict `pydantic` models and the explicit ban on `print()` in favor of `structlog` (ensuring credentials aren't accidentally flushed to stdout).

### Implementation Readiness Validation ✅

**Decision Completeness:**
All critical libraries have exact, latest stable versions defined (`textual 8.0.2`, `litellm 1.82.0`).

**Structure Completeness:**
A full directory tree has been mapped with explicit file purposes defined.

**Pattern Completeness:**
The specific rules around naming (PascalCase for classes, snake_case for modules/models) and the absolute ban on `print()` give the developer agents (like Claude or Codex) unambiguous guidelines.

### Gap Analysis Results

**Nice-to-Have Gaps:**
- While `structlog` is chosen, the exact JSON formatting structure for the exported logs isn't fully schema'd out yet. This will be handled during the Epic creation phase when the Pydantic models are actually written.

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**✅ Architectural Decisions**
- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**✅ Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**✅ Project Structure**
- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** HIGH based on the maturity of the `textual` framework and strict isolation patterns.

**Key Strengths:**
- Unambiguous decoupling of the visual layer from the network execution layer.
- Future-proofed AI integration by using `litellm` instead of locking into OpenAI SDK directly.

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented.
- Use implementation patterns consistently across all components.
- Respect project structure and boundaries.
- Refer to this document for all architectural questions.
