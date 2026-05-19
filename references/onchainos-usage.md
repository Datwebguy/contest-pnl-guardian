# onchainOS Usage Pattern

Contest PnL Guardian must use onchainOS as the primary source of truth and trading tool.

## Required Data Calls

Before proposing a live trade, gather these data points through onchainOS or the Agentic Wallet plugin context:

- Wallet address, chain, and token balances
- Token metadata for input and output assets
- Token security/risk assessment
- Liquidity, route, expected output, fees, and slippage
- Recent token volume and price movement
- Simulation or dry-run result when available
- Recent wallet trades needed to estimate contest volume and realized PnL

## Execution Gate

Only execute a live swap after displaying:

- Chain
- Input token and amount
- Output token
- Slippage tolerance
- Route summary
- Contest qualification status
- Main risks

Then require the user to confirm the exact live swap.

## Fallbacks

- If token metadata is missing, ask onchainOS for metadata before classifying the trade.
- If simulation fails, do not execute. Explain the failure and request updated route data.
- If the chain is not Solana or X Layer, mark the trade as non-qualifying for contest scoring.
- If contest volume cannot be computed, provide a partial status and list the missing onchainOS fields.
