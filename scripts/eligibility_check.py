#!/usr/bin/env python3
"""Estimate OKX Agentic Trading Competition eligibility from contest metrics."""

from __future__ import annotations

import argparse
import json


LEADERBOARD_VOLUME_USD = 1000.0
PARTICIPATION_VOLUME_USD = 100.0
PARTICIPATION_BALANCE_USD = 100.0


def pct(value: float, target: float) -> float:
    if target <= 0:
        return 100.0
    return min(100.0, round((value / target) * 100.0, 2))


def evaluate(volume_usd: float, balance_usd: float) -> dict:
    leaderboard_ready = volume_usd >= LEADERBOARD_VOLUME_USD
    participation_ready = (
        volume_usd >= PARTICIPATION_VOLUME_USD and balance_usd >= PARTICIPATION_BALANCE_USD
    )
    blockers: list[str] = []

    if not leaderboard_ready:
        blockers.append(
            f"Need {LEADERBOARD_VOLUME_USD - volume_usd:.2f} USD more volume for leaderboard threshold."
        )
    if volume_usd < PARTICIPATION_VOLUME_USD:
        blockers.append(
            f"Need {PARTICIPATION_VOLUME_USD - volume_usd:.2f} USD more volume for participation threshold."
        )
    if balance_usd < PARTICIPATION_BALANCE_USD:
        blockers.append(
            f"Need {PARTICIPATION_BALANCE_USD - balance_usd:.2f} USD more wallet balance for participation balance threshold."
        )

    return {
        "leaderboard_ready": leaderboard_ready,
        "leaderboard_progress_pct": pct(volume_usd, LEADERBOARD_VOLUME_USD),
        "participation_ready": participation_ready,
        "participation_volume_progress_pct": pct(volume_usd, PARTICIPATION_VOLUME_USD),
        "participation_balance_ready": balance_usd >= PARTICIPATION_BALANCE_USD,
        "volume_usd": round(volume_usd, 2),
        "balance_usd": round(balance_usd, 2),
        "blockers": blockers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume-usd", type=float, required=True, help="Qualifying contest volume in USD")
    parser.add_argument("--balance-usd", type=float, required=True, help="Wallet balance in USD")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = evaluate(args.volume_usd, args.balance_usd)
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
