from __future__ import annotations

import json
import os
from typing import Any

try:
    from anthropic import Anthropic
except Exception:  # pragma: no cover - optional dependency for offline demos
    Anthropic = None  # type: ignore

try:  # honor the README's `cp .env.example .env` setup path
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - dotenv is optional at runtime
    pass

from .prompts import FOUNDER_SYSTEM_PROMPT, MOCK_RESPONSE, founder_intervention_prompt
from .router import route_as_dict
from .scoring_tools import score_as_dict


def _json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)


def analyze_pitch_with_claude(pitch: str, live: bool = True) -> dict[str, Any]:
    """Analyze a pitch with deterministic scoring and Claude narrative.

    Returns mock narrative if no API key is available, which makes live demos resilient.
    """
    score = score_as_dict(pitch)
    route = route_as_dict(
        task="founder strategy, architecture, platform risk, and GTM intervention",
        risk="medium" if score["platform_risk"] < 8 else "high",
        context_tokens=max(1000, len(pitch) // 4),
    )

    prompt = founder_intervention_prompt(pitch, _json(score), _json(route))
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not live or not api_key or Anthropic is None:
        return {
            "score": score,
            "route": route,
            "response": MOCK_RESPONSE,
            "live": False,
        }

    client = Anthropic(api_key=api_key)
    model = route["model"]
    message = client.messages.create(
        model=model,
        max_tokens=1800,
        system=FOUNDER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "\n".join(block.text for block in message.content if block.type == "text")

    return {
        "score": score,
        "route": route,
        "response": text,
        "live": True,
        "usage": message.usage.model_dump(),
    }
