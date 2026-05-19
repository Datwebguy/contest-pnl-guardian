# Contest Rules Reference

Use this file as the local rule memory for Contest PnL Guardian. Source rule pages should remain the authority when judges run the skill.

## Known Contest Requirements

- The skill must use onchainOS as the primary data source and trading tool.
- Contest scoring is based on realized PnL and realized PnL percentage.
- Trades should be routed through Agentic Wallet/onchainOS.
- Qualifying contest chains are Solana and X Layer.
- Stablecoin, native token, and wrapped native token swaps should be treated as non-qualifying contest trades.
- The leaderboard target requires at least 1000 USD in trading volume.
- The participation reward target requires at least 100 USD in trading volume and at least 100 USD wallet balance during the competition.
- Suspicious hedging, manipulation, or abusive activity can create disqualification risk.

## Implementation Notes

- Classify native or wrapped native symbols as non-qualifying sides: SOL, WSOL, X, OKB if represented as the X Layer gas/native asset, WOKB, ETH, WETH.
- Classify common stablecoins as non-qualifying sides: USDT, USDC, DAI, FDUSD, TUSD, USDD, PYUSD, USDE, USD1.
- If either side is unknown, mark contest qualification as unknown and require onchainOS token metadata.
- If a pair is non-qualifying, still explain whether it may be useful for setup or risk reduction outside contest scoring.
- For trade planning, separate "counts for contest" from "good trade". A trade can qualify and still be too risky.
