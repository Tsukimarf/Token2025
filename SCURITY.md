# Security Policy

Bit Laner Deth ($BLD) takes the security of its smart contracts, NFT program, and web/dashboard code seriously. This document describes supported versions, how to report a vulnerability, and what to expect after you report one.

---

## Supported versions

| Version | Status | Notes |
|---|---|---|
| 2.0.x | ✅ Actively supported | Current pre-mainnet release, OtterSec-audited |
| gemini/ tools & web3/ dashboard | ✅ Actively supported | Front-end, QML, and data-layer bundled with the token |
| < 2.0 | ❌ Not supported | Pre-audit prototypes, do not deploy |

Only the latest `2.0.x` release line and the code on the `main`/`Tsukimarf-patch-1` branches receive security fixes. Older tags are kept for reference only.

---

## Scope

In scope for this policy:

- On-chain programs: `bld_token`, `bld_nft_mint`, `bld_staking`, `bld_burn_claim` (Anchor/IDL, see [Smart contracts & ABI/IDL](README.md#smart-contracts--abiidl))
- Multi-language database exports (`bld_full_database.json/.sql`, `gemini/*.json/.sql/.csv/.qml`)
- The `web3/index.html` dashboard and its client-side wallet-connection code
- The Pythagoras Verifier utility (`gemini/` folder) bundled with the dashboard

Out of scope:

- Third-party wallets (Phantom, MetaMask), RPC providers, or DEX front-ends
- Denial-of-service via brute-force traffic against public RPC endpoints
- Issues that require physical access to a user's device or already-compromised keys
- Findings that rely solely on outdated/unsupported browsers

---

## Reporting a vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

1. Report privately via GitHub's [Security Advisories](https://github.com/Tsukimarf/Token2025/security/advisories/new) ("Report a vulnerability" button under the repo's **Security** tab).
2. If that's unavailable, contact the maintainer through the channel(s) listed on the project's GitHub profile ([Tsukimarf](https://github.com/Tsukimarf)) and mark the message as security-sensitive.
3. Include, where possible:
   - A clear description of the issue and its impact (funds at risk, data exposure, etc.)
   - Steps to reproduce, or a minimal proof-of-concept
   - Affected file(s), program instruction, or contract address
   - Your suggested severity (Critical / High / Medium / Low)

### What to expect

| Stage | Target time |
|---|---|
| Acknowledgement of report | Within 72 hours |
| Initial triage & severity assessment | Within 7 days |
| Fix or mitigation for Critical/High findings | Best-effort, prioritized over new features |
| Public disclosure | Coordinated with the reporter, typically after a fix ships |

We ask reporters to give us a reasonable window to investigate and patch before any public disclosure, and not to exploit a vulnerability beyond what's needed to demonstrate it (no draining funds, no touching other users' wallets/data).

---

## Bug bounty

A formal bug bounty program (Immunefi, up to 500,000,000 BLD for critical findings) is planned for the mainnet launch — see [Security roadmap](README.md#security-roadmap). Until that program is live, valid reports handled through this policy will still be credited (and rewarded at the maintainer's discretion) even for pre-mainnet/testnet findings.

---

## Current audit status

- **Auditor:** OtterSec, v2.0, June 2025 — [ottersec.notion.site](https://ottersec.notion.site)
- **Score:** 94 / 100 — 0 critical, 2 medium (mitigated), 3 low, 1 info
- **Second audit:** Sec3 / Neodyme, planned for v2.1
- Full breakdown: see [Security](README.md#security) in the README, and the `security` block in `web3/bld_full_database.json`.

---

## Disclaimer

BLD is a meme coin created for entertainment and community building. Reporting or fixing a vulnerability does not constitute financial, legal, or investment advice, and does not guarantee any particular reward amount outside the bug bounty program once it is formally live.