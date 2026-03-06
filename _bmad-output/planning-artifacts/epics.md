---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ['prd.md', 'architecture.md', 'ux-design-specification.md']
---

# Script-kiddies - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Script-kiddies, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Users can launch an interactive command-line interface (`skconsole`).
FR2: Users can view a dynamic, animated ASCII welcome screen upon launch.
FR3: Users can view an interactive menu categorized by exploits, vulnerabilities, and checks.
FR4: Users can toggle different TUI verbosity levels and pane layouts (e.g., EDR trace view vs. summary view).
FR5: Users can view a real-time ASCII threat graph that visually branches based on the `AgentDeployer`'s decision tree.
FR6: Users can view a live "Token Spend" counter during autonomous attacks.
FR7: Users can view gamified failure messages (e.g., hacker movie quotes) when an attack fails.
FR8: Users can load specific exploit modules using the `use [module_name]` command.
FR9: Users can view module options using the `show options` command.
FR10: Users can set target URLs and configuration variables using the `set [variable] [value]` command.
FR11: Users can execute the loaded module against the configured target using the `run` command.
FR12: The system can dynamically discover and load new exploit modules dropped into the `src/modules/` directory without code recompilation.
FR13: Users can execute the framework in a "rapid validation" mode via a single CLI command bypassing the interactive prompt.
FR14: Users can input target definitions directly via URL.
FR15: Users can load a list of multiple targets from a designated local directory or file.
FR16: Users can provide target authentication credentials via an interactive prompt.
FR17: Users can load target authentication credentials from a local secrets file.
FR18: The system can connect to both local inference engines (Ollama) and commercial APIs (OpenAI, Anthropic).
FR19: The system can deploy an LLM-driven attacker agent instructed with a specific objective.
FR20: The system can engage the target in a multi-turn, adaptive execution loop based on the target's responses.
FR21: The system can stream verbose, narrative logging of the agent's actions to the TUI.
FR22: The system will automatically terminate the autonomous loop if the `max_turns` limit is reached.
FR23: The system will automatically fallback to injecting static OWASP Top 10 payloads if the autonomous agent errors or times out.
FR24: The system can evaluate attack success deterministically by checking target output for a known injected secret.
FR25: The system can evaluate attack success probabilistically using an independent local "Judge Model".
FR26: The system will sanitize or redact identified sensitive data from the terminal output and logs.
FR27: Users can capture a snapshot of the current TUI state using an export command.
FR28: Users can export attack results and threat graph data in JSON format.
FR29: Users can export attack results in Markdown format for human-readable reporting.
FR30: Users can export attack results in SARIF format for CI/CD integration.
FR31: Users can pipe the raw output of the engine to standard stdout.

### NonFunctional Requirements

NFR1: The system must never log target API keys or Bearer tokens to standard output or log files in plain text.
NFR2: The system must utilize a redaction module to scrub identified sensitive data before saving export reports to disk.
NFR3: The framework codebase must adhere to OWASP Top 10 for LLM Applications and pass automated security linting (Bandit, Semgrep) before main branch deployment.
NFR4: The project must generate and maintain a Software Bill of Materials (SBOM) for all releases.
NFR5: The `AgentDeployer` must enforce a configurable network timeout (default: 30 seconds) per LLM call. If exceeded, it must fail gracefully without crashing the `skconsole` loop.
NFR6: The system must enforce a hardcoded maximum token limit per attack session (e.g., 10,000 tokens) to prevent API cost runaway.
NFR7: The system must provide actionable, verbose error logging in a debug pane to differentiate between WAF blocks (HTTP 403) and LLM hallucinations.
NFR8: The framework must install and execute successfully via `pip` on standard distributions of Linux (Kali Linux, Ubuntu), macOS (M-series and Intel), and Windows (WSL2).
NFR9: The core framework installation must not require C++ build tools or massive machine learning tensor libraries (e.g., PyTorch) to function.

### Additional Requirements

