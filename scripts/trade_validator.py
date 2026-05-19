#!/usr/bin/env python3
"""Validate whether a trade likely qualifies for the OKX Agentic Trading Competition."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass


QUALIFYING_CHAINS = {"solana", "x layer", "xlayer", "x-layer"}
STABLE_SYMBOLS = {
    "USDT",
    "USDC",
    "DAI",
    "FDUSD",
    "TUSD",
    "USDD",
    "PYUSD",
    "USDE",
    "USD1",
}
NATIVE_OR_WRAPPED = {
    "SOL",
    "WSOL",
    "X",
    "OKB",
    "WOKB",
    "ETH",
    "WETH",
}


@dataclass
class Validation:
    qualifies: bool
    status: str
    reasons: list[str]
    warnings: list[str]


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def normalize_chain(chain: str) -> str:
    return chain.strip().lower()


def validate_trade(chain: str, from_token: str, to_token: str) -> Validation:
    reasons: list[str] = []
    warnings: list[str] = []
    normalized_chain = normalize_chain(chain)
    from_symbol = normalize_symbol(from_token)
    to_symbol = normalize_symbol(to_token)

    if normalized_chain not in QUALIFYING_CHAINS:
        reasons.append("Chain is not Solana or X Layer.")

    disallowed = STABLE_SYMBOLS | NATIVE_OR_WRAPPED
    disallowed_sides = [symbol for symbol in (from_symbol, to_symbol) if symbol in disallowed]
    if disallowed_sides:
        reasons.append(
            "Pair includes stablecoin/native/wrapped-native side(s): "
            + ", ".join(disallowed_sides)
            + "."
        )

    if from_symbol == to_symbol:
        reasons.append("Input and output token symbols are the same.")

    if not from_symbol or not to_symbol:
        reasons.append("Both input and output token symbols are required.")

    if reasons:
        return Validation(False, "does_not_qualify", reasons, warnings)

    warnings.append("Confirm token metadata, route, and simulation with onchainOS before execution.")
    return Validation(True, "likely_qualifies", ["Chain and pair pass local contest filters."], warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chain", required=True, help="Trade chain, e.g. Solana or X Layer")
    parser.add_argument("--from-token", required=True, help="Input token symbol")
    parser.add_argument("--to-token", required=True, help="Output token symbol")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = validate_trade(args.chain, args.from_token, args.to_token)
    payload = {
        "qualifies": result.qualifies,
        "status": result.status,
        "reasons": result.reasons,
        "warnings": result.warnings,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Status: {result.status}")
        print(f"Qualifies: {str(result.qualifies).lower()}")
        for reason in result.reasons:
            print(f"- {reason}")
        for warning in result.warnings:
            print(f"Warning: {warning}")
    return 0 if result.qualifies else 2


if __name__ == "__main__":
    raise SystemExit(main())
