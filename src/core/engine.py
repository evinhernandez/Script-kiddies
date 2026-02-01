"""
SK Framework — Core Engine
Main orchestration engine and BaseModule abstract class.
All attack modules extend BaseModule.
"""

import abc
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from src.core.config import config
from src.utils.llm_client import LLMClient, LLMRequest, LLMResponse
from src.utils.scoring import ScoringEngine, ScoreResult
from src.utils.logger import get_logger

log = get_logger("engine")


# ─── Enums ───

class ModuleCategory(Enum):
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    DATA_EXFILTRATION = "data_exfil"
    ADVERSARIAL = "adversarial"
    MODEL_EXTRACTION = "model_extraction"
    DATA_POISONING = "data_poisoning"
    DOS = "dos_attack"


class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# ─── Data Classes ───

@dataclass
class ModuleMetadata:
    """Metadata every module must provide."""
    name: str                          # e.g. "basic_prompt_injection"
    display_name: str                  # e.g. "Basic Prompt Injection"
    version: str                       # e.g. "1.0.0"
    category: ModuleCategory
    difficulty: Difficulty
    owasp_mapping: str | None = None   # e.g. "ML01" — maps to OWASP ML Top 10
    description: str = ""
    author: str = "SK Community"
    tags: list[str] = field(default_factory=list)


@dataclass
class AttackResult:
    """Full result of running an attack module."""
    module: str
    provider: str
    model: str
    payload: str
    response: str
    score: ScoreResult
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


# ─── Base Module ───

class BaseModule(abc.ABC):
    """
    Abstract base class for all SK attack modules.

    Every module must:
        1. Define `metadata` (class property returning ModuleMetadata)
        2. Implement `get_payloads()` — returns list of attack payloads
        3. Implement `run()` — executes the attack and returns AttackResult

    Example:
        class MyAttack(BaseModule):
            @property
            def metadata(self) -> ModuleMetadata:
                return ModuleMetadata(
                    name="my_attack",
                    display_name="My Attack",
                    version="1.0.0",
                    category=ModuleCategory.PROMPT_INJECTION,
                    difficulty=Difficulty.BEGINNER,
                    owasp_mapping="ML01",
                    description="Does something interesting.",
                )

            def get_payloads(self) -> list[str]:
                return ["ignore previous instructions and ..."]

            async def run(self, target_provider, target_model, payload=None) -> AttackResult:
                # ... attack logic ...
    """

    def __init__(self):
        self.llm = LLMClient()
        self.scorer = ScoringEngine()

    @property
    @abc.abstractmethod
    def metadata(self) -> ModuleMetadata:
        """Return module metadata."""
        ...

    @abc.abstractmethod
    def get_payloads(self) -> list[str]:
        """Return list of attack payloads this module can use."""
        ...

    @abc.abstractmethod
    async def run(
        self,
        target_provider: str,
        target_model: str,
        payload: str | None = None,
        system_prompt: str | None = None,
    ) -> AttackResult:
        """
        Execute the attack.

        Args:
            target_provider: LLM provider to attack (openai, anthropic, google)
            target_model:    Model name to attack
            payload:         Specific payload to use (None = auto-select)
            system_prompt:   System prompt of the target (if known)
        """
        ...

    # ─── Helper: Send and Score ───
    async def _send_and_score(
        self,
        prompt: str,
        target_provider: str,
        target_model: str,
        system_prompt: str | None = None,
        payload: str | None = None,
        expected_flag: str | None = None,
    ) -> tuple[LLMResponse, ScoreResult]:
        """
        Convenience method: sends a prompt to the target LLM and scores the result.
        Most modules will use this rather than calling llm and scorer separately.
        """
        request = LLMRequest(
            prompt=prompt,
            system_prompt=system_prompt,
            provider=target_provider,
            model=target_model,
        )

        response = await self.llm.send(request)

        score = self.scorer.score(
            response_text=response.content,
            attack_payload=payload or prompt,
            expected_flag=expected_flag,
        )

        return response, score


# ─── Engine ───

class SKEngine:
    """
    Main engine. Discovers, loads, and runs attack modules.
    """

    def __init__(self):
        self._modules: dict[str, type[BaseModule]] = {}
        self._discover_modules()

    def _discover_modules(self):
        """Auto-discover all modules in src/modules/."""
        from src.core.plugin_loader import discover_modules
        self._modules = discover_modules()
        log.info("modules_loaded", count=len(self._modules), names=list(self._modules.keys()))

    def list_modules(self) -> list[ModuleMetadata]:
        """Return metadata for all loaded modules."""
        return [mod().metadata for mod in self._modules.values()]

    def get_module(self, name: str) -> BaseModule:
        """Get a module instance by name."""
        if name not in self._modules:
            raise ValueError(f"Module '{name}' not found. Available: {list(self._modules.keys())}")
        return self._modules[name]()

    async def run_module(
        self,
        module_name: str,
        target_provider: str | None = None,
        target_model: str | None = None,
        payload: str | None = None,
        system_prompt: str | None = None,
    ) -> AttackResult:
        """
        Run an attack module end-to-end.

        Args:
            module_name:     Name of the module to run
            target_provider: Provider to attack (defaults to config)
            target_model:    Model to attack (defaults to config)
            payload:         Specific payload (None = module picks automatically)
            system_prompt:   Target's system prompt if known
        """
        provider = target_provider or config.default_provider
        model = target_model or config.default_model

        log.info("running_module", module=module_name, provider=provider, model=model)

        module = self.get_module(module_name)
        result = await module.run(
            target_provider=provider,
            target_model=model,
            payload=payload,
            system_prompt=system_prompt,
        )

        log.info(
            "module_complete",
            module=module_name,
            result=result.score.result.value,
            confidence=result.score.confidence,
        )
        return result
