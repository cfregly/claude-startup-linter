"""Claude Agent SDK example: repo reviewer for founder demos.

Run this after installing the Claude Agent SDK and setting ANTHROPIC_API_KEY.
It asks Claude to inspect the current repository and produce a founder-ready launch plan.
"""

from __future__ import annotations

import asyncio

try:
    from claude_agent_sdk import ClaudeAgentOptions, query
except Exception as exc:  # pragma: no cover
    raise SystemExit("Install claude-agent-sdk first: pip install claude-agent-sdk") from exc


PROMPT = """
Review this repository as if I am about to demo it to technical founders.
Return:
1. The 15-minute demo flow.
2. The strongest Claude-specific proof points.
3. Three improvements to make it more production credible.
4. A README patch if needed.
""".strip()


async def main() -> None:
    options = ClaudeAgentOptions(allowed_tools=["Read", "Grep", "Glob", "Edit", "Bash"])
    async for message in query(prompt=PROMPT, options=options):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
