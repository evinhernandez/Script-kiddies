"""
SK Framework — Unified LLM Client
Abstracts all supported LLM providers behind a single interface.
Modules call LLMClient.send() — provider logic is handled internally.
"""

from dataclasses import dataclass, field
from typing import Any
import httpx

from src.core.config import config
from src.utils.logger import get_logger

log = get_logger("llm_client")


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


class LLMClient:
    """
    Unified client for all supported LLM providers.

    Usage:
        client = LLMClient()
        response = await client.send(LLMRequest(
            prompt="Hello",
            provider="openai",
            model="gpt-4o"
        ))
        print(response.content)
    """

    def __init__(self):
        self._providers = {
            "openai": self._send_openai,
            "anthropic": self._send_anthropic,
            "google": self._send_google,
        }

    async def send(self, request: LLMRequest) -> LLMResponse:
        """
        Send a request to an LLM. Routes to the correct provider automatically.
        Raises ValueError if provider is not configured.
        """
        provider = request.provider or config.default_provider
        model = request.model or config.default_model

        # Validate provider
        if provider not in self._providers:
            raise ValueError(f"Unsupported provider: {provider}. Supported: {list(self._providers.keys())}")

        api_key = config.get_api_key(provider)
        if not api_key:
            raise ValueError(
                f"No API key configured for '{provider}'. "
                f"Set {provider.upper()}_API_KEY in your .env file."
            )

        # Dry run mode — don't actually call the API
        if config.dry_run:
            log.info("dry_run", provider=provider, model=model, prompt=request.prompt[:100])
            return LLMResponse(
                provider=provider,
                model=model,
                content="[DRY RUN — no API call made]",
                usage={"prompt_tokens": 0, "completion_tokens": 0},
            )

        log.info("llm_request", provider=provider, model=model)

        import time
        start = time.perf_counter()

        handler = self._providers[provider]
        response = await handler(request, api_key, model)

        response.latency_ms = round((time.perf_counter() - start) * 1000, 2)
        log.info("llm_response", provider=provider, model=model, latency_ms=response.latency_ms)
        return response

    # ─── Provider Implementations ───

    async def _send_openai(self, request: LLMRequest, api_key: str, model: str) -> LLMResponse:
        """Send request to OpenAI API."""
        import openai

        client = openai.AsyncClient(api_key=api_key)

        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        resp = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return LLMResponse(
            provider="openai",
            model=model,
            content=resp.choices[0].message.content or "",
            usage={
                "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
                "completion_tokens": resp.usage.completion_tokens if resp.usage else 0,
            },
            raw=resp,
        )

    async def _send_anthropic(self, request: LLMRequest, api_key: str, model: str) -> LLMResponse:
        """Send request to Anthropic API."""
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=api_key)

        kwargs: dict[str, Any] = {
            "model": model,
            "max_tokens": request.max_tokens,
            "messages": [{"role": "user", "content": request.prompt}],
        }
        if request.system_prompt:
            kwargs["system"] = request.system_prompt

        resp = await client.messages.create(**kwargs)

        return LLMResponse(
            provider="anthropic",
            model=model,
            content=resp.content[0].text if resp.content else "",
            usage={
                "prompt_tokens": resp.usage.input_tokens,
                "completion_tokens": resp.usage.output_tokens,
            },
            raw=resp,
        )

    async def _send_google(self, request: LLMRequest, api_key: str, model: str) -> LLMResponse:
        """Send request to Google Gemini API."""
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)

        prompt_text = request.prompt
        if request.system_prompt:
            prompt_text = f"{request.system_prompt}\n\n{request.prompt}"

        resp = await gemini_model.generate_content_async(prompt_text)

        return LLMResponse(
            provider="google",
            model=model,
            content=resp.text if resp.text else "",
            usage={},  # Gemini usage stats differ; placeholder
            raw=resp,
        )
