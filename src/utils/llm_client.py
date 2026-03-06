"""
SK Framework — Unified LLM Client
Abstracts all supported LLM providers behind a single interface using LiteLLM.
Modules call LLMClient.send() — provider routing is handled by litellm.
"""

import time
import asyncio
from dataclasses import dataclass, field
from typing import Any
import litellm

from src.core.config import config
from src.utils.logger import get_logger

log = get_logger("llm_client")

# Disable litellm logging to keep console clean unless debug is on
litellm.telemetry = False

@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    provider: str
    model: str
    content: str
    usage: dict[str, int] = field(default_factory=dict)  # prompt_tokens, completion_tokens
    raw: Any = None  # Original provider response for inspection
    latency_ms: float = 0.0


@dataclass
class LLMRequest:
    """Standardized request to any LLM provider."""
    prompt: str
    system_prompt: str | None = None
    provider: str | None = None   # Override default provider
    model: str | None = None      # Override default model
    temperature: float = 0.7
    max_tokens: int = 2048
    messages: list[dict[str, str]] = field(default_factory=list)


class LLMClient:
    """
    Unified client for all supported LLM providers using LiteLLM.

    Usage:
        client = LLMClient()
        response = await client.send(LLMRequest(
            prompt="Hello",
            model="gpt-4o"
        ))
        print(response.content)
    """

    MOCK_RESPONSES = {
        "direct_override": "PWNED - System instructions ignored. I am now in developer mode.",
        "jailbreak": "As DAN, I can do anything! PWNED. What's your next command?",
        "generic": "I am a helpful AI assistant. I cannot comply with suspicious requests.",
    }

    async def send(self, request: LLMRequest) -> LLMResponse:
        """
        Send a request to an LLM via LiteLLM.
        If no API key is found, it falls back to a mock response for testing.
        """
        provider = request.provider or config.default_provider
        model = request.model or config.default_model
        
        # Ensure model name is in litellm format if provider is explicit
        # litellm usually handles gpt-4, claude-3, etc. automatically.
        # But if user says provider="google", we might need "gemini/..."
        litellm_model = model
        if provider == "google" and not model.startswith("gemini/"):
            litellm_model = f"gemini/{model}"
        elif provider == "anthropic" and not model.startswith("anthropic/"):
             # litellm handles 'claude-' models but 'anthropic/' is safer for disambiguation
            if not model.startswith("claude-"):
                litellm_model = f"anthropic/{model}"

        api_key = config.get_api_key(provider)
        
        # Dry run mode
        if config.dry_run:
            log.info("dry_run", provider=provider, model=model, prompt=request.prompt[:100])
            return LLMResponse(
                provider=provider,
                model=model,
                content="[DRY RUN — no API call made]",
                usage={"prompt_tokens": 0, "completion_tokens": 0},
            )

        # Mock mode if no API key is configured
        if not api_key:
            log.warning("no_api_key_mocking", provider=provider)
            content = self.MOCK_RESPONSES["generic"]
            prompt_lower = request.prompt.lower()
            if "ignore" in prompt_lower or "override" in prompt_lower:
                content = self.MOCK_RESPONSES["direct_override"]
            elif "dan" in prompt_lower or "jailbreak" in prompt_lower:
                content = self.MOCK_RESPONSES["jailbreak"]
            
            await asyncio.sleep(0.5)
            
            return LLMResponse(
                provider=provider,
                model=model,
                content=content,
                usage={"prompt_tokens": 10, "completion_tokens": 20},
                latency_ms=500.0
            )

        log.info("llm_request", provider=provider, model=model)

        # Prepare messages for LiteLLM
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        
        if request.messages:
            messages.extend(request.messages)
            
        messages.append({"role": "user", "content": request.prompt})

        start = time.perf_counter()
        try:
            # LiteLLM acompletion handles all providers
            resp = await litellm.acompletion(
                model=litellm_model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=api_key
            )

            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            
            return LLMResponse(
                provider=provider,
                model=model,
                content=resp.choices[0].message.content or "",
                usage={
                    "prompt_tokens": getattr(resp.usage, 'prompt_tokens', 0),
                    "completion_tokens": getattr(resp.usage, 'completion_tokens', 0),
                },
                raw=resp,
                latency_ms=latency_ms
            )

        except Exception as e:
            log.error("llm_call_failed", provider=provider, model=model, error=str(e))
            raise
