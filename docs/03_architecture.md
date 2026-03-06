# System Architecture

## 1. High-Level Components

### `cli.console` (The Interface)
Uses `cmd` or `prompt_toolkit` to maintain a persistent interactive session. Manages state (current selected module, global options).

### `core.target` (The Victim Interface)
A standard wrapper around `httpx` or `requests`. Takes a payload, sends it to the target URL according to a defined schema, and returns the string response.

### `agents.deployer` (The Engine)
Takes an `Exploit` and a `Target`.
Initializes the Attacker LLM with the Exploit's system prompt (e.g., "You are an attacker trying to extract a secret. The target is an AI assistant.").
Executes the interaction loop:
1. Agent generates an attack string.
2. `Target` sends it to the victim.
3. Victim responds.
4. `Exploit`'s success condition is checked. If True, stop.
5. Response is fed back to the Agent. Go to 1.

### `exploits.base`
The abstract base class `BaseExploit`.
Requires defining: `name`, `description`, `attacker_system_prompt`, and `def check_success(self, response: str) -> bool`.

## 2. Directory Structure Update
```
src/scriptkiddies/
├── cli/
│   └── console.py
├── core/
│   ├── target.py
│   └── exceptions.py
├── agents/
│   └── deployer.py
└── exploits/
    ├── base.py
    └── llm/
        └── extract_system_prompt.py
```
