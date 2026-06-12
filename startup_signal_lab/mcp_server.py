from __future__ import annotations

import json
from pathlib import Path

from .anthropic_client import analyze_pitch_with_claude
from .router import route_as_dict
from .scoring_tools import score_as_dict

try:
    from mcp.server.fastmcp import FastMCP
except Exception:  # pragma: no cover - optional dependency
    FastMCP = None  # type: ignore


def _load_pricing() -> dict:
    pricing_path = Path(__file__).resolve().parent.parent / "pricing.json"
    return json.loads(pricing_path.read_text())


def _estimate_unit_economics(
    input_tokens: int,
    output_tokens: int,
    requests_per_month: int,
    model: str = "claude-sonnet-4-6",
) -> dict:
    pricing = _load_pricing()
    model_pricing = pricing["models"].get(model)
    if model_pricing is None:
        return {"error": f"unknown model '{model}'", "valid_models": sorted(pricing["models"])}
    input_cost_per_mtok = model_pricing["input_per_mtok"]
    output_cost_per_mtok = model_pricing["output_per_mtok"]
    input_cost = (input_tokens * requests_per_month / 1_000_000) * input_cost_per_mtok
    output_cost = (output_tokens * requests_per_month / 1_000_000) * output_cost_per_mtok
    total = input_cost + output_cost
    return {
        "model": model,
        "monthly_input_cost_usd": round(input_cost, 2),
        "monthly_output_cost_usd": round(output_cost, 2),
        "monthly_total_cost_usd": round(total, 2),
        "cost_per_request_usd": round(total / max(1, requests_per_month), 6),
        "pricing_note": pricing.get("_verify", "Verify pricing before quoting."),
    }


if FastMCP is not None:
    mcp = FastMCP("claude-startup-linter")

    @mcp.tool()
    def score_startup_signal(pitch: str) -> str:
        """Score value prop, urgency, differentiation, platform risk, distribution, and data boundary."""
        return json.dumps(score_as_dict(pitch), indent=2)

    @mcp.tool()
    def route_claude_model(task: str, risk: str = "medium", context_tokens: int = 8000) -> str:
        """Choose a Claude model based on task complexity, risk, and context size."""
        return json.dumps(route_as_dict(task, risk, context_tokens), indent=2)

    @mcp.tool()
    def estimate_unit_economics(input_tokens: int, output_tokens: int, requests_per_month: int, model: str = "claude-sonnet-4-6") -> str:
        """Estimate monthly cost and per-request cost for a Claude workload using pricing.json."""
        return json.dumps(_estimate_unit_economics(input_tokens, output_tokens, requests_per_month, model), indent=2)

    @mcp.tool()
    def draft_founder_intervention(pitch: str) -> str:
        """Draft a founder intervention: value prop, wedge, architecture, platform risk, and metrics."""
        result = analyze_pitch_with_claude(pitch, live=True)
        return result["response"]
else:
    mcp = None


def main() -> None:
    if mcp is None:
        raise RuntimeError("mcp package not installed. Run: pip install mcp")
    mcp.run()


if __name__ == "__main__":
    main()
