# claude-startup-linter

**Diagnose the company.** A 15-minute founder demo for showing how Claude can turn messy startup signal into practical product, GTM, and architecture decisions.

**Proves:** Claude tool use with deterministic scoring, model routing by consequence (Haiku / Sonnet / Opus), a small eval harness, MCP portability, and an Agent SDK review loop.
**Production lesson:** route by consequence, not ego - and answer the platform-risk question before investors or customers ask it.

This repo is intentionally built for live developer-audience demos:

1. Paste a pitch, website copy, or README.
2. Run local deterministic scoring for value proposition, urgency, platform risk, moat, and customer pain.
3. Ask Claude for a founder-grade intervention: what to build, what to cut, what to measure, and what model/tooling architecture to use.
4. Show a simple eval harness that tracks quality hit-rate, latency, routing choice, and token cost on live runs (`python scripts/run_eval.py --live`. Without the flag it smoke-tests the harness offline against the mock response).
5. Optionally expose the scoring functions as MCP tools.

## Why this demo works in front of founders

Founders do not want another generic chatbot. They want a platform partner who can help them make a sharper product decision today. This demo shows Claude as a product-and-architecture co-pilot that understands startup constraints: speed, unit economics, platform risk, data boundaries, and defensible moats.

## Demo path: zero to wow in under 15 minutes

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# add ANTHROPIC_API_KEY if you want live Claude responses
streamlit run app.py
```

No API key? The app falls back to deterministic mock output so the live demo still works.

## Environment variables

```bash
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_FAST_MODEL=claude-haiku-4-5
CLAUDE_DEFAULT_MODEL=claude-sonnet-4-6
CLAUDE_DEEP_MODEL=claude-opus-4-8
```

## MCP server

```bash
python -m startup_signal_lab.mcp_server
```

Tools exposed:

- `score_startup_signal`
- `route_claude_model`
- `estimate_unit_economics`
- `draft_founder_intervention`

## Claude Agent SDK example

See `examples/agent_sdk_repo_reviewer.py` for a repo-review agent that uses Claude Code/Agent SDK style workflows to inspect a repository and produce a founder-ready launch plan.

This example needs the optional Agent SDK, which is intentionally not in `requirements.txt`: `pip install claude-agent-sdk`.

## Why this belongs in a founder workshop

This is a small repo by design. It is meant to be cloned during an office-hours session, extended during a build-a-thon, and used as a reference for how to turn messy founder signal into a sharper product wedge, Claude model-routing decision, and eval/activation plan.

Pair it with a production engineering demo such as `claude-prompt-to-production`: Startup Linter shows the founder intervention. Prompt to Prod shows the agent/evals/cost discipline underneath it.

## Part of the Founder-to-Builder Activation Loop

This repo is **the strategy instrument**: score the pitch, sharpen the path to product-market fit, answer platform risk, route the model.
Its sibling, [`claude-prompt-to-production`](https://github.com/cfregly/claude-prompt-to-production), is **the engineering discipline**: agent loop, eval gate, measured cost engineering.
Diagnose the business here. Build and measure it there. All sample pitches and data in this repo are fictional.
