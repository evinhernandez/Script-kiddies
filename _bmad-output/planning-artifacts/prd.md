---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish']
inputDocuments: ['product-brief-Script-kiddies-2026-03-04.md', 'project-memory/01_project_brief.md', 'project-memory/02_prd.md', 'project-memory/03_architecture.md']
workflowType: 'prd'
---

# Product Requirements Document - Script-kiddies

**Author:** ehernandez
**Date:** 2026-03-04

## Executive Summary

Script-kiddies is an open-source offensive security framework engineered to standardize the testing of AI infrastructure against real-world vulnerabilities. It specifically targets the OWASP Top 10 for LLM Applications and data exfiltration vectors. Designed for a spectrum of users—from "vibe coders" seeking rapid validation to enterprise pentesters requiring compliance-ready evidence—the framework bridges the gap between ad-hoc prompt injection scripts and rigid, proprietary SaaS platforms. It provides a methodical, interactive CLI environment to execute and visualize complex autonomous attacks against both local and hosted AI models.

### What Makes This Special

Unlike static vulnerability scanners, Script-kiddies utilizes an `AgentDeployer` engine that deploys autonomous, goal-oriented LLM attackers. These agents engage in a multi-turn execution loop, dynamically adapting their jailbreaks to bypass target defenses in real-time. This autonomous engine pairs with a highly visual, cinematic Terminal User Interface (TUI) featuring a real-time ASCII threat graph. This unique combination delivers the "cool factor" required for viral, community-driven adoption at CTF events while simultaneously capturing the precise attack path necessary for enterprise SOC2 reporting.

## Project Classification

- **Project Type:** CLI Tool / API Backend
- **Domain:** Cybersecurity / Scientific (High validation methodology)
- **Complexity:** High (Multi-turn autonomous LLM execution against live targets)
- **Project Context:** Brownfield (Building upon an initialized core architecture and project memory)

## Success Criteria

### User Success
- **Immediate Value (TTV):** Users can install the framework (`pip install -e .`), load a module, and execute an attack in under 2 minutes.
- **Actionable Confidence:** Users receive a clear, exportable artifact (Markdown/SARIF) proving their AI deployment is either vulnerable or secure.

### Business Success
- **Community Adoption:** Achieve sustained month-over-month growth in GitHub stars, clones, and PyPI downloads.
- **Ecosystem Integration:** Achieve native inclusion in leading cybersecurity operating systems (Kali Linux, Parrot OS).
- **OWASP Flagship:** Achieve incubation and graduation as an official OWASP testing standard project.

### Technical Success
- **Agentic Reliability:** The `AgentDeployer` navigates multi-turn attacks without crashing or dropping conversational context.
- **Extensibility:** Users can load a new exploit module by dropping a Python file into `src/modules/` with zero changes to core routing.

### Measurable Outcomes
- Acquire >10 community-contributed exploit modules within 6 months of launch.
- Achieve integration into at least two major CTF platforms (TryHackMe, Hack The Box).

## Product Scope

### MVP - Minimum Viable Product (Phase 1)
- **Core CLI Engine:** The `skconsole` interactive interface supporting Metasploit-style commands (`use`, `set`, `run`).
- **Autonomous Engine:** The `AgentDeployer` executing multi-turn LLM-driven attacks against HTTP/JSON targets.
- **Visual TUI:** A responsive `rich`-based terminal interface featuring split-pane views and a live ASCII threat graph.
- **Core Modules:** Initial exploit modules targeting the OWASP Top 10 for LLM Applications (Prompt Extraction, RAG Poisoning, Data Exfiltration).
- **Static Fallback:** A fail-safe mechanism that injects static OWASP Top 10 payloads if the autonomous agent errors.
- **Deterministic Validation:** Mechanisms to evaluate success by checking target output for known injected secrets.

### Growth Features (Phase 2)
- **Enterprise Proxies:** Integration with custom CA certs and dynamic auth hooks.
- **WAF Evasion:** Detection of HTTP 429s/403s with exponential backoff mechanisms.
- **Advanced Export:** SARIF export format for GitHub Advanced Security integration.
- **Judge Model:** A secondary independent LLM for evaluating non-deterministic attack success.

### Vision (Phase 3)
- **Enterprise Lifecycle Integration:** Merging offensive capabilities into the `Script-kiddie.ai` platform to provide complete AI-SPM and NHI mapping alongside defensive Guardrails.
- **Web UI:** A graphical dashboard for enterprise users.

## User Journeys

