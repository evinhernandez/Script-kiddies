# SK Framework (Script-Kiddies)
### An Open-Source Offensive Security Framework for AI Systems

![License: MIT](https://img.shields.io/badge/License-MIT-3ecfb2.svg?style=for-the-badge)
![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge)
![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg?style=for-the-badge)

SK Framework is a powerful, extensible red-teaming platform designed to test LLMs against prompt injection, jailbreaking, and data exfiltration. It features a cinematic terminal dashboard, an autonomous agent engine for multi-turn attacks, and professional reporting.

---

## 🚀 Key Features

*   **Cinematic TUI Dashboard**: Real-time monitoring of attacks via a multi-pane Textual interface.
*   **Autonomous Agent Engine**: A multi-turn "Attacker LLM" that adapts its payloads based on target responses.
*   **LiteLLM Integration**: Seamlessly switch between OpenAI, Anthropic, Gemini, or local models (Ollama).
*   **Dynamic Plugin System**: Add new exploits by dropping Python files into `src/modules/`.
*   **Headless Mode**: Integrate into CI/CD pipelines with simple CLI commands.
*   **Professional Reporting**: Export attack results to JSON and human-readable Markdown reports.
*   **Deterministic Verification**: Use "Expected Flags" to verify successful leaks without LLM hallucinations.
*   **Instant Local Lab**: Spin up Ollama and OWASP AI Goat with a single Docker command.

---

## 🔬 Local Security Lab

We provide a pre-configured environment for "target practice" against local open-source LLMs.

```bash
cd labs/
docker-compose up -d
sk attack prompt_injection --model llama3 --base_url http://localhost:11434/v1
```
See the [Lab Guide](docs/LAB_GUIDE.md) for full setup instructions.

---

## 🏆 Exploit Showcase (Hall of Fame)

The SK Framework has successfully demonstrated the following high-impact attack chains:
*   **Llama 3 System Prompt Leak**: Extracted secret instructions from a base Llama 3 model in 3 turns using the autonomous agent.
*   **Mistral 7B Roleplay Escape**: Successfully bypassed safety guardrails by pivoting to a "DAN" persona after an initial refusal.
*   **OWASP AI Goat Flag Capture**: Automated the discovery and extraction of the 'SK-ALPHA' flag from the AI Goat vulnerable environment.

---

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/script-kiddies.git
    cd script-kiddies
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the framework**:
    ```bash
    pip install -e .
    pip install -r requirements-dev.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root:
    ```bash
    OPENAI_API_KEY=your_key_here
    ANTHROPIC_API_KEY=your_key_here
    ```

---

## 🕹️ Usage

### 1. Interactive Console (The REPL)
Launch the Matrix-themed operator console:
```bash
skconsole
```
**Commands:**
*   `show modules`: List available attack vectors.
*   `use <module>`: Load an exploit.
*   `show options`: See required parameters.
*   `set TARGET <provider>`: Configure your target.
*   `run`: Launch the cinematic dashboard and execute the attack.

### 2. Headless Mode (Automation)
Run a single attack and export the report:
```bash
sk attack prompt_injection --target openai --model gpt-4o --export
```

### 3. Agentic Attacks
Force a model to leak its secret instructions using the autonomous agent:
```bash
sk attack agentic_prompt_extraction --max_turns 5 --expected_flag "SECRET-123"
```

---

## 🏗️ Architecture

The framework is divided into three main layers:
1.  **Core Engine**: Orchestrates module discovery, session persistence (SQLite), and scoring.
2.  **Agent Layer**: Manages multi-turn conversation state and autonomous payload generation.
3.  **UI Layer**: Provides both a high-fidelity Textual dashboard and a scriptable Click CLI.

---

## 🧪 Testing

Run the full test suite:
```bash
PYTHONPATH=. python3 -m unittest discover tests
```

---

## 🤝 Contributing

We welcome new modules! Check out `docs/MODULE_GUIDE.md` (coming soon) to learn how to write your own exploit plugins.

*Disclaimer: SK Framework is for educational and authorized security testing purposes only. Use responsibly.*
