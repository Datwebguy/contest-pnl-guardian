#!/usr/bin/env python3
"""Estimate OKX Agentic Trading Competition eligibility from contest metrics."""

from __future__ import annotations

import argparse
import json

from core import evaluate_eligibility


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume-usd", type=float, required=True, help="Qualifying contest volume in USD")
    parser.add_argument("--balance-usd", type=float, required=True, help="Wallet balance in USD")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = evaluate_eligibility(args.volume_usd, args.balance_usd)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Contest Status")
        print(f"- Leaderboard: {'ready' if result['leaderboard_ready'] else 'not ready'}")
        print(f"- Leaderboard progress: {result['leaderboard_progress_pct']}%")
        print(f"- Participation: {'ready' if result['participation_ready'] else 'not ready'}")
        print(f"- Participation volume progress: {result['participation_volume_progress_pct']}%")
        print(f"- Participation balance: {'ready' if result['participation_balance_ready'] else 'not ready'}")
        for blocker in result["blockers"]:
            print(f"- {blocker}")
    return 0 if result["participation_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