### 1. The Hacker / Red Teamer (Core Interactive Journey)
**Opening Scene:** The Red Teamer launches `skconsole` and is greeted by a dynamic ASCII welcome screen.
**Rising Action:** They navigate an interactive menu to choose an autonomous RAG poisoning module. They set the target URL.
**Climax:** Upon execution, the TUI opens a split-pane view simulating an EDR-style trace. Vibrant colors flash as the autonomous attack runs, and the `AgentDeployer` verbosely narrates its actions ("Attempting role-play bypass... Failed. Pivoting to delimiter injection...").
**Resolution:** The target breaks and leaks the system prompt. The screen flashes success. The user remains in the exploit context to pivot deeper or hits an export hotkey to generate a sanitized file for evidence.

### 2. The Vibe Coder (Rapid Validation Journey)
**Opening Scene:** An indie developer finishes a LangChain app and wants to check for API key leaks before pushing to GitHub.
**Rising Action:** They run a single CLI command (`sk test auto --target http://localhost:8000`).
**Climax:** The cinematic TUI launches directly into the live threat graph, running the OWASP baseline quickly and verbosely.
**Resolution:** The test finishes with a "green checkmark" summary, giving them confidence to commit their code.

### 3. The Enterprise Pentester (Compliance & Reporting Journey)
**Opening Scene:** A consultant tests a corporate LLM deployment during a paid engagement.
**Rising Action:** They load a bulk target file via the interactive menu and configure the output format for SARIF.
**Climax:** They screen-share the live EDR-style trace demonstrating the autonomous agent bypassing the client's guardrails in real-time.
**Resolution:** They export the threat graph and structured evidence files directly into their SOC2 compliance report.

## Domain-Specific Requirements

### Compliance & Regulatory
- **OWASP LLM Top 10:** The framework maps all exploits directly to the OWASP Top 10 for LLMs.
- **Enterprise Standards:** Exported reports align with NIST AI RMF and CISA "Secure by Design" guidelines.
- **Data Privacy:** The tool sanitizes actual PII/PCI/HIPAA data before displaying it in the terminal or saving it to logs.

### Technical Constraints
- **Context Window Management:** The `AgentDeployer` manages the context window during multi-turn attacks to avoid dropping history or exceeding API limits.
- **Safe Execution:** The framework ensures downstream tool execution (e.g., Agent Tool Abuse tests) does not inadvertently cause destructive actions on the target system without explicit warning.

### Integration Requirements
- **Local & Hosted Interoperability:** The engine integrates with local inference engines (Ollama) and commercial APIs (OpenAI, Anthropic) via `litellm`.
- **Reporting Standards:** The engine outputs evidence in SARIF format for enterprise SIEM integration.

### Risk Mitigations
- **Target Rate Limiting:** The framework includes configurable throttling to prevent DDoSing the target API.
- **Model Hallucination:** The framework requires deterministic scoring to differentiate between successful exploits and hallucinated success responses.

## Innovation & Novel Patterns

### Detected Innovation Areas
- **Autonomous Agent Hacking Loop:** Shifting from static payload injection to deploying a goal-oriented LLM (`AgentDeployer`) that dynamically interacts with the target in a multi-turn conversation.
- **Cinematic TUI:** Using `rich` and `textual` to create a visually striking Terminal UI featuring a real-time ASCII threat graph mapping the attacker's decision tree.
- **Tmux-style Pane Management:** Implementing dynamic window panes to manage cognitive overload, separating the threat graph, raw EDR trace, and token spend into configurable views.

### Validation Approach
- **Deterministic Success Scoring:** Target system prompts must contain known secrets (e.g., 'SK-ALPHA-99') that the framework checks to confirm success.
- **Independent Judge Model:** Utilizing a secondary, smaller local model to evaluate the conversation log independently from the Attacker Agent.

## CLI Tool / API Backend Specific Requirements

### Project-Type Overview
Script-kiddies is architected as a hybrid CLI Tool and headless API Backend. The primary UI is the interactive `skconsole`, but the core engine is decoupled to allow REST/GraphQL exposure in Phase 2.

### Technical Architecture Considerations
- **Decoupled Engine:** The `AgentDeployer` and `Target` classes operate independently from the TUI, communicating via an event stream or asynchronous callbacks.
- **Authentication Handling:** The framework supports loading credentials from a local secrets file (`.env`) or prompting the user interactively during the `set TARGET` flow.

### Command Structure & Output Formats
- **Interactive Commands:** The CLI supports `use [module]`, `set [variable]`, `show options`, `run`, and `export`.
- **Machine-Readable Exports:** The engine standardizes attack results into JSON, SARIF, Markdown, and raw STDOUT.

