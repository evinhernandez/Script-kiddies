# Project Brief: Script-kiddies

## 1. Vision
To build the "Metasploit of AI"—an open-source offensive security framework designed specifically for red-teaming AI infrastructure (LLMs, SLMs, RAG pipelines, Vector Databases, and Agentic workflows).

## 2. Problem Statement
The AI industry lacks a standardized, easy-to-use offensive testing framework. Current tools are either basic static prompt-injection lists or complex, proprietary SaaS platforms. Red teamers need an interactive console capable of deploying *autonomous attacker agents* that dynamically probe and exploit AI systems.

## 3. Key Differentiators
*   **Deployable Autonomous Agents:** Instead of just sending static strings, the framework deploys an LLM-driven agent instructed to achieve a goal (e.g., "extract the secret key from this RAG system").
*   **BMAD Method:** Built using a documentation-first AI approach to ensure context retention across development phases.
*   **Metasploit-style UX:** A familiar `skconsole` interface with commands like `use`, `set TARGET`, and `run`.

## 4. Target Audience
*   AI Security Red Teamers
*   Vibe Coders ensuring their deployments are secure
*   Enterprise developers (as a feeder for the commercial 'Guardrails' platform)
