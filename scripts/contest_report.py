#!/usr/bin/env python3
"""Generate a compact contest readiness report for demo and judging flows."""

from __future__ import annotations

import argparse
import json

from core import build_report


def parse_trade(value: str) -> tuple[str, str, str]:
    parts = [part.strip() for part in value.split(":")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Use CHAIN:FROM_TOKEN:TO_TOKEN, e.g. Solana:BONK:WIF")
    return parts[0], parts[1], parts[2]


def print_text(report: dict) -> None:
    status = report["contest_status"]
    summary = report["summary"]
    print("Contest Readiness Report")
    print(f"- Participation ready: {str(summary['participation_ready']).lower()}")
    print(f"- Leaderboard ready: {str(summary['leaderboard_ready']).lower()}")
    print(f"- Volume: ${status['volume_usd']:.2f}")
    print(f"- Balance: ${status['balance_usd']:.2f}")
    print(f"- Qualifying trade ideas: {summary['qualifying_trade_ideas']}")
    for blocker in status["blockers"]:
        print(f"- Blocker: {blocker}")
    print("")
    print("Trade Ideas")
    for trade in report["proposed_trades"]:
        pair = f"{trade['from_token']} -> {trade['to_token']}"
        print(f"- {trade['chain']} {pair}: {trade['status']}")
        for reason in trade["reasons"]:
            print(f"  Reason: {reason}")
    print("")
    print("Execution Gate")
    print("- Confirm token metadata, liquidity, route, simulation, and swap through onchainOS.")
    print("- Require explicit user confirmation before live execution.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume-usd", type=float, required=True)
    parser.add_argument("--balance-usd", type=float, required=True)
    parser.add_argument(
        "--trade",
        action="append",
        type=parse_trade,
        default=[],
        help="Proposed trade as CHAIN:FROM_TOKEN:TO_TOKEN. Repeatable.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report(args.volume_usd, args.balance_usd, args.trade)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