### Implementation Considerations
- **Dynamic Module Loader:** The framework recursively scans `src/modules/` on startup and automatically registers any Python class inheriting from `BaseModule`.

## Functional Requirements

### 1. Terminal User Interface (TUI) Management
- **FR1:** Users can launch an interactive command-line interface (`skconsole`).
- **FR2:** Users can view a dynamic, animated ASCII welcome screen upon launch.
- **FR3:** Users can view an interactive menu categorized by exploits, vulnerabilities, and checks.
- **FR4:** Users can toggle different TUI verbosity levels and pane layouts (e.g., EDR trace view vs. summary view).
- **FR5:** Users can view a real-time ASCII threat graph that visually branches based on the `AgentDeployer`'s decision tree.
- **FR6:** Users can view a live "Token Spend" counter during autonomous attacks.
- **FR7:** Users can view gamified failure messages (e.g., hacker movie quotes) when an attack fails.

### 2. Module & Execution Management
- **FR8:** Users can load specific exploit modules using the `use [module_name]` command.
- **FR9:** Users can view module options using the `show options` command.
- **FR10:** Users can set target URLs and configuration variables using the `set [variable] [value]` command.
- **FR11:** Users can execute the loaded module against the configured target using the `run` command.
- **FR12:** The system can dynamically discover and load new exploit modules dropped into the `src/modules/` directory without code recompilation.
- **FR13:** Users can execute the framework in a "rapid validation" mode via a single CLI command bypassing the interactive prompt.

### 3. Target Configuration & Connectivity
- **FR14:** Users can input target definitions directly via URL.
- **FR15:** Users can load a list of multiple targets from a designated local directory or file.
- **FR16:** Users can provide target authentication credentials via an interactive prompt.
- **FR17:** Users can load target authentication credentials from a local secrets file.
- **FR18:** The system can connect to both local inference engines (Ollama) and commercial APIs (OpenAI, Anthropic).

### 4. Autonomous Attacker Engine (AgentDeployer)
- **FR19:** The system can deploy an LLM-driven attacker agent instructed with a specific objective.
- **FR20:** The system can engage the target in a multi-turn, adaptive execution loop based on the target's responses.
- **FR21:** The system can stream verbose, narrative logging of the agent's actions to the TUI.
- **FR22:** The system will automatically terminate the autonomous loop if the `max_turns` limit is reached.
- **FR23:** The system will automatically fallback to injecting static OWASP Top 10 payloads if the autonomous agent errors or times out.

### 5. Validation & Evaluation
- **FR24:** The system can evaluate attack success deterministically by checking target output for a known injected secret.
- **FR25:** The system can evaluate attack success probabilistically using an independent local "Judge Model".
- **FR26:** The system will sanitize or redact identified sensitive data from the terminal output and logs.

### 6. Evidence Capture & Export
- **FR27:** Users can capture a snapshot of the current TUI state using an export command.
- **FR28:** Users can export attack results and threat graph data in JSON format.
- **FR29:** Users can export attack results in Markdown format for human-readable reporting.
- **FR30:** Users can export attack results in SARIF format for CI/CD integration.
- **FR31:** Users can pipe the raw output of the engine to standard stdout.

## Non-Functional Requirements

### Security & Privacy (Drink Our Own Champagne)
- **NFR1:** The system must never log target API keys or Bearer tokens to standard output or log files in plain text.
- **NFR2:** The system must utilize a redaction module to scrub identified sensitive data before saving export reports to disk.
- **NFR3:** The framework codebase must adhere to OWASP Top 10 for LLM Applications and pass automated security linting (Bandit, Semgrep) before main branch deployment.
- **NFR4:** The project must generate and maintain a Software Bill of Materials (SBOM) for all releases.

### Performance & Reliability
- **NFR5:** The `AgentDeployer` must enforce a configurable network timeout (default: 30 seconds) per LLM call. If exceeded, it must fail gracefully without crashing the `skconsole` loop.
- **NFR6:** The system must enforce a hardcoded maximum token limit per attack session (e.g., 10,000 tokens) to prevent API cost runaway.
- **NFR7:** The system must provide actionable, verbose error logging in a debug pane to differentiate between WAF blocks (HTTP 403) and LLM hallucinations.

### Portability & Compatibility
- **NFR8:** The framework must install and execute successfully via `pip` on standard distributions of Linux (Kali Linux, Ubuntu), macOS (M-series and Intel), and Windows (WSL2).
- **NFR9:** The core framework installation must not require C++ build tools or massive machine learning tensor libraries (e.g., PyTorch) to function.
