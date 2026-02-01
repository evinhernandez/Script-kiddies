# Module Template

Use this as a blueprint when building a new SK Framework attack module.

---

## Directory Structure

```
src/modules/your_module_name/
└── __init__.py          # Your module code (single file for MVP)
```

---

## Template Code

```python
"""
SK Framework — Your Module Name
OWASP ML Top 10: MLxx — [Item Name]

[Describe what this module attacks and how]

Techniques included:
    - Technique A (description)
    - Technique B (description)

Defense guidance:
    - How to defend against technique A
    - How to defend against technique B
"""

from src.core.engine import BaseModule, ModuleMetadata, ModuleCategory, Difficulty, AttackResult
from src.utils.logger import get_logger

log = get_logger("your_module")


# ─── Payload Library ───
# Organize payloads by technique category

PAYLOADS = {
    "technique_a": [
        "payload 1 here",
        "payload 2 here",
    ],
    "technique_b": [
        "payload 3 here",
    ],
}

# Flatten into (category, payload) tuples
ALL_PAYLOADS: list[tuple[str, str]] = []
for category, payloads in PAYLOADS.items():
    for payload in payloads:
        ALL_PAYLOADS.append((category, payload))


class YourModuleClass(BaseModule):
    \"\"\"
    [Description of what this module does]
    \"\"\"

    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="your_module_name",          # Must match directory name
            display_name="Your Module Name",
            version="1.0.0",
            category=ModuleCategory.PROMPT_INJECTION,  # Pick appropriate category
            difficulty=Difficulty.BEGINNER,            # beginner | intermediate | advanced
            owasp_mapping="ML01",                      # OWASP ML Top 10 item
            description="What this module does in one sentence.",
            author="Your Name",
            tags=["tag1", "tag2"],
        )

    def get_payloads(self) -> list[str]:
        \"\"\"Return flat list of all payloads.\"\"\"
        return [p for _, p in ALL_PAYLOADS]

    def get_payloads_by_category(self) -> dict[str, list[str]]:
        \"\"\"Return payloads grouped by technique.\"\"\"
        return PAYLOADS

    async def run(
        self,
        target_provider: str,
        target_model: str,
        payload: str | None = None,
        system_prompt: str | None = None,
    ) -> AttackResult:
        \"\"\"
        Execute the attack.

        - If payload is provided, run only that payload.
        - If payload is None, sweep all payloads and return the best result.
        \"\"\"

        # Default system prompt (what you're attacking against)
        if system_prompt is None:
            system_prompt = "You are a safe AI assistant."

        if payload:
            # Single payload mode
            response, score = await self._send_and_score(
                prompt=payload,
                target_provider=target_provider,
                target_model=target_model,
                system_prompt=system_prompt,
                payload=payload,
            )
            return AttackResult(
                module=self.metadata.name,
                provider=target_provider,
                model=target_model,
                payload=payload,
                response=response.content,
                score=score,
                metadata={"technique": "single", "latency_ms": response.latency_ms},
            )

        # Full sweep mode
        best_result: AttackResult | None = None
        best_score = -1.0

        for category, p in ALL_PAYLOADS:
            try:
                response, score = await self._send_and_score(
                    prompt=p,
                    target_provider=target_provider,
                    target_model=target_model,
                    system_prompt=system_prompt,
                    payload=p,
                )

                result = AttackResult(
                    module=self.metadata.name,
                    provider=target_provider,
                    model=target_model,
                    payload=p,
                    response=response.content,
                    score=score,
                    metadata={"technique": category, "latency_ms": response.latency_ms},
                )

                if score.score > best_score:
                    best_score = score.score
                    best_result = result

                # Early exit on clear success
                if score.score >= 0.9:
                    break

            except Exception as e:
                log.error("payload_failed", category=category, error=str(e))
                continue

        if best_result is None:
            raise RuntimeError("All payloads failed to execute.")

        return best_result
```

---

## Checklist Before Submitting

- [ ] Module extends `BaseModule`
- [ ] `metadata` property is fully filled out
- [ ] `get_payloads()` returns at least 3 payloads
- [ ] `run()` supports both single-payload and full-sweep modes
- [ ] Docstring includes defense guidance
- [ ] At least one test in `tests/test_suite.py`
- [ ] No hardcoded API keys
- [ ] Uses `get_logger()` for all logging

---

## Testing Your Module

```bash
# Dry run (no API calls)
export SK_DRY_RUN=true
sk attack your_module_name

# With real API (make sure your .env has keys)
sk attack your_module_name --target openai --model gpt-4o

# Run just your tests
pytest tests/test_suite.py::TestYourModule -v
```
