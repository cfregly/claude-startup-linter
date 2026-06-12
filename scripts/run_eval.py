from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python scripts/run_eval.py` from the repo root without an install step.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from startup_signal_lab.evals import run_evals  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Startup Linter eval suite.")
    parser.add_argument(
        "--live",
        action="store_true",
        help="grade real Claude responses (requires ANTHROPIC_API_KEY); default is an offline smoke test of the harness against the mock response",
    )
    args = parser.parse_args()
    print(json.dumps(run_evals(live=args.live), indent=2))
