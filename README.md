# Contest PnL Guardian

Contest PnL Guardian is an onchainOS-first skill that helps Agentic Wallet users validate qualifying trades, track contest eligibility, and trade with risk-aware guardrails for the OKX Agentic Trading Competition.

## What It Does

- Checks participation and leaderboard readiness.
- Validates whether proposed trades likely count for the contest.
- Rejects stablecoin, native-token, and wrapped-native-token swaps for contest scoring.
- Guides agents to use onchainOS for wallet data, token metadata, routes, simulations, and swaps.
- Requires explicit user confirmation before live execution.

## Install

After the skill is accepted into the OKX Plugin Store, users should be able to install it with:

```bash
npx skills add okx/plugin-store --skill contest-pnl-guardian
```

During development, clone this repository and load the skill directory in an agent that supports local skills.

## Local Test Commands

Generate a demo readiness report:

```bash
python scripts/contest_report.py --volume-usd 250 --balance-usd 120 --trade Solana:BONK:WIF --trade Solana:SOL:USDC
```

Validate a likely qualifying trade:

```bash
python scripts/trade_validator.py --chain Solana --from-token BONK --to-token WIF
```

Validate an invalid contest trade:

```bash
python scripts/trade_validator.py --chain Solana --from-token SOL --to-token USDC
```

Check eligibility progress:

```bash
python scripts/eligibility_check.py --volume-usd 250 --balance-usd 120
```

## Demo Prompt

```text
Use Contest PnL Guardian to check whether I am contest-ready with $250 volume, $120 wallet balance, and these proposed trades: Solana BONK to WIF, Solana SOL to USDC.
```

## Safety

This skill does not ask for private keys. Live trades must be executed only through onchainOS or Agentic Wallet after the user explicitly confirms the exact swap.
