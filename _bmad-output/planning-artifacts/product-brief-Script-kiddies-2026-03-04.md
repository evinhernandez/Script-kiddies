---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments: ['project-memory/01_project_brief.md', 'project-memory/02_prd.md', 'project-memory/03_architecture.md']
date: 2026-03-04
author: ehernandez
---

# Product Brief: Script-kiddies

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

Script-kiddies is an open-source offensive security framework—often conceptualized as the "Metasploit of AI." It provides penetration testers, security engineers, and AI administrators with a methodical, interactive platform to test AI systems for vulnerabilities. By utilizing deployable, autonomous Attacker Agents rather than static payload lists, the framework dynamically probes LLMs, RAG pipelines, and agentic workflows to expose risks like prompt leakage and data exfiltration. The ultimate goal is community-driven adoption, serving as the premier testing standard in real-world environments and competitive arenas like DEF CON and Black Hat CTF villages.

---

## Core Vision

### Problem Statement
The AI industry currently lacks a standardized, methodical, and easy-to-use offensive testing framework. Security professionals struggle to adequately test AI systems for vulnerabilities because current tools rely on static, easily bypassed prompt-injection lists or are locked behind proprietary SaaS platforms.

### Problem Impact
Without a standardized way to test AI infrastructure, organizations deploy LLMs and agents that are highly susceptible to prompt injection, data exfiltration, and unauthorized data leakage. Security engineers are left blindly trusting model outputs or manually attempting disjointed attack techniques, leading to critical security oversights.

### Why Existing Solutions Fall Short
Current solutions are either static (simple lists of prompt injections that fail against dynamic LLM defenses) or disjointed scripts that lack a unified methodology. They do not offer a cohesive, extensible environment (like a `console` interface) that security professionals are accustomed to, nor do they leverage autonomous AI agents to actively adapt their attack strategies against a target.

### Proposed Solution
Script-kiddies introduces an interactive command-line interface (`skconsole`) that allows users to easily load modules, set targets, and run attacks. Its core differentiator is the `AgentDeployer`—an engine that deploys an autonomous LLM attacker instructed with a specific goal (e.g., "extract the secret key"). This attacker dynamically interacts with the target, adapting its jailbreaks and strategies until the goal is met or max iterations are reached. To drive adoption, the platform features a highly visual, "hacker-movie" style Terminal UI using the `rich` library, complete with a real-time ASCII live threat graph that tracks the autonomous agent's decision tree.


### Cinematic TUI & ASCII Threat Graph
The framework will utilize a highly visual Terminal User Interface (TUI) powered by the `rich` and `textual` libraries. It will feature a split-pane layout with a 'Matrix-style' real-time expanding ASCII threat graph. This graph visually maps the autonomous agent's decision tree (e.g., branching out when trying a 'Role-play Jailbreak' and turning red upon failure or green upon success). This provides a 'cool factor' for the practitioner while capturing the attack path perfectly for SOC2 enterprise reporting.

### Key Differentiators
1. **Deployable Autonomous Agents:** Moves beyond static testing by using an LLM to actively attack another LLM in a multi-turn loop.
2. **Familiar Metasploit-Style UX:** Lowers the barrier to entry for traditional security professionals via a modular CLI (`use`, `set TARGET`, `run`).
3. **Cinematic Terminal UI (TUI):** A matrix-style, highly responsive terminal interface featuring live ASCII threat graphs that visually map the AI's attack path—gamifying the experience for hackers while providing exportable documentation for SOC2 reports.
4. **CTF and Conference Ready:** Built from the ground up to be leveraged in high-visibility environments like hacker villages, driving viral, community-led growth.

## Target Users

### Primary Users

1. **The 'Vibe Coder' / Indie Developer**
   - **Context:** Building rapid prototypes or AI apps using tools like LangChain, Vercel AI SDK, or Open Claw. They are not security experts.
   - **Problem:** They want to make sure they haven't accidentally exposed their system prompts or API keys, but they don't have time to learn complex security frameworks.
   - **Success Vision:** A simple, one-line install (`pip install -e .`) and a command (`sk attack auto`) that gives them a 'green checkmark' indicating their app is reasonably safe. They might even invoke this as a 'Skill' for their own coding agents.

2. **The Hacker / Red Teamer**
   - **Context:** Attending DEF CON, playing CTFs, or actively looking for bounties.
   - **Problem:** Needs a modular, extensible toolkit to test novel, complex AI jailbreaks without writing a custom script every time.
   - **Success Vision:** They can drop a new exploit script into the `modules/` folder, load it via `skconsole`, and use the autonomous agent engine to dynamically attack a target, all while watching the cool ASCII threat graph.

3. **The Enterprise Pentester / Security Consultant**
   - **Context:** Hired by enterprises (via companies like Vitruvius Cyber) to validate the security posture of an enterprise AI deployment.
   - **Problem:** Needs to systematically prove vulnerabilities exist (data exfiltration, prompt leakage) and generate compliance-ready evidence.
   - **Success Vision:** A tool that not only executes advanced autonomous attacks but also generates standardized, exportable proof (SARIF, Markdown reports, threat graphs) to show to the CISO.