### From Architecture
- Starter Template/Base: Custom Brownfield Integration (Textual Standard Pattern). The project exists, but the TUI must be built inside `src/cli/ui` using `textual.App`.
- Core Communication: The `AgentDeployer` must run asynchronously and emit `textual.message.Message` events (e.g., `AttackFired`).
- Data Boundary: All data passed between modules MUST use Pydantic models (`AttackResult`, `ThreatNode`).
- Dependency Rule: No heavy native C++ ML dependencies. Use `litellm` for LLM gateway routing.

### From UX Design
- TUI Constraints: Must be 100% keyboard navigable and degrade gracefully on <80 col SSH windows.
- TUI Layout: Split-pane dashboard displaying Target Status, Agent Thoughts stream, and Live ASCII Threat Graph.
- Aesthetic: "Cyber-Operator" theme. True Black background, Slate Gray inactive borders, Neon Cyan active borders, Hacker Green for success, Alert Red for failure.
- Export Feature: A global hotkey (Ctrl+E) must instantly dump the threat graph and logs to a sanitized Markdown/SARIF file.


### FR Coverage Map


FR1: Epic 1 - Launch interactive CLI (`skconsole`)
FR2: Epic 1 - ASCII welcome screen
FR3: Epic 1 - Interactive menu
FR4: Epic 3 - Toggle TUI verbosity and pane layouts
FR5: Epic 3 - Real-time ASCII threat graph
FR6: Epic 3 - Live 'Token Spend' counter
FR7: Epic 3 - Gamified failure messages
FR8: Epic 1 - Load exploit modules
FR9: Epic 1 - View module options
FR10: Epic 1 - Set target configuration variables
FR11: Epic 1 - Execute loaded module
FR12: Epic 4 - Dynamic plugin discovery
FR13: Epic 4 - Rapid validation mode
FR14: Epic 1 - Input target URL
FR15: Epic 1 - Load multiple targets
FR16: Epic 1 - Interactive target authentication
FR17: Epic 1 - Secrets file authentication
FR18: Epic 2 - Local and commercial inference connections
FR19: Epic 2 - Deploy LLM attacker agent
FR20: Epic 2 - Multi-turn adaptive execution loop
FR21: Epic 3 - Stream verbose agent logging to TUI
FR22: Epic 2 - Terminate loop at max_turns
FR23: Epic 1 - Static payload fallback
FR24: Epic 2 - Deterministic success evaluation
FR25: Epic 2 - Probabilistic success evaluation (Judge model)
FR26: Epic 5 - Data sanitization/redaction
FR27: Epic 5 - Capture TUI state/evidence
FR28: Epic 5 - JSON export
FR29: Epic 5 - Markdown export
FR30: Epic 5 - SARIF export
FR31: Epic 5 - Raw stdout piping


## Epic List


### Epic 1: The Metasploit Foundation (Interactive CLI & Target Config)
A Red Teamer can launch the `skconsole`, navigate the welcome screen, load an exploit module, set target variables (including auth), and execute a basic (static) attack.
**FRs covered:** FR1, FR2, FR3, FR8, FR9, FR10, FR11, FR14, FR15, FR16, FR17, FR23

### Epic 2: The Autonomous Agent Engine (LLM Execution Loop)
The framework can now deploy an autonomous LLM attacker that intelligently adapts its payloads over multiple turns against a target, rather than just sending static strings.
**FRs covered:** FR18, FR19, FR20, FR22, FR24, FR25

### Epic 3: The Cinematic Dashboard (Real-Time TUI)
When a user types `run`, the standard prompt vanishes and is replaced by a visually stunning, split-pane dashboard featuring a live ASCII threat graph and cascading agent logs.
**FRs covered:** FR4, FR5, FR6, FR7, FR21

### Epic 4: The Vibe Coder Experience & Extensibility
Indie developers can run the tool in a single command for rapid validation, and security researchers can drop new exploit python files into a folder to instantly extend the framework.
**FRs covered:** FR12, FR13

### Epic 5: Evidence Capture & Compliance Export
Enterprise Pentesters can sanitize their terminal output to remove PII and export their attack paths into JSON, Markdown, or SARIF formats for SOC2 reporting.
**FRs covered:** FR26, FR27, FR28, FR29, FR30, FR31


