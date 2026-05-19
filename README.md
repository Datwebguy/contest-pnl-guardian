# Contest PnL Guardian

Contest PnL Guardian is an onchainOS-first skill that helps Agentic Wallet users validate qualifying trades, track contest eligibility, and trade with risk-aware guardrails for the OKX Agentic Trading Competition.

## What It Does

- Checks participation and leaderboard readiness.
- Handles registration/join intent through onchainOS competition tooling.
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

## Beginner Setup With Claude Code

1. Install Node.js LTS from `https://nodejs.org`.
2. Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

3. Create and open a project folder:

```bash
mkdir contest-pnl-guardian-demo
cd contest-pnl-guardian-demo
```

4. Install the OKX onchainOS skills:

```bash
npx skills add okx/onchainos-skills
```

Recommended selections:

- `okx-agentic-wallet`
- `okx-dex-market`
- `okx-dex-signal`
- `okx-dex-swap`
- `okx-dex-token`
- `okx-growth-competition`
- `okx-how-to-play`
- `okx-onchain-gateway`
- `okx-security`
- `okx-wallet-portfolio`

Choose project scope. If prompted for target agents, include Claude Code.

5. Clone this skill and copy it into Claude Code's project skill folder:

```bash
git clone https://github.com/Datwebguy/contest-pnl-guardian.git
mkdir -p .claude/skills
cp -R contest-pnl-guardian .claude/skills/contest-pnl-guardian
```

On Windows PowerShell:

```powershell
git clone https://github.com/Datwebguy/contest-pnl-guardian.git
New-Item -ItemType Directory -Path .claude\skills -Force
xcopy contest-pnl-guardian .claude\skills\contest-pnl-guardian /E /I /Y
```

6. Start Claude Code from the project folder:

```bash
claude
```

On Windows PowerShell, use `claude.cmd` if script execution is blocked.

7. In Claude, log in to Agentic Wallet:

```text
Log in to Agentic Wallet with email.
```

8. Ask Contest PnL Guardian to guide the flow:

```text
Use Contest PnL Guardian. I am new and want to join the OKX Agentic Trading Contest. Walk me through wallet setup, registration, eligibility, and safe trade planning. Do not register or trade without my explicit confirmation.
```

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

Registration test prompt:

```text
Use Contest PnL Guardian in dry-run mode. Show how you would register me for the Agentic Trading Contest without actually joining.
```

## Safety

This skill does not ask for private keys. Live trades must be executed only through onchainOS or Agentic Wallet after the user explicitly confirms the exact swap.
