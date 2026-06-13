from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import pathlib
import re
from typing import Any


@dataclass(frozen=True)
class StartupSignalScore:
    value_prop: int
    urgency: int
    differentiation: int
    platform_risk: int
    distribution: int
    data_boundary: int
    overall: int
    flags: list[str]
    suggested_wedge: str


def _has_any(text: str, patterns: list[str]) -> bool:
    t = text.lower()
    return any(p in t for p in patterns)


# Buzzwords that spend words without carrying signal. Slop costs a point because
# adjectives displace numbers. The shared canon (buzzword stems plus filler
# phrases) loads from slop_rules.json, synced from the claude-deslop repo; do
# not hand-edit it. Stems like "leverag" match as substrings.
_RULES = json.loads((pathlib.Path(__file__).parent / "slop_rules.json").read_text())
SLOP_TERMS = _RULES["buzzwords"] + _RULES["phrases"]


def _count_specifics(text: str) -> int:
    # A rough proxy for concrete claims: numbers, named buyers, before/after, integrations.
    return len(re.findall(r"\b\d+(?:\.\d+)?%?|\$\d+|[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)+\b", text))


def clamp(value: int, low: int = 1, high: int = 10) -> int:
    return max(low, min(high, value))


def score_startup_signal(text: str) -> StartupSignalScore:
    """Score a startup pitch for founder-facing intervention.

    Scores are intentionally simple and explainable for live demos. In production,
    combine deterministic checks with Claude-as-judge evals and founder outcomes.
    """
    if not text or len(text.strip()) < 20:
        return StartupSignalScore(
            value_prop=1,
            urgency=1,
            differentiation=1,
            platform_risk=9,
            distribution=1,
            data_boundary=1,
            overall=1,
            flags=["Not enough signal to evaluate."],
            suggested_wedge="Start with a one-sentence painkiller claim for a specific buyer.",
        )

    specifics = _count_specifics(text)
    value_prop = 4 + min(3, specifics // 2)
    urgency = 4
    differentiation = 4
    platform_risk = 5
    distribution = 4
    data_boundary = 4
    flags: list[str] = []

    if _has_any(text, ["save", "reduce", "faster", "latency", "cost", "revenue", "conversion", "payback"]):
        value_prop += 2
        urgency += 1
    else:
        flags.append("Value proposition needs a measurable before/after claim.")

    if _has_any(text, ["compliance", "regulated", "audit", "security", "privacy", "pii", "hipaa", "soc 2", "sox"]):
        data_boundary += 3
        urgency += 1

    if _has_any(text, ["openai", "anthropic", "claude", "gemini", "cloud", "aws", "bedrock", "azure"]):
        platform_risk += 2
        flags.append("Explicit platform-risk story required: why won't the model/cloud platform absorb this?")

    if _has_any(text, ["proprietary data", "workflow", "system of record", "network", "feedback loop", "usage data"]):
        differentiation += 3
    else:
        flags.append("Moat is not yet obvious; explain what compounds with each user or workflow.")

    if _has_any(text, ["yc", "design partner", "pilot", "customer", "paid", "usage", "arr", "retention"]):
        distribution += 3
    else:
        flags.append("Distribution path is fuzzy; name the first 25 buyers and the activation event.")

    if _has_any(text, ["always-on", "embedded", "inline", "copilot", "agent", "mcp", "ci", "ide"]):
        differentiation += 1
        value_prop += 1

    slop_hits = [t for t in SLOP_TERMS if t in text.lower()]
    if slop_hits:
        value_prop -= 1
        flags.append(
            "De-slop the pitch: buzzwords carry no signal ("
            + ", ".join(slop_hits[:3])
            + "); replace each with a number or a named workflow."
        )

    value_prop = clamp(value_prop)
    urgency = clamp(urgency)
    differentiation = clamp(differentiation)
    platform_risk = clamp(platform_risk)
    distribution = clamp(distribution)
    data_boundary = clamp(data_boundary)
    # Platform risk is inverted in the overall score: lower risk is better.
    overall = round((value_prop + urgency + differentiation + distribution + data_boundary + (11 - platform_risk)) / 6)

    if overall >= 8:
        wedge = "Double down on the narrow wedge; show the fastest path from first use to weekly habit."
    elif differentiation >= 7 and distribution <= 5:
        wedge = "The product may be sharp, but GTM is the bottleneck; define the partner/channel motion."
    elif platform_risk >= 7:
        wedge = "Lead with platform-risk mitigation: data, workflow ownership, evals, and customer-specific integrations."
    else:
        wedge = "Narrow the buyer and convert the pitch from category language to a painful operational metric."

    return StartupSignalScore(
        value_prop=value_prop,
        urgency=urgency,
        differentiation=differentiation,
        platform_risk=platform_risk,
        distribution=distribution,
        data_boundary=data_boundary,
        overall=overall,
        flags=flags,
        suggested_wedge=wedge,
    )


def score_as_dict(text: str) -> dict[str, Any]:
    return asdict(score_startup_signal(text))
