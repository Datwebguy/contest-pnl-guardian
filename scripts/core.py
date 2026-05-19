"""Shared contest validation logic for Contest PnL Guardian scripts."""

from __future__ import annotations

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

LEADERBOARD_VOLUME_USD = 1000.0
PARTICIPATION_VOLUME_USD = 100.0
PARTICIPATION_BALANCE_USD = 100.0


@dataclass(frozen=True)
class Validation:
    qualifies: bool
    status: str
    reasons: list[str]
    warnings: list[str]


def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def normalize_chain(chain: str) -> str:
    return chain.strip().lower()


def pct(value: float, target: float) -> float:
    if target <= 0:
        return 100.0
    return min(100.0, round((value / target) * 100.0, 2))


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


def validation_to_dict(result: Validation) -> dict:
    return {
        "qualifies": result.qualifies,
        "status": result.status,
        "reasons": result.reasons,
        "warnings": result.warnings,
    }


def evaluate_eligibility(volume_usd: float, balance_usd: float) -> dict:
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


def build_report(volume_usd: float, balance_usd: float, trades: list[tuple[str, str, str]]) -> dict:
    eligibility = evaluate_eligibility(volume_usd, balance_usd)
    validated_trades = [
        {
            "chain": chain,
            "from_token": from_token,
            "to_token": to_token,
            **validation_to_dict(validate_trade(chain, from_token, to_token)),
        }
        for chain, from_token, to_token in trades
    ]

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
