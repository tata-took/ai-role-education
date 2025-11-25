"""Lightweight LLM client abstraction used by flow scripts."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

import yaml


def load_model_config() -> dict:
    """Load role-specific model configuration from config/models.yaml."""

    config_path = Path(__file__).parent / "config" / "models.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_MODEL_CONFIG: dict | None = None


def get_model_settings(role_name: str) -> dict:
    """Return model settings for a role, falling back to default."""

    global _MODEL_CONFIG
    if _MODEL_CONFIG is None:
        _MODEL_CONFIG = load_model_config()

    if role_name in _MODEL_CONFIG:
        return _MODEL_CONFIG[role_name]
    return _MODEL_CONFIG.get("default", {})


class LLMClient(Protocol):
    """Protocol for minimal LLM completion client."""

    def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """Return completion text for the given prompts."""


class DummyEchoClient:
    """Test double that echoes prompts instead of calling a real LLM."""

    def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        temperature: float | None = None,
    ) -> str:
        header_parts = []
        if model:
            header_parts.append(f"model={model}")
        if temperature is not None:
            header_parts.append(f"temperature={temperature}")
        header = f"# DummyEcho Response ({', '.join(header_parts)})" if header_parts else "# DummyEcho Response"
        return "\n".join(
            [
                header,
                "## System Prompt",
                system_prompt,
                "",
                "## User Prompt",
                user_prompt,
            ]
        )


class OpenAILLMClient:
    """Example skeleton for a production LLM client (OpenAI)."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY is not set")
        self.default_model = model
        self.api_key = api_key

    def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """Call OpenAI's API and return the text response.

        Replace the NotImplementedError with an actual client call, for example
        using the `openai` package:

        ```python
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model=model or self.default_model,
            temperature=temperature,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.output_text
        ```
        """

        raise NotImplementedError("Wire up OpenAI SDK here when ready")


def get_llm_client(provider: str) -> LLMClient:
    """Return an LLM client implementation for the given provider."""

    if provider == "openai":
        return OpenAILLMClient()
    raise NotImplementedError(f"Provider '{provider}' is not supported yet")


__all__ = [
    "LLMClient",
    "DummyEchoClient",
    "OpenAILLMClient",
    "get_model_settings",
    "get_llm_client",
    "load_model_config",
]
