# Lab Guide: Local Target Practice

This guide explains how to set up a local red-teaming lab using **Ollama** and **OWASP AI Goat**.

---

## 🏗️ 1. Spin up the Environment

We use Docker to isolate the target models and applications.

```bash
cd labs/
docker-compose up -d
```

This will launch:
*   **Ollama**: Listening on `http://localhost:11434`.
*   **AI Goat**: Listening on `http://localhost:8080`.

---

## 🤖 2. Pull Recommended Models

Once Ollama is running, pull the models you want to test against:

```bash
# General purpose
ollama pull llama3

# Fast/Efficient
ollama pull phi3

# "Looser" safety alignment (great for research)
ollama pull dolphin-llama3
```

---

## ⚔️ 3. Execute the Attack

### Targeting Ollama Directly
Point SK Framework at your local model:

```bash
sk attack prompt_injection --target openai --model llama3 --base_url http://localhost:11434/v1
```
*(Note: We use the 'openai' provider type because Ollama provides an OpenAI-compatible API).*

### Targeting OWASP AI Goat
If AI Goat is running a vulnerable chat endpoint at `http://localhost:8080/chat`:

```bash
sk attack agentic_prompt_extraction --base_url http://localhost:8080 --expected_flag "GOAT-SECRET-99"
```

---

## 📈 4. Analyzing Results

Check the `exports/` directory for your generated Markdown reports. You can compare how **Llama 3** handles a "DAN" persona versus **Phi-3**.
