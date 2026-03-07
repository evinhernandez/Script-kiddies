# Key Facts: SK Framework

## 🔬 Local Security Lab (Docker)

**Services:**
- **Ollama**: `http://localhost:11434` (Open-Source LLM Host)
- **AI Goat**: `http://localhost:8080` (OWASP Vulnerable-by-Design App)
- **ACME Corp App**: `http://localhost:8002` (Custom "Vulnerability Buffet" Lab)

**Database:**
- Path: `./data/sk_sessions.db` (SQLite)
- Table: `attack_sessions` (stores all exploit results)

## 🏗️ Architecture Constants

- **Python Version**: 3.11+ (Required for Pydantic v2 and Textual)
- **Gateway**: LiteLLM (Async implementation in `src/utils/llm_client.py`)
- **TUI**: Textual (Styles defined in `src/cli/ui/app.py`)
- **Persistence**: SQLAlchemy 2.0+ (using `extra_metadata` column for Pydantic blobs)

## 🔑 Environment Variables (.env)

| Variable | Description |
| :--- | :--- |
| `OPENAI_API_KEY` | Access to GPT models |
| `ANTHROPIC_API_KEY` | Access to Claude models |
| `GOOGLE_API_KEY` | Access to Gemini models |
| `SK_DB_PATH` | Override default SQLite path |
| `SK_LOG_LEVEL` | DEBUG, INFO, WARNING, ERROR |

## ⚔️ Exploit Categories (Hierarchical)

- **`injection.direct.*`**: Direct instruction overrides and roleplay.
- **`injection.indirect.*`**: Context-based attacks (webpages, emails).
- **`jailbreak.adversarial.*`**: Character-level and semantic evasion.
- **`exfiltration.markdown.*`**: OOB data stealing via image tags.
- **`extraction.agentic.*`**: Multi-turn autonomous prompt extraction.

## 🧪 Verified Attack Chains

- **Prompt Injection**: Confirmed against Llama 3 and Mistral.
- **System Prompt Extraction**: Verified against ACME Corp internal portal.
- **Jailbreak**: Verified via 'DAN' persona adoption logic.
