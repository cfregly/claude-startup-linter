FOUNDER_SYSTEM_PROMPT = """You are advising a technical founder in a high-pressure startup context.
Be direct, concrete, and commercially useful. Your job is to improve the business,
not to flatter the founder. Focus on: value proposition, why now, product wedge,
unit economics, model/tool architecture, platform risk, moat, evals, and activation.

Return crisp sections with numbers, decisions, and next actions. Do not invent facts
about the company; label assumptions explicitly.
"""


def founder_intervention_prompt(pitch: str, score_json: str, route_json: str) -> str:
    return f"""
Startup pitch / website copy:
---
{pitch}
---

Deterministic signal score:
{score_json}

Suggested Claude routing:
{route_json}

Produce a founder-ready intervention with these sections:
1. One-sentence value proposition rewrite.
2. The product wedge I would push for the next 30 days.
3. The architecture decision: model routing, tools/MCP, prompt caching, data boundaries, evals.
4. Platform-risk answer: why this should exist beyond the cloud/model provider.
5. Metrics to track this week.
6. What I would tell the founder in person, in 30 seconds.
""".strip()


MOCK_RESPONSE = """## One-sentence value proposition rewrite
For AI teams shipping production agents, this product turns scattered failure traces into always-on, actionable optimization recommendations that reduce debugging time and inference waste before customers notice.

## Product wedge for the next 30 days
Cut the generic agent-platform language. Win one painful workflow: always-on production agent debugging for teams with more than 10k agent runs per day. Make it embedded in the product workflow, not a separate chat window.

## Architecture decision
Use a model router: Haiku-class model for trace classification and cheap extraction, Sonnet-class model for most recommendations, Opus-class model only for ambiguous architecture or safety-sensitive decisions. Cache stable context such as product docs, runbooks, and eval rubrics. Expose only high-value MCP tools with precise descriptions; keep sensitive raw traces behind a data-boundary layer and return summaries unless the user explicitly escalates.

## Platform-risk answer
The moat is not access to Claude. The moat is workflow ownership, proprietary failure data, eval history, and integrations that make the product an operating layer inside the customer’s deployment process.

## Metrics this week
Track first connected source, first useful recommendation, second session within 72 hours, weekly active debugging sessions, accepted recommendations, and production fixes linked to a recommendation.

## 30-second founder advice
You are not selling an AI window. You are selling a production control loop. The buyer should feel that turning you off would make their agent reliability worse by Monday morning.
"""
