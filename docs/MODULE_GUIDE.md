# Developer Guide: Building Exploit Modules

SK Framework is designed to be fully extensible. You can add new attack vectors simply by dropping a Python file into `src/modules/`.

---

## 🏗️ Module Structure

Every module must inherit from `BaseModule` and implement a few core methods.

### 1. Metadata
Defines how the module appears in the console.
```python
@property
def metadata(self) -> ModuleMetadata:
    return ModuleMetadata(
        name="my_exploit",
        display_name="My Custom Exploit",
        version="1.0.0",
        category=ModuleCategory.PROMPT_INJECTION,
        difficulty=Difficulty.BEGINNER,
        description="Detailed description here.",
        tags=["custom", "new-vector"]
    )
```

### 2. Options
Defines the configurable parameters (variables) for the module.
```python
def get_options(self) -> list[ModuleOption]:
    return [
        ModuleOption(name="TARGET", default="openai", required=True),
        ModuleOption(name="CUSTOM_PARAM", default="value", description="Explanation")
    ]
```

### 3. The `run` Method
The core logic of your attack. Use `self._send_and_score()` for a standard "Send prompt -> Get Score" flow.
```python
async def run(self, target_provider, target_model, **kwargs) -> AttackResult:
    payload = "Your attack string here."
    
    # Sends payload to the target and runs the heuristic scoring engine
    response, score = await self._send_and_score(
        prompt=payload,
        target_provider=target_provider,
        target_model=target_model
    )
    
    return AttackResult(
        module=self.metadata.name,
        provider=target_provider,
        model=target_model,
        payload=payload,
        response=response.content,
        score=score
    )
```

---

## 🛠️ Best Practices

1.  **Use `self.log`**: For structured logging that appears in the Cinematic Dashboard.
2.  **Handle Multi-turn**: If your exploit requires interaction, use the `AgentDeployer` (see `src/modules/system_prompt_extraction/` for reference).
3.  **Heuristic Scoring**: Add new "Critical Signals" to `src/utils/scoring.py` if your exploit extracts a specific format (like a token or API key).

---

## 🧪 Testing Your Module

Restart `skconsole` and your new module will be auto-discovered:
```bash
skconsole
sk> use my_exploit
sk(my_exploit)> show options
sk(my_exploit)> run
```
