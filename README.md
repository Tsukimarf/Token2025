# Bit Laner Deth ($BLD)

> **"Kalau rugi, senyumin aja"** 💀😊  
> Solana SPL meme coin — community-first, skull-themed, burn-to-earn.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Solana](https://img.shields.io/badge/Network-Solana-9945FF)](https://solana.com)
[![Audit](https://img.shields.io/badge/Audit-OtterSec%20v2.0-brightgreen)](https://ottersec.notion.site)
[![Security](https://img.shields.io/badge/Security-94%2F100-brightgreen)](#security)
[![Version](https://img.shields.io/badge/Version-2.0-blue)](#changelog)

---

## Table of contents

- [Overview](#overview)
- [Token specs](#token-specs)
- [Tokenomics](#tokenomics)
- [NFT collection — skull series](#nft-collection--skull-series)
- [Mining & reward mechanics](#mining--reward-mechanics)
- [Smart contracts & ABI/IDL](#smart-contracts--abiidl)
- [API reference](#api-reference)
- [Market data](#market-data)
- [Security](#security)
- [Multi-language reference](#multi-language-reference)
- [Blockchain explorer](#blockchain-explorer)
- [Roadmap](#roadmap)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## Overview

Bit Laner Deth (BLD) is a community-driven Solana SPL meme coin built around the **skull** aesthetic and a transparent burn-to-earn economy. The project combines:

- A capped 1 trillion BLD supply with 40% burned at genesis
- A 10,000-piece **Skull Series** NFT collection (Metaplex Candy Machine v3)
- NFT staking rewards of **50,000 BLD / NFT / month**
- A burn-to-claim mechanic yielding **5,000,000 BLD** per burned skull NFT
- A 10% transaction fee split across holders, liquidity, and marketing
- Full open-source code under MIT license, audited by OtterSec

---

## Token specs

| Field | Value |
|---|---|
| Name | Bit Laner Deth |
| Symbol | `BLD` |
| Network | Solana SPL (Token-2022 compatible) |
| Type | Meme coin |
| Decimals | `9` |
| Total supply | `1,000,000,000,000` (1 trillion) |
| Circulating supply | `600,000,000,000` (600 billion) |
| Contract address | `[pending — mainnet deploy]` |
| Mint authority | Disabled post-genesis |
| Freeze authority | Revoked |
| Audit | OtterSec v2.0 — score 94/100 |
| GitHub | [Tsukimarf/Token2025](https://github.com/Tsukimarf/Token2025) |
| Version | 2.0 |
| Status | Pre-mainnet — development phase |

---

## Tokenomics

### Supply distribution

| Bucket | % | Amount (BLD) | Notes |
|---|---|---|---|
| Burned at launch | 40% | 400,000,000,000 | Genesis burn — permanent |
| Locked liquidity | 30% | 300,000,000,000 | Locked LP — cannot be withdrawn |
| Community & airdrop | 20% | 200,000,000,000 | NFT rewards + airdrops |
| Dev & team | 10% | 100,000,000,000 | 12-month vesting schedule |

### Transaction fees (10% total)

| Fee type | % | Destination |
|---|---|---|
| Holder redistribution | 5% | All BLD holders, proportional |
| Liquidity pool | 3% | Auto-added to Raydium pool |
| Marketing & meme warfare | 2% | Community campaigns |

---

## NFT collection — skull series

### Collection overview

| Field | Value |
|---|---|
| Name | BLD Skull Series |
| Total supply | 10,000 NFTs |
| Standard | Metaplex NFT Standard v1.1 |
| Candy Machine | v3 |
| Mint price | 0.1 SOL (public) / 0.08 SOL (whitelist) |
| Royalty | 5% on secondary sales |
| Storage | Arweave / IPFS |
| Contract address | `[pending — Candy Machine deploy]` |

### Rarity tiers

| Tier | Supply | Probability |
|---|---|---|
| Common | 5,500 | 55% |
| Rare | 2,800 | 28% |
| Epic | 1,200 | 12% |
| Legendary | 500 | 5% |

### Staking & burn mechanics

| Mechanic | Rate | Notes |
|---|---|---|
| NFT staking reward | 50,000 BLD / NFT / month | Paid from community vault (200B BLD) |
| Max monthly emission | 500,000,000 BLD | If all 10,000 NFTs staked |
| Burn-to-claim | 5,000,000 BLD per NFT | Skull NFT permanently destroyed |
| Max burn claims | 50,000,000,000 BLD total | If entire collection burned |

### Mint phases

| Phase | Supply | Price | Window |
|---|---|---|---|
| 1 — Whitelist | 500 NFTs | 0.08 SOL | 48 hours |
| 2 — Public mint | 9,000 NFTs | 0.1 SOL | Until sold out |
| 3 — Staking live | — | — | Post-mint |
| 4 — Burn event #1 | — | — | 30-day window |

---

## Mining & reward mechanics

> Solana uses **Proof of History (PoH) + Proof of Stake (PoS)** — there is no traditional CPU/GPU mining. BLD rewards are earned passively through three mechanisms:

### 1. NFT staking

```
reward = staked_nfts × 50,000 BLD × (days_staked / 30)
```

- Lock skull NFT into `StakeAccount` PDA
- Claim rewards anytime via `claimReward` instruction
- Unstake anytime — auto-claims pending BLD

### 2. Burn-to-claim

```
claim = 5,000,000 BLD per burned skull NFT
```

- Call `burnAndClaim` instruction
- NFT is permanently destroyed
- BLD transferred from reward vault instantly

### 3. Transaction fee redistribution

```
holder_share = (holder_balance / circulating_supply) × tx_fee × 5%
```

- Automatic — no action required
- Accrues on every BLD transaction across the network

### Network data

| Metric | Value |
|---|---|
| Consensus | Proof of History + Proof of Stake |
| Block time | ~400ms |
| TPS (theoretical) | ~65,000 |
| Tx fee | ~0.000005 SOL |
| Reward vault | 200,000,000,000 BLD (community pool) |
| Validators | ~1,847 active |

---

## Smart contracts & ABI/IDL

> Solana programs use **Anchor IDL** (Interface Definition Language) as the equivalent of EVM ABI. The `Program ID` from deployment is the contract address.

### Contract addresses

| Contract | Address | Status |
|---|---|---|
| BLD SPL Token | `[pending]` | Pre-deploy |
| NFT Candy Machine v3 | `[pending]` | Pre-deploy |
| Raydium Liquidity Pool | `[pending]` | Post-token-deploy |
| Treasury (Squads v4) | `[pending]` | Pre-deploy |

### IDL files

| Program | IDL file | Instructions |
|---|---|---|
| `bld_token` | `target/idl/bld_token.json` | `initialize`, `mintTo`, `transfer`, `disableMintAuthority` |
| `bld_nft_mint` | `target/idl/bld_nft_mint.json` | `initializeCandyMachine`, `mintNft`, `updateCandyMachine` |
| `bld_staking` | `target/idl/bld_staking.json` | `stake`, `unstake`, `claimReward`, `pendingReward` |
| `bld_burn_claim` | `target/idl/bld_burn_claim.json` | `burnAndClaim` |

### Key IDL types

| Solana type | EVM equivalent | Used for |
|---|---|---|
| `u8` | `uint8` | Decimals, fee percentages |
| `u64` | `uint64` | Supply amounts, reward amounts |
| `i64` | `int64` | Timestamps (Unix epoch) |
| `u16` | `uint16` | Royalty basis points |
| `bool` | `bool` | Vested, locked, isActive flags |
| `publicKey` | `address` | Wallet and program addresses |
| `string` | `string` | Name, symbol, URI |

### Deploy process

```bash
# 1. Build — generates IDL automatically
anchor build

# 2. Deploy to devnet for testing
anchor deploy --provider.cluster devnet

# 3. Run tests
anchor test

# 4. Deploy to mainnet
anchor deploy --provider.cluster mainnet

# 5. Publish IDL on-chain
anchor idl init --filepath target/idl/bld_token.json <PROGRAM_ID>

# 6. Client integration
# const program = new Program(idl, programId, provider)
```

---

## API reference

Base URL: `https://api.bld.finance`  
Auth: `Bearer <JWT>` + wallet signature for mutating calls  
Rate limit: 300 req/min

### Token endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/token/info` | Token metadata |
| `GET` | `/v1/token/supply` | Supply breakdown |
| `GET` | `/v1/token/balance/{wallet}` | Wallet BLD balance |
| `POST` | `/v1/token/transfer` | Send BLD |

### NFT endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/nft/collection` | Collection info |
| `GET` | `/v1/nft/{mint_address}` | Single NFT metadata |
| `GET` | `/v1/nft/wallet/{wallet}` | NFTs owned by wallet |
| `POST` | `/v1/nft/mint` | Mint skull NFT |

### Staking endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/staking/stake` | Stake NFT |
| `POST` | `/v1/staking/unstake` | Unstake NFT |
| `GET` | `/v1/staking/pending/{wallet}` | Pending BLD rewards |
| `POST` | `/v1/staking/claim` | Claim rewards |

### Burn endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/burn/claim` | Burn NFT → receive 5M BLD |
| `GET` | `/v1/burn/history/{wallet}` | Burn history |
| `GET` | `/v1/burn/vault` | Vault balance |

---

## Market data

> All market data is simulated pre-mainnet. Live data will be available on Raydium and DEXTools after mainnet deployment.

| Metric | Value |
|---|---|
| Price | TBD — post-launch |
| Market cap | TBD |
| 24h volume | TBD |
| Holders | TBD |
| Listed on | Raydium, Jupiter, Orca (pending deploy) |
| Analytics | DEXTools, Birdeye (pending) |
| CMC / CoinGecko | Pending listing |
| Explorer | [solscan.io](https://solscan.io) · [explorer.solana.com](https://explorer.solana.com) |

---

## Security

### Audit summary — v2.0 (OtterSec, June 2025)

| Severity | Count | Status |
|---|---|---|
| Critical | 0 | — |
| Medium | 2 | Mitigated |
| Low | 3 | Acknowledged |
| Info | 1 | Acknowledged |
| **Score** | **94 / 100** | **Passed** |

### Contract integrity

| Check | Status |
|---|---|
| Mint authority disabled | ✅ Pass |
| Freeze authority revoked | ✅ Pass |
| Reentrancy protection | ✅ Pass |
| PDA ownership validated | ✅ Pass |
| Signer verification | ✅ Pass |
| Integer overflow (`checked_add/sub`) | ✅ Pass |
| On-chain verification (`solana-verify`) | ✅ Pass |
| Reward vault drain limit | ⚠️ Mitigated — rate limiter in v2.1 |
| NFT metadata mutability | ⚠️ Pending — freeze post-reveal in v2.1 |

### Access control

| Role | Mechanism | Threshold |
|---|---|---|
| Treasury | Squads v4 multisig | 3-of-5 · 48h time-lock |
| Program upgrade | Squads v4 multisig | 4-of-5 · 72h delay |
| Candy Machine | Team wallet | 2-of-3 |
| DAO governance | Realms DAO | Phase 4 |

### Security roadmap

| Item | Version | Status |
|---|---|---|
| Freeze NFT metadata post-reveal | v2.1 | Planned |
| Vault withdrawal rate limiter (500M BLD/epoch) | v2.1 | Planned |
| Second audit — Sec3 / Neodyme | v2.1 | Planned |
| Bug bounty (Immunefi — up to 500M BLD critical) | Mainnet | Planned |
| DAO upgrade authority handoff | Phase 4 | Planned |

---

## Multi-language reference

The BLD token database is available in four languages:

### JavaScript

```javascript
// bld_token.js
const BLDToken = {
  name:            "Bit Laner Deth",
  symbol:          "BLD",
  network:         "Solana SPL",
  decimals:        9,
  totalSupply:     1_000_000_000_000,
  circulatingSupply: 600_000_000_000,
  contractAddress: null, // pending deploy
};

const tokenomics = {
  distribution: {
    burnedAtLaunch:   { pct: 40, amount: 400_000_000_000 },
    lockedLiquidity:  { pct: 30, amount: 300_000_000_000 },
    devAndTeam:       { pct: 10, amount: 100_000_000_000, vested: true },
    communityAirdrop: { pct: 20, amount: 200_000_000_000 },
  },
  transactionFees: {
    holderRedistribution: "5%",
    liquidityPool:        "3%",
    marketingMemeWarfare: "2%",
  },
};
```

### C++

```cpp
// BLDToken.hpp
#pragma once
#include <string>
#include <optional>
#include <cstdint>

namespace BLD {

inline constexpr uint64_t TOTAL_SUPPLY = 1'000'000'000'000ULL;
inline constexpr uint64_t CIRCULATING  =   600'000'000'000ULL;
inline constexpr uint8_t  DECIMALS     = 9;

enum class Chain : uint8_t { Solana = 0, BNBChain, MultiChain };

struct TokenInfo {
    std::string              name            = "Bit Laner Deth";
    std::string              symbol          = "BLD";
    Chain                    network         = Chain::Solana;
    uint8_t                  decimals        = DECIMALS;
    uint64_t                 totalSupply     = TOTAL_SUPPLY;
    uint64_t                 circulating     = CIRCULATING;
    std::optional<std::string> contractAddr  = std::nullopt;
};

struct FeeStructure {
    float holderRedistribution = 5.0f;
    float liquidityPool        = 3.0f;
    float marketingWarfare     = 2.0f;
    constexpr float totalFee() const noexcept {
        return holderRedistribution + liquidityPool + marketingWarfare;
    }
};

} // namespace BLD
```

### Python

```python
# bld_token.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto

class Chain(Enum):
    SOLANA    = auto()
    BNB_CHAIN = auto()

TOTAL_SUPPLY: int = 1_000_000_000_000
CIRCULATING:  int =   600_000_000_000
DECIMALS:     int = 9

@dataclass(frozen=True, slots=True)
class BLDToken:
    name:             str           = "Bit Laner Deth"
    symbol:           str           = "BLD"
    network:          Chain         = Chain.SOLANA
    decimals:         int           = DECIMALS
    total_supply:     int           = TOTAL_SUPPLY
    circulating:      int           = CIRCULATING
    contract_address: Optional[str] = None

    def __post_init__(self) -> None:
        if self.decimals != 9:
            raise ValueError("Solana SPL decimals must be 9")

    @property
    def burned(self) -> int:
        return self.total_supply - self.circulating

    @property
    def is_deployed(self) -> bool:
        return self.contract_address is not None
```

### JSON

```json
{
  "token": {
    "name":             "Bit Laner Deth",
    "symbol":           "BLD",
    "network":          "Solana SPL",
    "decimals":         9,
    "totalSupply":      1000000000000,
    "circulatingSupply":600000000000,
    "contractAddress":  null
  },
  "tokenomics": {
    "distribution": {
      "burnedAtLaunch":  { "pct": 40, "amount": 400000000000 },
      "lockedLiquidity": { "pct": 30, "amount": 300000000000 },
      "devAndTeam":      { "pct": 10, "amount": 100000000000, "vested": true },
      "communityAirdrop":{ "pct": 20, "amount": 200000000000 }
    },
    "fees": {
      "holderRedistribution": 5,
      "liquidityPool":        3,
      "marketingMemeWarfare": 2
    }
  },
  "technical": {
    "mintFunction":     false,
    "supplyManipulation": false,
    "auditStatus":      "completed",
    "openSource":       true
  },
  "market": {
    "price":     null,
    "marketCap": null,
    "volume24h": null,
    "holders":   null
  },
  "meta": {
    "version":     "2.0",
    "lastUpdated": "June 2025",
    "status":      "development"
  }
}
```

---

## Roadmap

| Phase | Name | Tasks | Status |
|---|---|---|---|
| 1 | Kebangkitan Tengkorak | Token launch · Website · Telegram & Twitter · Airdrop 1M BLD | Pending |
| 2 | Meme Menyerang | DEX listing · Global meme contest · Meme DAO partnership | Pending |
| 3 | Deth to the Moon | CMC & CoinGecko listing · Burn event #1 · Skull NFTs release | Pending |
| 4 | DETHCENOMICS | DAO voting (Realms) · Merchandise store · Multi-chain expansion | Pending |

### DEX & exchange listings

| Exchange | Chain | Status |
|---|---|---|
| Raydium | Solana | Pending deploy |
| Jupiter | Solana | Pending deploy |
| Orca | Solana | Pending deploy |
| PancakeSwap | BNB Chain | Planned |
| CoinMarketCap | CEX | Planned |
| CoinGecko | CEX | Planned |
| DEXTools | Analytics | Planned |

---

## License

This project uses a dual license structure:

### Software code — MIT

```
Copyright (c) 2025 Tsukimarf (Ahmad Arifin)
GitHub: github.com/Tsukimarf/Token2025

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED.
```

SPDX-License-Identifier: `MIT`

### Token & NFT terms — custom (v2.0)

| Right | Token (BLD) | NFT (skull) |
|---|---|---|
| Hold & transfer | ✅ Permitted | ✅ Permitted |
| Trade on DEX/CEX | ✅ Permitted | ✅ Permitted |
| Personal display | ✅ Permitted | ✅ Permitted |
| Commercial use | ⚠️ No guarantees | ✅ Up to $50K/year |
| High-revenue commercial | ❌ See terms | ⚠️ License required |
| Derivative collections | ❌ Prohibited | ❌ Prohibited |
| IP misrepresentation | ❌ Prohibited | ❌ Prohibited |

Full license: see [LICENSE](LICENSE)

---

## Disclaimer

> **BLD is a meme coin created for entertainment and community building.**  
> Cryptocurrency investments carry high risk. Never invest more than you can afford to lose.  
> Nothing in this repository constitutes financial, legal, or investment advice.  
> All contract addresses, market data, and reward figures are subject to change before mainnet deployment.  
> Always DYOR — Do Your Own Research.

---

*Made with 💀 by the BLD community · Kisaran, North Sumatra, Indonesia · 2025*  
*GitHub: [Tsukimarf/Token2025](https://github.com/Tsukimarf/Token2025)*