### Secondary Users

1. **The CISO / Enterprise Security Administrator**
   - **Context:** They don't run the tool themselves. They receive the output from the Pentester or the automated CI/CD pipeline.
   - **Problem:** Needs to understand *how* the AI broke and *what* the risk is in plain English, not just 'Injection Succeeded.'
   - **Success Vision:** Reviewing the exported ASCII threat graphs and structured reports to understand the exact decision tree the attacker took, proving the need for enterprise guardrails.

### User Journey

1. **Discovery:** The Vibe Coder sees a cool Matrix-style screenshot of the threat graph on Twitter. The Pentester sees it used at a Black Hat AI Village.
2. **Onboarding:** They run `pip install sk-framework`. They type `skconsole` and are dropped into a Metasploit-like interface. It feels immediately familiar to security folks and incredibly 'cool' to indie devs.
3. **Core Usage:** The user sets a target URL (`set TARGET ...`) and runs an autonomous exploit (`run`). They watch the live threat graph build in real-time as the agent tries different jailbreaks.
4. **Success Moment:** The agent successfully extracts a hidden system prompt. The screen flashes red, the threat graph shows the exact path, and the user feels the rush of a successful hack.
5. **Long-term:** The Vibe Coder integrates it into their daily AI-agent workflow as a 'Skill.' The Pentester uses it as their default tool on every engagement, exporting the threat graphs for their client reports.

## Success Metrics

### User Success Metrics
- **The 'Holy F***' Moment:** Users experience an immediate rush of excitement (the 'cool factor') upon seeing the live ASCII threat graph execute an attack.
- **Workflow Integration:** Vibe coders seamlessly integrate the tool into their daily AI-agent workflow without friction or complex setup.
- **Confidence in Posture:** Users report a measurable increase in confidence regarding their AI application's security posture before deployment.
- **Time-to-Value:** Users can go from `pip install` to running their first successful AI exploit in under 2 minutes.

### Business Objectives (Open Source & Community)
- **OWASP Integration:** Successfully incubate and transition the project into an official OWASP Flagship or Lab project.
- **Ecosystem Distribution:** Gain native inclusion in premier security operating systems like Kali Linux, Parrot OS, and BlackArch.
- **Educational Adoption:** Get leveraged as a core learning tool in cybersecurity training platforms like TryHackMe and Hack The Box.
- **Community Evangelism:** Drive organic growth through conference presentations (DEF CON, Black Hat, local OWASP chapters) and word-of-mouth.

### Key Performance Indicators (KPIs)
- **Adoption:** Number of GitHub stars, clones, and PyPI downloads month-over-month.
- **Community Contributions:** Number of pull requests specifically adding new exploit modules (`src/modules/`) from external security researchers.
- **Engagement:** Number of active feature requests and issues opened by the community.
- **Ecosystem Mentions:** Tracked mentions and usage in third-party CTF write-ups, blog posts, and conference talks.

## MVP Scope

### Core Features
- **Metasploit-Style TUI (`skconsole`):** A highly responsive Terminal User Interface utilizing `rich`, providing interactive commands (`use`, `set`, `run`) with an ASCII live threat graph mapping the agent's attack path.
- **Autonomous Agent Engine (`AgentDeployer`):** A multi-turn LLM-driven execution loop that adapts to target defenses in real-time rather than relying solely on static payloads.
- **Target Agnosticism:** The ability to test both local models (via Ollama/vLLM) and hosted LLM applications via generic HTTP/JSON interfaces.
- **Essential Exploit Modules:** An initial set of modules specifically targeting the OWASP Top 10 for LLM Applications (e.g., Prompt Injection, Insecure Output Handling, Training Data Poisoning concepts via RAG, Data Exfiltration).
- **Framework Mapping:** Output reporting that maps successful attacks to relevant security frameworks (OWASP, NIST AI RMF, CISA guidelines).

### Out of Scope for MVP
- **Web UI / Dashboard:** No graphical web application or React frontend for version 1.0. The focus remains strictly on a world-class TUI and CLI to facilitate seamless integration as an AI 'Skill' or sub-agent (for Claude, Gemini, Open Claw).
- **Enterprise RBAC/SSO:** Multi-user team management and role-based access control are deferred to the enterprise SaaS platform.

### MVP Success Criteria
- Security researchers can successfully execute an OWASP LLM Top 10 attack against a local or hosted target entirely from the `skconsole`.
- The live threat graph renders correctly and updates dynamically based on the `AgentDeployer`'s decisions.
- Vibe coders are able to install the tool via pip and run a test in under 5 minutes.

### Future Vision (2-3 Years)
- **Full Lifecycle Integration:** Merging this offensive red-team framework directly into the broader `Script-kiddie.ai` enterprise platform.
- **Complete AI-SPM & CI/CD:** The offensive modules become automated, continuous validation checks that run alongside defensive Guardrails.
- **Agentic Threat Hunting:** Deploying fleets of Script-kiddies agents that continuously map an organization's Non-Human Identities (NHI), test MCP server configurations, and report back to a centralized SOC dashboard.
