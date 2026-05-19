#!/usr/bin/env python3
"""Generate a compact contest readiness report for demo and judging flows."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode not in (0, 1, 2):
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return json.loads(completed.stdout)


def parse_trade(value: str) -> tuple[str, str, str]:
    parts = [part.strip() for part in value.split(":")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Use CHAIN:FROM_TOKEN:TO_TOKEN, e.g. Solana:BONK:WIF")
    return parts[0], parts[1], parts[2]


def build_report(volume_usd: float, balance_usd: float, trades: list[tuple[str, str, str]]) -> dict:
    eligibility = run_json(
        [
            sys.executable,
            str(SCRIPT_DIR / "eligibility_check.py"),
            "--volume-usd",
            str(volume_usd),
            "--balance-usd",
            str(balance_usd),
            "--json",
        ]
    )

    validated_trades = []
    for chain, from_token, to_token in trades:
        result = run_json(
            [
                sys.executable,
                str(SCRIPT_DIR / "trade_validator.py"),
                "--chain",
                chain,
                "--from-token",
                from_token,
                "--to-token",
                to_token,
                "--json",
            ]
        )
        validated_trades.append(
            {
                "chain": chain,
                "from_token": from_token,
                "to_token": to_token,
                **result,
            }
        )

    qualifying_count = sum(1 for trade in validated_trades if trade["qualifies"])
    return {
        "contest_status": eligibility,
        "proposed_trades": validated_trades,
        "summary": {
            "participation_ready": eligibility["participation_ready"],
            "leaderboard_ready": eligibility["leaderboard_ready"],
            "qualifying_trade_ideas": qualifying_count,
            "needs_onchainos_before_execution": True,
        },
    }


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
