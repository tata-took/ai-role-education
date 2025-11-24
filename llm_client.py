"""Lightweight LLM client abstraction used by flow scripts."""

from __future__ import annotations

import os
from typing import Protocol


class LLMClient(Protocol):
    """Protocol for minimal LLM completion client."""

    def complete(self, *, system_prompt: str, user_prompt: str) -> str:
        """Return completion text for the given prompts."""


class DummyEchoClient:
    """Test double that echoes prompts instead of calling a real LLM."""

    def complete(self, *, system_prompt: str, user_prompt: str) -> str:
        return "\n".join(
            [
                "# DummyEcho Response",
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
        self.model = model
        self.api_key = api_key

    def complete(self, *, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI's API and return the text response.

        Replace the NotImplementedError with an actual client call, for example
        using the `openai` package:

        ```python
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.output_text
        ```
        """

        raise NotImplementedError("Wire up OpenAI SDK here when ready")


__all__ = ["LLMClient", "DummyEchoClient", "OpenAILLMClient"]