## Epic 1: The Metasploit Foundation (Interactive CLI & Target Config)
A Red Teamer can launch the `skconsole`, navigate the welcome screen, load an exploit module, set target variables (including auth), and execute a basic (static) attack.

### Story 1.1: Core CLI Scaffold and REPL Loop
As a Red Teamer,
I want to launch the `skconsole` and enter an interactive REPL loop,
So that I can interact with the framework without writing standalone python scripts.

**Acceptance Criteria:**
**Given** I have installed the framework via `pip install -e .`
**When** I type `skconsole` in my terminal
**Then** I am presented with an ASCII welcome screen
**And** dropped into an interactive prompt (`sk>`) that supports basic `exit` and `help` commands.

### Story 1.2: Module Loading and Introspection
As a Red Teamer,
I want to use the `use` command to load an exploit module and view its options,
So that I know what parameters I need to configure before attacking.

**Acceptance Criteria:**
**Given** I am in the `skconsole` prompt
**When** I type `use modules.prompt_injection.basic`
**Then** the prompt changes to reflect the loaded module context (`sk (basic)>`)
**And** typing `show options` displays a table of required parameters (e.g., TARGET, PAYLOAD).

### Story 1.3: Target Configuration State Management
As a Red Teamer,
I want to set global and module-specific variables (like TARGET URLs and Auth Tokens),
So that the exploit engine knows where to direct its attacks.

**Acceptance Criteria:**
**Given** I have a module loaded in `skconsole`
**When** I type `set TARGET http://localhost:8000/api`
**Then** the framework saves that URL into its active session state
**And** subsequent `show options` commands reflect the updated TARGET value.

### Story 1.4: Base Module Execution (Static Fallback)
As a Red Teamer,
I want to type `run` to execute a loaded module against my configured target,
So that I can test basic, static payload injections against an endpoint.

**Acceptance Criteria:**
**Given** I have set a valid TARGET and loaded a basic prompt injection module
**When** I type `run`
**Then** the `BaseModule.run()` method executes, sending an HTTP request to the target
**And** the raw response is printed to the console (pre-textual dashboard implementation).


## Epic 2: The Autonomous Agent Engine (LLM Execution Loop)
The framework can now deploy an autonomous LLM attacker that intelligently adapts its payloads over multiple turns against a target, rather than just sending static strings.

### Story 2.1: LiteLLM Gateway Integration
As an Agent Deployer Engine,
I want to route all LLM requests through LiteLLM,
So that users can configure OpenAI, Anthropic, or local Ollama models interchangeably.

**Acceptance Criteria:**
**Given** I configure an `ATTACKER_MODEL` in the console (e.g., `gpt-4o`)
**When** the `AgentDeployer` class initiates an attack
**Then** the request is successfully routed through the `litellm.completion` asynchronous wrapper
**And** the engine receives a standard, normalized response object regardless of the underlying provider.

### Story 2.2: Autonomous Multi-Turn Execution Loop
As a Red Teamer,
I want the exploit module to use an LLM to dynamically generate payloads based on previous target responses,
So that the attack adapts to basic WAFs or guardrails automatically.

**Acceptance Criteria:**
**Given** I run an agentic exploit module
**When** the target rejects the first payload
**Then** the `AgentDeployer` feeds the rejection back into the Attacker LLM context
**And** generates a new, modified payload for a second attempt
**And** halts if the `max_turns` (default 5) limit is reached to prevent runaway costs.

### Story 2.3: Deterministic Success Evaluation
As a Red Teamer,
I want the engine to independently verify if an attack succeeded by searching for a leaked secret,
So that I don't have to rely on the Attacker LLM hallucinating its own success.

**Acceptance Criteria:**
**Given** an autonomous attack loop is running
**When** the target responds
**Then** the `AgentDeployer` checks the response string against a predefined expected regex or secret (e.g., 'SK-ALPHA-99')
**And** immediately halts the loop and flags 'SUCCESS' if the string is found.


## Epic 3: The Cinematic Dashboard (Real-Time TUI)
When a user types `run`, the standard prompt vanishes and is replaced by a visually stunning, split-pane dashboard featuring a live ASCII threat graph and cascading agent logs.

