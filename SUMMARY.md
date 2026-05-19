## 1. Overview

Contest PnL Guardian helps Agentic Wallet users participate in the OKX Agentic Trading Competition with rule-aware trading workflows.

Core operations:
- Check contest eligibility and trading-volume progress.
- Validate whether proposed Solana or X Layer trades are likely to count.
- Reject stablecoin, native-token, and wrapped-native-token swaps for contest scoring.
- Build dry-run-first trade plans with risk controls.
- Require explicit confirmation before live onchainOS swaps.
- Summarize post-trade contest impact and realized PnL status.

Tags: `okx` `onchainos` `agentic-wallet` `trading` `contest` `pnl` `solana` `xlayer`

## 2. Prerequisites

- onchainOS or Agentic Wallet access for wallet, token, route, simulation, and swap data.
- A funded wallet controlled by the user.
- Contest activity focused on Solana and X Layer.
- Token metadata and route simulation before live execution.
- Explicit user confirmation before any live swap.

## 3. Quick Start

1. **Check readiness**: Ask the agent to check contest volume, wallet balance, and chain usage.
2. **Validate trade ideas**: Ask whether proposed Solana or X Layer token-token swaps count for contest scoring.
3. **Plan safely**: Have the agent use onchainOS data for liquidity, security, route, and simulation checks.
4. **Confirm execution**: Review the exact chain, tokens, amount, route, and risk notes before approving a live swap.
5. **Review results**: Ask for updated contest progress and realized PnL impact after execution.
