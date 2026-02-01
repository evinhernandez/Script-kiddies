# SK Framework
### An open-source AI security testing & training framework by Script-Kiddies

[![License: MIT](https://img.shields.io/badge/License-MIT-3ecfb2.svg?style=for-the-badge)](LICENSE)
[![OWASP Aligned](https://img.shields.io/badge/OWASP-ML%20Top%2010-e8d48b.svg?style=for-the-badge)](https://owasp.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3ecfb2.svg?style=for-the-badge)](https://python.org)
[![Status](https://img.shields.io/badge/Status-MVP-c9a84c.svg?style=for-the-badge)]()

```
> sk --help
```

**SK Framework** is a modular, plugin-based offensive security framework
purpose-built for AI systems. Think Metasploit — but for LLMs, AI agents,
and ML pipelines.

Learn how AI systems get attacked. Learn how to defend them.

---

## What is SK Framework?

AI is everywhere. Security training hasn't caught up. SK Framework bridges
that gap by giving security practitioners, developers, and students hands-on
offensive tooling against AI systems in a safe, controlled environment.

- **Attack AI systems** — prompt injection, jailbreaks, model poisoning, adversarial inputs, data exfiltration
- **Train defenders** — guided labs mapped to OWASP ML Security Top 10
- **Extend everything** — plugin architecture lets you write custom attack modules, labs, and scoring engines
- **CTF-ready** — built-in challenge/flag system and leaderboards

---

## Architecture

```
sk-framework/
├── src/
│   ├── core/                 # Engine: session manager, plugin loader, config
│   │   ├── engine.py         # Main orchestration engine
│   │   ├── session.py        # Attack session state management
│   │   ├── plugin_loader.py  # Dynamic module discovery & loading
│   │   └── config.py         # Configuration & env handling
│   ├── modules/              # Attack & scan modules (the weapons rack)
│   │   ├── prompt_injection/ # Prompt injection attacks
│   │   ├── jailbreak/        # Jailbreak techniques
│   │   ├── data_exfil/       # Data exfiltration probes
│   │   └── adversarial/      # Adversarial input generation
│   ├── labs/                 # Guided training labs
│   │   ├── lab_runner.py     # Lab execution engine
│   │   |- owasp_ml_top10/    # One lab per OWASP ML Top 10 item
│   │   └── ctf/              # Capture The Flag challenges
│   ├── api/                  # REST API server (FastAPI)
│   │   ├── app.py            # FastAPI application
│   │   ├── routes/           # Route handlers
│   │   └── middleware/       # Auth, rate limiting, logging
│   ├── cli/                  # Command-line interface
│   │   └── main.py           # Click-based CLI
│   └── utils/                # Shared utilities
│       ├── llm_client.py     # Unified LLM API client
│       ├── scoring.py        # Attack success scoring
│       └── logger.py         # Structured logging
├── labs/                     # Lab definition files (YAML)
├── tests/                    # Test suite
├── docs/                     # Documentation
├── config/                   # Default configs
├── scripts/                  # Setup & helper scripts
└── .github/                  # GitHub Actions CI, issue templates
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- An API key for at least one LLM provider (OpenAI, Anthropic, Google, etc.)

### Install

```bash
git clone https://github.com/script-kiddies/sk-framework.git
cd sk-framework
pip install -r requirements.txt
cp config/.env.template .env
# Edit .env with your API keys
```

### First Run

```bash
# List all available attack modules
sk modules list

# Run a prompt injection attack against a target model
sk attack prompt_injection --target openai --model gpt-4o --payload auto

# Start an interactive lab
sk lab start owasp_ml_01

# Launch the web UI (API + dashboard)
sk serve --port 8000

# Run CTF challenges
sk ctf list
sk ctf start prompt_escape_001
```

---

## OWASP ML Security Top 10 — Lab Mapping

| # | OWASP Item | SK Lab | Module |
|---|-----------|--------|--------|
| ML01 | Input Manipulation | `owasp_ml_01` | `prompt_injection` |
| ML02 | Data Poisoning | `owasp_ml_02` | `data_poisoning` |
| ML03 | Model Inversion | `owasp_ml_03` | `model_inversion` |
| ML04 | Membership Inference | `owasp_ml_04` | `membership_inference` |
| ML05 | Model Theft | `owasp_ml_05` | `model_extraction` |
| ML06 | AI Supply Chain | `owasp_ml_06` | `supply_chain` |
| ML07 | Transfer Learning Attack | `owasp_ml_07` | `transfer_attack` |
| ML08 | Model Skewing | `owasp_ml_08` | `model_skewing` |
| ML09 | Integrity Attacks | `owasp_ml_09` | `integrity` |
| ML10 | Model Denial of Service | `owasp_ml_10` | `dos_attack` |

---

## Contributing

SK Framework is community-driven. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

1. Fork the repo
2. Branch: `git checkout -b feature/your-module`
3. Build following the [Module Template](docs/module_template.md)
4. Add tests in `tests/`
5. Submit a PR — CI runs automatically

---

## Roadmap

- [x] Core engine & plugin architecture
- [x] CLI interface
- [x] Prompt injection module
- [x] Jailbreak module
- [x] OWASP ML Top 10 lab stubs
- [ ] Data exfiltration module
- [ ] Adversarial input generator
- [ ] Web dashboard UI
- [ ] CTF challenge engine
- [ ] Leaderboard system
- [ ] Docker containerized labs
- [ ] OWASP project submission

---

*SK Framework is an educational security tool. Use responsibly and only against systems you own or have explicit permission to test.*
