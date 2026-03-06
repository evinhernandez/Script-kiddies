# SK Framework (Script-Kiddies)
### An Open-Source Offensive Security Framework for AI Systems

![License: MIT](https://img.shields.io/badge/License-MIT-3ecfb2.svg?style=for-the-badge)
![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge)
![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg?style=for-the-badge)

SK Framework is a powerful, extensible red-teaming platform designed to test LLMs against prompt injection, jailbreaking, and data exfiltration. It features a cinematic terminal dashboard, an autonomous agent engine for multi-turn attacks, and professional reporting.

---

## 🚀 Quick Start

Get up and running in 60 seconds:

```bash
# 1. Clone and Install
git clone https://github.com/evinhernandez/script-kiddies.git
cd script-kiddies
python3 -m venv venv && source venv/bin/activate
pip install -e .

# 2. Launch Operator Console
skconsole

# 3. Run your first autonomous attack
sk(sk)> use agentic_prompt_extraction
sk(agentic_prompt_extraction)> run
```

---

## ✨ Key Features

*   **Cinematic TUI Dashboard**: Real-time monitoring of attacks via a multi-pane Textual interface with live log streaming and latency tracking.
*   **Autonomous Agent Engine**: A multi-turn "Attacker LLM" that automatically adapts its payloads based on target refusals or responses.
*   **LiteLLM Integration**: Unified access to OpenAI, Anthropic, Gemini, or any local model via Ollama/vLLM.
*   **Dynamic Plugin System**: Modular exploit architecture—just drop a Python file into `src/modules/` to add a new vector.
*   **Deterministic Verification**: Use "Expected Flags" to verify successful leaks, eliminating LLM hallucinations in security reports.
*   **Instant Local Lab**: Spin up a complete security testbed (Ollama + OWASP AI Goat) with a single Docker command.

---

## 🔬 Local Security Lab

We provide a pre-configured environment for "target practice" against local open-source LLMs.

```bash
cd labs/
docker-compose up -d
# Point framework at local Llama 3 running in Docker
sk attack prompt_injection --model llama3 --base_url http://localhost:11434/v1
```
See the [Lab Guide](docs/LAB_GUIDE.md) for full setup instructions.

---

## 🏗️ Architecture Overview

The framework is built for modularity and speed:
1.  **Core Engine**: Handles module discovery, dynamic loading, and SQLite session persistence.
2.  **Scoring Engine**: Multi-heuristic evaluation (regex, keyword, semantic) to determine attack success.
3.  **Agent Layer**: Orchestrates multi-turn loops using a "thinking" attacker model.
4.  **UI Layer**: Professional Textual dashboard for operators + Click CLI for automation.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Docker & Docker Compose (for local labs)

### Development Install
```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Configuration
Create a `.env` file in the project root to store your API keys:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=x-...
GOOGLE_API_KEY=...
```

---

## 🧪 Testing

Run the full test suite to ensure everything is configured correctly:
```bash
PYTHONPATH=. python3 -m unittest discover tests
```

---

## ❓ Troubleshooting

*   **ModuleNotFoundError: No module named 'pydantic_settings'**: Run `pip install pydantic-settings`. The framework uses Pydantic v2 features.
*   **ConnectionRefusedError (localhost:8001/11434)**: Ensure your local target or Docker containers are running before starting the attack.
*   **TUI looks garbled**: Use a modern terminal emulator (like iTerm2, WezTerm, or VS Code Terminal) that supports TrueColor and UTF-8.

---

## 🤝 Contributing

We are looking for security researchers to contribute new exploits! 
- Read the [Module Development Guide](docs/MODULE_GUIDE.md).
- Submit a PR with your new module in `src/modules/<category>/`.

---

*Disclaimer: SK Framework is for educational and authorized security testing purposes only. The authors are not responsible for misuse.*