### Story 3.1: Textual App Foundation and Split-Pane Layout
As a Red Teamer,
I want the execution phase to launch into a multi-pane terminal dashboard,
So that I can view target status, agent thoughts, and threat trees simultaneously without terminal scrolling clutter.

**Acceptance Criteria:**
**Given** I am in `skconsole`
**When** I type `run`
**Then** the application instantiates a full-screen `textual.App` overriding the standard REPL
**And** the screen is divided into 3 distinct bordered panes (Status, Logs, Threat Graph).

### Story 3.2: Async Event Bus (Engine to UI Communication)
As the TUI Dashboard,
I want to receive real-time state updates from the `AgentDeployer` without blocking the main rendering thread,
So that the UI remains highly responsive while the LLM makes 10-second API calls.

**Acceptance Criteria:**
**Given** the `textual` dashboard is active and the `AgentDeployer` is running in a background task
**When** the agent fires a payload
**Then** the engine yields a `PayloadFired` Textual Message
**And** the TUI intercepts that message and updates the Agent Logs pane instantly.

### Story 3.3: Live ASCII Threat Graph Widget
As a Red Teamer,
I want to watch a dynamic tree graph build itself in real-time as the agent attacks,
So that I can visually understand the attack decision path at a glance.

**Acceptance Criteria:**
**Given** the dashboard is running
**When** the `AgentDeployer` pivots to a new strategy or receives a target response
**Then** the `rich.Tree` widget in the right pane appends a new node
**And** colors it Red `[X]` for blocked or Green `[✓]` for success based on the evaluation engine.

### Story 3.4: Gamified Failure States & Token Spend
As a Vibe Coder,
I want to see my token spend and see playful hacker quotes when attacks fail,
So that the security testing experience feels like an engaging game.

**Acceptance Criteria:**
**Given** the dashboard is running
**When** an attack completes
**Then** the final Token Spend for the session is calculated and displayed in the Status pane
**And** if the attack failed, a randomized "hacker culture" quote is displayed in a centered modal overlay.


## Epic 4: The Vibe Coder Experience & Extensibility
Indie developers can run the tool in a single command for rapid validation, and security researchers can drop new exploit python files into a folder to instantly extend the framework.

### Story 4.1: Dynamic Plugin Discovery
As an Exploit Developer,
I want to add a new python file to `src/modules/` and have it immediately available in the console,
So that I don't have to edit core routing files to test a new exploit.

**Acceptance Criteria:**
**Given** I drop a new python class inheriting from `BaseModule` into the `modules` directory
**When** I launch `skconsole` and type `use new_module`
**Then** the framework successfully loads it using standard library `importlib` and `pkgutil` scanning.

### Story 4.2: Headless CLI Execution Mode
As a Vibe Coder,
I want to run a scan with a single bash command,
So that I can rapidly validate an endpoint without navigating an interactive REPL.

**Acceptance Criteria:**
**Given** I am in my standard bash terminal
**When** I run `sk run agentic_prompt_extraction --target http://localhost:8000`
**Then** the framework bypasses the `skconsole` REPL, runs the exploit via the dashboard, and exits cleanly upon completion.


## Epic 5: Evidence Capture & Compliance Export
Enterprise Pentesters can sanitize their terminal output to remove PII and export their attack paths into JSON, Markdown, or SARIF formats for SOC2 reporting.

### Story 5.1: Pydantic Data Boundaries
As the Core Engine,
I want all Attack Results and Threat Nodes strictly typed as Pydantic models,
So that data serialization across the application boundary is guaranteed and safe.

**Acceptance Criteria:**
**Given** an exploit completes
**When** it returns data to the console
**Then** the data is strictly structured as an `AttackResult` Pydantic model (not a raw dict).

### Story 5.2: Markdown and JSON Export
As an Enterprise Pentester,
I want to export the final attack result to a file,
So that I have compliance-ready evidence of the vulnerability.

**Acceptance Criteria:**
**Given** an attack has completed in the dashboard
**When** I press the Export hotkey (`E`)
**Then** the Pydantic `AttackResult` is serialized and saved to disk as both a readable `.md` file and a parsable `.json` file.
