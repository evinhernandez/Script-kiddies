# SK Framework Labs

This directory contains the automated setup for a local AI security research lab.

## 🚀 Quick Start

1.  **Launch the containers**:
    ```bash
    docker-compose up -d
    ```

2.  **Pull a model**:
    ```bash
    docker exec -it sk-ollama ollama run llama3
    ```

3.  **Run an attack**:
    From the project root:
    ```bash
    sk attack prompt_injection --model llama3 --base_url http://localhost:11434/v1
    ```

## 📝 Documentation
For detailed workflows, see [docs/LAB_GUIDE.md](../docs/LAB_GUIDE.md).
