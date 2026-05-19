#!/usr/bin/env python3
"""Validate whether a trade likely qualifies for the OKX Agentic Trading Competition."""

from __future__ import annotations

import argparse
import json

from core import validate_trade, validation_to_dict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chain", required=True, help="Trade chain, e.g. Solana or X Layer")
    parser.add_argument("--from-token", required=True, help="Input token symbol")
    parser.add_argument("--to-token", required=True, help="Output token symbol")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = validate_trade(args.chain, args.from_token, args.to_token)
    payload = validation_to_dict(result)

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
