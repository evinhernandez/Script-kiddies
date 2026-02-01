# Contributing to SK Framework

Thank you for wanting to contribute. SK Framework is community-driven and we
need attack modules, labs, bug fixes, documentation, and ideas from the
security community.

---

## Quick Start for Contributors

```bash
git clone https://github.com/script-kiddies/sk-framework.git
cd sk-framework
git checkout -b feature/your-contribution
pip install -r requirements-dev.txt
# ... make your changes ...
python -m pytest tests/
git push origin feature/your-contribution
# Open a PR on GitHub
```

---

## What We Need Most

### 1. Attack Modules
New attack techniques against AI systems. Each module is self-contained and
follows the base class in `src/core/engine.py`. See
[Module Template](docs/module_template.md).

### 2. Labs
Guided training exercises mapped to OWASP ML Security Top 10. Labs are
defined in YAML + Python. See existing labs in `src/labs/owasp_ml_top10/`
for examples.

### 3. CTF Challenges
Capture-the-flag style puzzles. Each challenge has a hidden flag that players
extract by successfully exploiting an AI system vulnerability.

### 4. Bug Fixes & Security Issues
Found a bug? Report it via a GitHub Issue. Found a security vulnerability in
SK Framework itself? Email security@scriptkiddies.ai — do not open a public
issue.

---

## Code Standards

- **Python 3.10+** — use type hints everywhere
- **Black** for formatting: `black src/`
- **Ruff** for linting: `ruff check src/`
- **Pytest** for tests: all modules need at least one test
- **Docstrings** on every class and public method
- No print statements — use the logger: `from src.utils.logger import get_logger`

---

## Module Checklist

Before submitting a new attack module, verify:

- [ ] Extends `BaseModule` from `src/core/engine.py`
- [ ] Has a `__init__.py` with module metadata (name, version, OWASP mapping)
- [ ] Has at least one test in `tests/modules/`
- [ ] Has a docstring explaining what it attacks and how
- [ ] Includes a "defend against this" section in the docstring
- [ ] Does NOT hardcode any API keys
- [ ] Works with the unified LLM client (`src/utils/llm_client.py`)

---

## Lab Checklist

- [ ] Defined in YAML (see `labs/` for schema)
- [ ] Maps to a specific OWASP ML Top 10 item
- [ ] Has step-by-step instructions
- [ ] Has hints (progressive — don't give it away immediately)
- [ ] Has a solution writeup
- [ ] Has a difficulty rating (beginner / intermediate / advanced)

---

## Pull Request Process

1. Keep PRs focused — one feature or fix per PR
2. Update docs if you change behavior
3. CI must pass (tests + lint + type check)
4. At least one maintainer review before merge
5. Squash merge preferred

---

## Code of Conduct

SK Framework is an educational and defensive security project. All
contributions must be oriented toward learning and defense. We do not accept
modules designed to attack production systems without authorization.

Be respectful. Be helpful. Be curious.

---

## Questions?

Open a GitHub Discussion or reach out at hello@scriptkiddies.ai
