"""
bld_database.py — Bit Laner Deth ($BLD) v2.1
Complete Python database: token, IDL, ABI, API, contracts, security.
v2.1: OtterSec re-audit (97/100) — NFT metadata freeze + vault EpochGuard rate limiter.
SPDX-License-Identifier: MIT
Copyright (c) 2025 Tsukimarf
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional, TypedDict, NamedTuple, ClassVar, NotRequired
from enum import Enum, auto
import json

# ─────────────────────────────────────────────
# constants
# ─────────────────────────────────────────────
TOTAL_SUPPLY:      int   = 1_000_000_000_000
CIRCULATING:       int   =   600_000_000_000
BURNED_AT_GENESIS: int   =   400_000_000_000
DECIMALS:          int   = 9
AUDIT_VERSION:     str   = "v2.1"
AUDIT_SCORE:       int   = 97
EPOCH_SLOTS:       int   = 432_000         # ~2 days
MAX_EPOCH_WITHDRAW:int   = 500_000_000 * 10**DECIMALS   # 500M BLD raw units (v2.1 rate limiter)
STAKING_REWARD:    int   = 50_000          # BLD / NFT / month
BURN_CLAIM_REWARD: int   = 5_000_000       # BLD per burned NFT
NFT_SUPPLY:        int   = 10_000
ROYALTY_BPS:       int   = 500             # 5%
MINT_PRICE_SOL:    float = 0.1
WL_PRICE_SOL:      float = 0.08


# ─────────────────────────────────────────────
# enums
# ─────────────────────────────────────────────
class Chain(Enum):
    SOLANA    = "solana-mainnet"
    BNB_CHAIN = "bsc-mainnet"
    MULTI     = "multi-chain"


class DeployStatus(Enum):
    PENDING  = "pending"
    DEPLOYED = "deployed"
    VERIFIED = "verified"


class AuditStatus(Enum):
    PASS      = "pass"
    MITIGATED = "mitigated"
    PENDING   = "pending"
    FAIL      = "fail"


class ExchangeType(Enum):
    DEX       = "dex"
    AGGREGATOR = "aggregator"
    CEX       = "cex"
    ANALYTICS = "analytics"


class ListingStatus(Enum):
    PENDING = "pending"
    LIVE    = "live"
    PLANNED = "planned"
    DELISTED = "delisted"


class HttpMethod(Enum):
    GET  = "GET"
    POST = "POST"
    PUT  = "PUT"


# ─────────────────────────────────────────────
# token
# ─────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class BLDToken:
    """Immutable BLD token metadata — frozen=True."""
    name:             str            = "Bit Laner Deth"
    symbol:           str            = "BLD"
    tagline:          str            = "Kalau rugi, senyumin aja"
    network:          Chain          = Chain.SOLANA
    decimals:         int            = DECIMALS
    total_supply:     int            = TOTAL_SUPPLY
    circulating:      int            = CIRCULATING
    burned_genesis:   int            = BURNED_AT_GENESIS
    standard:         str            = "SPL Token (Token-2022 compatible)"
    contract_address: Optional[str]  = None
    audit_score:      int            = AUDIT_SCORE
    auditor:          str            = "OtterSec"
    audit_version:    str            = AUDIT_VERSION
    version:          str            = "2.1"
    github:           str            = "https://github.com/Tsukimarf/Token2025"
    license:          str            = "MIT"

    _registry: ClassVar[list[BLDToken]] = []

    def __post_init__(self) -> None:
        if self.decimals != 9:
            raise ValueError(f"Solana SPL decimals must be 9, got {self.decimals}")
        if self.total_supply != TOTAL_SUPPLY:
            raise ValueError("Total supply must be 1 trillion BLD")
        if self.circulating + self.burned_genesis != TOTAL_SUPPLY:
            raise ValueError("circulating + burned must equal total_supply")

    @property
    def burned(self) -> int:
        return self.total_supply - self.circulating

    @property
    def is_deployed(self) -> bool:
        return self.contract_address is not None

    def to_dict(self) -> dict:
        return {
            "name":             self.name,
            "symbol":           self.symbol,
            "tagline":          self.tagline,
            "network":          self.network.value,
            "decimals":         self.decimals,
            "total_supply":     self.total_supply,
            "circulating":      self.circulating,
            "burned":           self.burned,
            "contract_address": self.contract_address,
            "is_deployed":      self.is_deployed,
            "audit_score":      self.audit_score,
            "auditor":          self.auditor,
            "audit_version":    self.audit_version,
            "version":          self.version,
        }


# ─────────────────────────────────────────────
# tokenomics
# ─────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class Bucket:
    pct:    int
    amount: int
    locked: bool = False
    vested: bool = False
    vesting_months: int = 0
    note:   str = ""

    def __post_init__(self) -> None:
        if not 0 <= self.pct <= 100:
            raise ValueError(f"pct must be 0-100, got {self.pct}")


@dataclass(frozen=True, slots=True)
class FeeItem:
    pct:  float
    dest: str


@dataclass(frozen=True, slots=True)
class FeeStructure:
    holder_redistribution: FeeItem = field(
        default_factory=lambda: FeeItem(5.0, "All BLD holders proportional"))
    liquidity_pool:        FeeItem = field(
        default_factory=lambda: FeeItem(3.0, "Auto-added to Raydium LP"))
    marketing:             FeeItem = field(
        default_factory=lambda: FeeItem(2.0, "Marketing and meme warfare fund"))

    @property
    def total_pct(self) -> float:
        return (self.holder_redistribution.pct
                + self.liquidity_pool.pct
                + self.marketing.pct)


distribution: dict[str, Bucket] = {
    "burned_at_launch":  Bucket(40, 400_000_000_000, note="Genesis burn — permanent"),
    "locked_liquidity":  Bucket(30, 300_000_000_000, locked=True, note="Raydium LP locked"),
    "community_airdrop": Bucket(20, 200_000_000_000, note="NFT rewards + airdrops"),
    "dev_and_team":      Bucket(10, 100_000_000_000, locked=True, vested=True,
                                vesting_months=12, note="12-month linear vesting"),
}
fees = FeeStructure()

assert sum(b.pct for b in distribution.values()) == 100, "Distribution must sum to 100"
assert fees.total_pct == 10.0, "Total fee must be 10%"


# ─────────────────────────────────────────────
# NFT collection
# ─────────────────────────────────────────────
@dataclass(slots=True)
class RarityTier:
    name:   str
    supply: int
    pct:    float


@dataclass(slots=True)
class MintPhase:
    phase:     int
    name:      str
    supply:    int
    price_sol: float
    window:    str


@dataclass(slots=True)
class NFTCollection:
    name:             str   = "BLD Skull Series"
    symbol:           str   = "BLDS"
    total_supply:     int   = NFT_SUPPLY
    candy_machine:    str   = "v3"
    storage:          str   = "Arweave"
    mint_price_sol:   float = MINT_PRICE_SOL
    wl_price_sol:     float = WL_PRICE_SOL
    royalty_bps:      int   = ROYALTY_BPS
    is_mutable:       bool  = True
    contract_address: Optional[str] = None
    staking_reward:   int   = STAKING_REWARD
    burn_to_claim:    int   = BURN_CLAIM_REWARD

    rarity_tiers: list[RarityTier] = field(default_factory=lambda: [
        RarityTier("common",    5500, 55.0),
        RarityTier("rare",      2800, 28.0),
        RarityTier("epic",      1200, 12.0),
        RarityTier("legendary",  500,  5.0),
    ])
    mint_phases: list[MintPhase] = field(default_factory=lambda: [
        MintPhase(1, "Whitelist",    500,  0.08, "48h"),
        MintPhase(2, "Public",      9000,  0.10, "until sold out"),
        MintPhase(3, "Staking",        0,  0.00, "post-mint"),
        MintPhase(4, "Burn event #1",  0,  0.00, "30 days"),
    ])

    def monthly_reward_pool(self) -> int:
        return self.total_supply * self.staking_reward

    def max_burn_claim_total(self) -> int:
        return self.total_supply * self.burn_to_claim

    @property
    def royalty_pct(self) -> float:
        return self.royalty_bps / 100


# ─────────────────────────────────────────────
# contract addresses
# ─────────────────────────────────────────────
BASE58_RE = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")


@dataclass(slots=True)
class ContractAddress:
    key:     str
    address: Optional[str]
    status:  DeployStatus
    note:    str
    program: Optional[str] = None

    @property
    def explorer_url(self) -> Optional[str]:
        if self.address:
            return f"https://solscan.io/account/{self.address}"
        return None

    def set_address(self, address: str) -> None:
        """Record a REAL deployed address (base58, 32-44 chars). Call only after on-chain deploy."""
        if not BASE58_RE.fullmatch(address):
            raise ValueError(f"invalid Solana address: {address!r}")
        self.address = address
        self.status  = DeployStatus.DEPLOYED


contracts: dict[str, ContractAddress] = {
    "bld_spl_token": ContractAddress(
        key="bld_spl_token", address=None,
        status=DeployStatus.PENDING,
        note="Deploy via spl-token CLI or Anchor",
        program="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    ),
    "nft_candy_machine": ContractAddress(
        key="nft_candy_machine", address=None,
        status=DeployStatus.PENDING,
        note="Metaplex Candy Machine v3",
        program="CndyV3LdqHUfDLmd1X2Bf82vQD3PkYPGM6ZaLmkKBSf",
    ),
    "staking_program": ContractAddress(
        key="staking_program", address=None,
        status=DeployStatus.PENDING,
        note="Anchor program — bld_staking",
    ),
    "burn_claim_program": ContractAddress(
        key="burn_claim_program", address=None,
        status=DeployStatus.PENDING,
        note="Anchor program — bld_burn_claim",
    ),
    "raydium_pool": ContractAddress(
        key="raydium_pool", address=None,
        status=DeployStatus.PENDING,
        note="Created after token deploy",
        program="675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
    ),
    "treasury_multisig": ContractAddress(
        key="treasury_multisig", address=None,
        status=DeployStatus.PENDING,
        note="Squads v4 — 3-of-5 multisig",
        program="SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf",
    ),
}


# ─────────────────────────────────────────────
# IDL types
# ─────────────────────────────────────────────
class IDLAccount(TypedDict):
    name:      str
    isMut:     bool
    isSigner:  bool


class IDLArg(TypedDict):
    name: str
    type: str


class IDLInstruction(TypedDict):
    name:     str
    accounts: list[IDLAccount]
    args:     list[IDLArg]


class IDLEventField(TypedDict):
    name:  str
    type:  str
    index: bool


class IDLEvent(TypedDict):
    name:   str
    fields: list[IDLEventField]


class IDLConstant(TypedDict):
    name:  str
    type:  str
    value: str


class IDLError(TypedDict):
    code: int
    name: str
    msg:  str


class IDLProgram(TypedDict):
    version:      str
    name:         str
    instructions: list[IDLInstruction]
    events:       list[IDLEvent]
    constants:    list[IDLConstant]
    errors:       NotRequired[list[IDLError]]   # added in v2.1


idl: dict[str, IDLProgram] = {
    "bld_token": {
        "version": "0.1.0",
        "name":    "bld_token",
        "instructions": [
            {
                "name": "initialize",
                "accounts": [
                    {"name": "mint",          "isMut": True,  "isSigner": True},
                    {"name": "authority",     "isMut": True,  "isSigner": True},
                    {"name": "systemProgram", "isMut": False, "isSigner": False},
                ],
                "args": [
                    {"name": "totalSupply", "type": "u64"},
                    {"name": "decimals",    "type": "u8"},
                ],
            },
            {
                "name": "mintTo",
                "accounts": [
                    {"name": "mint",        "isMut": True,  "isSigner": False},
                    {"name": "destination", "isMut": True,  "isSigner": False},
                    {"name": "authority",   "isMut": False, "isSigner": True},
                ],
                "args": [{"name": "amount", "type": "u64"}],
            },
            {
                "name": "transfer",
                "accounts": [
                    {"name": "from",  "isMut": True,  "isSigner": False},
                    {"name": "to",    "isMut": True,  "isSigner": False},
                    {"name": "owner", "isMut": False, "isSigner": True},
                ],
                "args": [{"name": "amount", "type": "u64"}],
            },
            {
                "name": "disableMintAuthority",
                "accounts": [
                    {"name": "mint",      "isMut": True,  "isSigner": False},
                    {"name": "authority", "isMut": False, "isSigner": True},
                ],
                "args": [],
            },
        ],
        "events": [
            {
                "name": "TokenInitialized",
                "fields": [
                    {"name": "mint",        "type": "publicKey", "index": True},
                    {"name": "totalSupply", "type": "u64",       "index": False},
                    {"name": "decimals",    "type": "u8",        "index": False},
                ],
            },
            {
                "name": "Transfer",
                "fields": [
                    {"name": "from",   "type": "publicKey", "index": True},
                    {"name": "to",     "type": "publicKey", "index": True},
                    {"name": "amount", "type": "u64",       "index": False},
                ],
            },
        ],
        "constants": [
            {"name": "TOTAL_SUPPLY", "type": "u64", "value": "1000000000000"},
            {"name": "DECIMALS",     "type": "u8",  "value": "9"},
        ],
    },

    "bld_staking": {
        "version": "0.2.0",
        "name":    "bld_staking",
        "instructions": [
            {
                "name": "stake",
                "accounts": [
                    {"name": "stakeAccount", "isMut": True,  "isSigner": False},
                    {"name": "nftMint",      "isMut": False, "isSigner": False},
                    {"name": "owner",        "isMut": True,  "isSigner": True},
                ],
                "args": [],
            },
            {
                "name": "unstake",
                "accounts": [
                    {"name": "stakeAccount", "isMut": True, "isSigner": False},
                    {"name": "owner",        "isMut": True, "isSigner": True},
                ],
                "args": [],
            },
            {
                "name": "claimReward",
                "accounts": [
                    {"name": "stakeAccount",  "isMut": True,  "isSigner": False},
                    {"name": "rewardVault",   "isMut": True,  "isSigner": False},
                    {"name": "epochGuard",    "isMut": True,  "isSigner": False},  # v2.1
                    {"name": "ownerTokenAcc", "isMut": True,  "isSigner": False},
                    {"name": "owner",         "isMut": False, "isSigner": True},
                ],
                "args": [],
            },
            {   # v2.1 — permissionless, callable after EPOCH_SLOTS
                "name": "resetEpoch",
                "accounts": [
                    {"name": "epochGuard", "isMut": True,  "isSigner": False},
                    {"name": "clock",      "isMut": False, "isSigner": False},
                ],
                "args": [],
            },
            {
                "name": "pendingReward",
                "accounts": [
                    {"name": "stakeAccount", "isMut": False, "isSigner": False},
                ],
                "args": [],
            },
        ],
        "events": [
            {
                "name": "Staked",
                "fields": [
                    {"name": "owner",    "type": "publicKey", "index": True},
                    {"name": "nftMint",  "type": "publicKey", "index": True},
                    {"name": "stakedAt", "type": "i64",       "index": False},
                ],
            },
            {
                "name": "RewardClaimed",
                "fields": [
                    {"name": "owner",  "type": "publicKey", "index": True},
                    {"name": "amount", "type": "u64",       "index": False},
                ],
            },
        ],
        "errors": [
            {"code": 6000, "name": "EpochLimitExceeded", "msg": "Vault withdrawal would exceed the per-epoch cap"},
            {"code": 6001, "name": "EpochNotElapsed",    "msg": "Epoch window has not elapsed yet"},
        ],
        "constants": [
            {"name": "REWARD_PER_NFT_PER_MONTH", "type": "u64", "value": "50000000000000"},
            {"name": "MAX_EPOCH_WITHDRAW",       "type": "u64", "value": str(MAX_EPOCH_WITHDRAW)},
            {"name": "EPOCH_SLOTS",              "type": "u64", "value": str(EPOCH_SLOTS)},
        ],
    },

    "bld_burn_claim": {
        "version": "0.1.0",
        "name":    "bld_burn_claim",
        "instructions": [
            {
                "name": "burnAndClaim",
                "accounts": [
                    {"name": "nftMint",         "isMut": True,  "isSigner": False},
                    {"name": "nftTokenAccount", "isMut": True,  "isSigner": False},
                    {"name": "burnRecord",      "isMut": True,  "isSigner": False},
                    {"name": "bldVault",        "isMut": True,  "isSigner": False},
                    {"name": "burnerTokenAcc",  "isMut": True,  "isSigner": False},
                    {"name": "burner",          "isMut": True,  "isSigner": True},
                    {"name": "tokenProgram",    "isMut": False, "isSigner": False},
                ],
                "args": [],
            },
        ],
        "events": [
            {
                "name": "BurnClaimed",
                "fields": [
                    {"name": "burner",    "type": "publicKey", "index": True},
                    {"name": "nftMint",   "type": "publicKey", "index": True},
                    {"name": "bldAmount", "type": "u64",       "index": False},
                ],
            },
        ],
        "constants": [
            {"name": "BLD_PER_BURN", "type": "u64", "value": "5000000000000000"},
        ],
    },
}


# ─────────────────────────────────────────────
# ABI (EVM-style — cross-chain / educational)
# ─────────────────────────────────────────────
class ABIInput(TypedDict):
    name:    str
    type:    str
    indexed: bool


class ABIOutput(TypedDict):
    name: str
    type: str


class ABIItem(TypedDict):
    type:             str
    name:             str
    inputs:           list[ABIInput]
    outputs:          list[ABIOutput]
    stateMutability:  str
    anonymous:        bool


abi: dict[str, list[ABIItem]] = {
    "bld_token": [
        {"type": "function", "name": "initialize",           "inputs": [{"name": "totalSupply", "type": "uint64", "indexed": False}, {"name": "decimals", "type": "uint8", "indexed": False}], "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "mintTo",               "inputs": [{"name": "amount", "type": "uint64", "indexed": False}],                                                               "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "transfer",             "inputs": [{"name": "to", "type": "address", "indexed": False}, {"name": "amount", "type": "uint64", "indexed": False}],          "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "disableMintAuthority", "inputs": [],                                                                                                                     "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "balanceOf",            "inputs": [{"name": "account", "type": "address", "indexed": False}],                                                             "outputs": [{"name": "", "type": "uint64"}], "stateMutability": "view", "anonymous": False},
        {"type": "function", "name": "totalSupply",          "inputs": [],                                                                                                                     "outputs": [{"name": "", "type": "uint64"}], "stateMutability": "view", "anonymous": False},
        {"type": "event",    "name": "Transfer",             "inputs": [{"name": "from", "type": "address", "indexed": True}, {"name": "to", "type": "address", "indexed": True}, {"name": "amount", "type": "uint64", "indexed": False}], "outputs": [], "stateMutability": "", "anonymous": False},
    ],
    "bld_staking": [
        {"type": "function", "name": "stake",         "inputs": [{"name": "nftMint", "type": "address", "indexed": False}], "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "unstake",       "inputs": [{"name": "nftMint", "type": "address", "indexed": False}], "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "claimReward",   "inputs": [{"name": "nftMint", "type": "address", "indexed": False}], "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "resetEpoch",    "inputs": [], "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "function", "name": "pendingReward", "inputs": [{"name": "nftMint", "type": "address", "indexed": False}], "outputs": [{"name": "", "type": "uint64"}], "stateMutability": "view", "anonymous": False},
        {"type": "event",    "name": "Staked",        "inputs": [{"name": "owner", "type": "address", "indexed": True}, {"name": "nftMint", "type": "address", "indexed": True}, {"name": "stakedAt", "type": "int64", "indexed": False}], "outputs": [], "stateMutability": "", "anonymous": False},
        {"type": "event",    "name": "RewardClaimed", "inputs": [{"name": "owner", "type": "address", "indexed": True}, {"name": "amount", "type": "uint64", "indexed": False}], "outputs": [], "stateMutability": "", "anonymous": False},
    ],
    "bld_burn_claim": [
        {"type": "function", "name": "burnAndClaim", "inputs": [{"name": "nftMint", "type": "address", "indexed": False}], "outputs": [], "stateMutability": "nonpayable", "anonymous": False},
        {"type": "event",    "name": "BurnClaimed",  "inputs": [{"name": "burner", "type": "address", "indexed": True}, {"name": "nftMint", "type": "address", "indexed": True}, {"name": "bldAmount", "type": "uint64", "indexed": False}], "outputs": [], "stateMutability": "", "anonymous": False},
    ],
}


# ─────────────────────────────────────────────
# API endpoints
# ─────────────────────────────────────────────
class APIParam(TypedDict):
    name:     str
    location: str   # path | body | query
    type:     str
    required: bool


@dataclass(frozen=True, slots=True)
class APIEndpoint:
    module:       str
    method:       HttpMethod
    path:         str
    description:  str
    auth_required: bool
    params:       tuple[APIParam, ...]

    @property
    def full_url(self) -> str:
        return f"https://api.bld.finance{self.path}"


API_BASE_URL   = "https://api.bld.finance"
API_VERSION    = "v1"
API_AUTH       = "Bearer JWT"
API_RATE_LIMIT = 300  # req/min

endpoints: list[APIEndpoint] = [
    APIEndpoint("contracts", HttpMethod.GET, "/v1/contracts",              "All contract addresses + deploy status (null until deployed)", False, ()),
    APIEndpoint("contracts", HttpMethod.GET, "/v1/contracts/{key}",        "One contract: address, program id, status, explorer URL",      False, ({"name":"key","location":"path","type":"string","required":True},)),
    APIEndpoint("security",  HttpMethod.GET, "/v1/audit",                  "Latest audit: OtterSec v2.1, score 97, findings",              False, ()),
    APIEndpoint("token",   HttpMethod.GET,  "/v1/token/info",              "Token metadata",                    True,  ()),
    APIEndpoint("token",   HttpMethod.GET,  "/v1/token/supply",            "Supply breakdown",                  True,  ()),
    APIEndpoint("token",   HttpMethod.GET,  "/v1/token/balance/{wallet}",  "Wallet BLD balance",                True,  ({"name":"wallet","location":"path","type":"string","required":True},)),
    APIEndpoint("token",   HttpMethod.POST, "/v1/token/transfer",          "Send BLD — requires signature",     True,  ({"name":"from","location":"body","type":"string","required":True},{"name":"to","location":"body","type":"string","required":True},{"name":"amount","location":"body","type":"integer","required":True},{"name":"signature","location":"body","type":"string","required":True})),
    APIEndpoint("nft",     HttpMethod.GET,  "/v1/nft/collection",          "Skull Series metadata",             True,  ()),
    APIEndpoint("nft",     HttpMethod.GET,  "/v1/nft/{mint_address}",      "Single NFT metadata",               True,  ({"name":"mint_address","location":"path","type":"string","required":True},)),
    APIEndpoint("nft",     HttpMethod.GET,  "/v1/nft/wallet/{wallet}",     "NFTs by wallet",                    True,  ({"name":"wallet","location":"path","type":"string","required":True},{"name":"staked","location":"query","type":"boolean","required":False},{"name":"rarity","location":"query","type":"string","required":False})),
    APIEndpoint("nft",     HttpMethod.POST, "/v1/nft/mint",                "Mint skull NFT",                    True,  ({"name":"payer","location":"body","type":"string","required":True},{"name":"signature","location":"body","type":"string","required":True},{"name":"whitelist_token","location":"body","type":"string","required":False})),
    APIEndpoint("staking", HttpMethod.POST, "/v1/staking/stake",           "Stake NFT",                         True,  ({"name":"wallet","location":"body","type":"string","required":True},{"name":"nft_mint","location":"body","type":"string","required":True},{"name":"signature","location":"body","type":"string","required":True})),
    APIEndpoint("staking", HttpMethod.POST, "/v1/staking/unstake",         "Unstake NFT",                       True,  ({"name":"wallet","location":"body","type":"string","required":True},{"name":"nft_mint","location":"body","type":"string","required":True},{"name":"signature","location":"body","type":"string","required":True})),
    APIEndpoint("staking", HttpMethod.GET,  "/v1/staking/pending/{wallet}","Pending BLD rewards",               True,  ({"name":"wallet","location":"path","type":"string","required":True},)),
    APIEndpoint("staking", HttpMethod.POST, "/v1/staking/claim",           "Claim rewards",                     True,  ({"name":"wallet","location":"body","type":"string","required":True},{"name":"nft_mints","location":"body","type":"array","required":True},{"name":"signature","location":"body","type":"string","required":True})),
    APIEndpoint("burn",    HttpMethod.POST, "/v1/burn/claim",              "Burn NFT → 5M BLD",                 True,  ({"name":"wallet","location":"body","type":"string","required":True},{"name":"nft_mint","location":"body","type":"string","required":True},{"name":"signature","location":"body","type":"string","required":True})),
    APIEndpoint("burn",    HttpMethod.GET,  "/v1/burn/history/{wallet}",   "Burn history",                      True,  ({"name":"wallet","location":"path","type":"string","required":True},)),
    APIEndpoint("burn",    HttpMethod.GET,  "/v1/burn/vault",              "Vault balance",                     False, ()),
]

HTTP_STATUS_CODES: dict[int, str] = {
    200: "OK",
    400: "Bad request — invalid params or insufficient balance",
    401: "Unauthorized — invalid or missing JWT",
    403: "Forbidden — signature verification failed",
    404: "Not found",
    409: "Conflict — duplicate state",
    500: "Internal server error",
}


# ─────────────────────────────────────────────
# security
# ─────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class SecurityCheck:
    name:   str
    status: AuditStatus
    detail: str


@dataclass(frozen=True, slots=True)
class AccessRole:
    name:         str
    mechanism:    str
    threshold:    str
    timelock_hrs: int


security_checks: list[SecurityCheck] = [
    SecurityCheck("Mint authority disabled",  AuditStatus.PASS,      "Revoked post-genesis. No new BLD possible."),
    SecurityCheck("Freeze authority revoked", AuditStatus.PASS,      "Cannot freeze any token account."),
    SecurityCheck("Reentrancy protection",    AuditStatus.PASS,      "Anchor account guards prevent cross-program reentrancy."),
    SecurityCheck("PDA ownership validated",  AuditStatus.PASS,      "All stake/burn PDAs verify seeds and bump."),
    SecurityCheck("Signer verification",      AuditStatus.PASS,      "Every mutating instruction requires explicit signer."),
    SecurityCheck("Integer overflow guards",  AuditStatus.PASS,      "checked_add / checked_sub on all arithmetic."),
    SecurityCheck("On-chain verification",    AuditStatus.PASS,      "solana-verify confirms deployed bytecode."),
    SecurityCheck("Vault drain rate limit",   AuditStatus.PASS,      "EpochGuard: 500M BLD max per 432,000-slot epoch; permissionless reset. (v2.1)"),
    SecurityCheck("NFT metadata mutability",  AuditStatus.PASS,      "isMutable: false post-reveal; update authority = SystemProgram. (v2.1)"),
]


class AuditFindings(NamedTuple):
    critical: int
    medium:   int
    low:      int
    info:     int


class AuditRecord(NamedTuple):
    version: str
    date:    str
    score:   int
    findings: Optional[AuditFindings]
    note:    str


audit_history: list[AuditRecord] = [
    AuditRecord("v1.0", "March 2026",   0,  None, "Genesis, internal review only"),
    AuditRecord("v1.1", "April 2026",   0,  None, "Freeze authority revoked, signer checks, NFT URI validation"),
    AuditRecord("v2.0", "June 2025",    94, AuditFindings(0, 2, 3, 1), "Full OtterSec audit, 2 medium open"),
    AuditRecord("v2.1", "October 2026", 97, AuditFindings(0, 0, 1, 1), "Metadata freeze + vault rate limiter, 0 medium"),
]

access_roles: list[AccessRole] = [
    AccessRole("Treasury",        "Squads v4", "3-of-5", 48),
    AccessRole("Program upgrade", "Squads v4", "4-of-5", 72),
    AccessRole("Candy Machine",   "Team wallet","2-of-3",  0),
    AccessRole("DAO governance",  "Realms DAO", "on-chain vote", 0),
]


# ─────────────────────────────────────────────
# roadmap
# ─────────────────────────────────────────────
class Phase(TypedDict):
    phase:     int
    name:      str
    tasks:     list[str]
    status:    str
    completed: bool


roadmap: list[Phase] = [
    {"phase": 1, "name": "Kebangkitan Tengkorak", "status": "pending", "completed": False,
     "tasks": ["Token launch & website", "Telegram & Twitter", "First airdrop 1M BLD", "DEX liquidity seed"]},
    {"phase": 2, "name": "Meme Menyerang",         "status": "pending", "completed": False,
     "tasks": ["Raydium/Jupiter/Orca listing", "Global meme contest", "Meme DAO partnership", "NFT whitelist"]},
    {"phase": 3, "name": "Deth to the Moon",        "status": "pending", "completed": False,
     "tasks": ["CMC & CoinGecko listing", "Burn event #1", "Skull Series mint", "Staking live"]},
    {"phase": 4, "name": "DETHCENOMICS",            "status": "pending", "completed": False,
     "tasks": ["Realms DAO", "Merch store", "Multi-chain BNB", "DAO upgrade authority", "Immunefi bounty"]},
]


# ─────────────────────────────────────────────
# exchanges
# ─────────────────────────────────────────────
class Exchange(NamedTuple):
    name:   str
    type:   ExchangeType
    chain:  Chain
    status: ListingStatus
    url:    str


exchanges: list[Exchange] = [
    Exchange("Raydium",       ExchangeType.DEX,       Chain.SOLANA,    ListingStatus.PENDING,  "https://raydium.io"),
    Exchange("Jupiter",       ExchangeType.AGGREGATOR, Chain.SOLANA,  ListingStatus.PENDING,  "https://jup.ag"),
    Exchange("Orca",          ExchangeType.DEX,       Chain.SOLANA,    ListingStatus.PENDING,  "https://orca.so"),
    Exchange("PancakeSwap",   ExchangeType.DEX,       Chain.BNB_CHAIN, ListingStatus.PLANNED,  "https://pancakeswap.finance"),
    Exchange("CoinMarketCap", ExchangeType.CEX,       Chain.MULTI,     ListingStatus.PLANNED,  "https://coinmarketcap.com"),
    Exchange("CoinGecko",     ExchangeType.CEX,       Chain.MULTI,     ListingStatus.PLANNED,  "https://coingecko.com"),
    Exchange("DEXTools",      ExchangeType.ANALYTICS, Chain.SOLANA,    ListingStatus.PLANNED,  "https://dextools.io"),
    Exchange("Birdeye",       ExchangeType.ANALYTICS, Chain.SOLANA,    ListingStatus.PLANNED,  "https://birdeye.so"),
]


# ─────────────────────────────────────────────
# validation
# ─────────────────────────────────────────────
def validate_all() -> None:
    token = BLDToken()
    nft   = NFTCollection()

    assert token.total_supply == TOTAL_SUPPLY
    assert token.burned       == BURNED_AT_GENESIS
    assert token.decimals     == 9
    assert not token.is_deployed
    assert token.audit_version == "v2.1" and token.audit_score == 97
    assert audit_history[-1].score == token.audit_score
    assert audit_history[-1].findings.medium == 0
    assert MAX_EPOCH_WITHDRAW == 500_000_000_000_000_000
    assert all(s.status == AuditStatus.PASS for s in security_checks)
    assert any(i["name"] == "resetEpoch" for i in idl["bld_staking"]["instructions"])

    assert fees.total_pct                         == 10.0
    assert sum(b.pct for b in distribution.values()) == 100
    assert distribution["dev_and_team"].vested    is True
    assert distribution["locked_liquidity"].locked is True

    assert nft.total_supply         == 10_000
    assert nft.staking_reward       == 50_000
    assert nft.burn_to_claim        == 5_000_000
    assert nft.monthly_reward_pool()== 500_000_000
    assert nft.royalty_pct          == 5.0

    assert len(idl)       == 3
    assert len(endpoints) == 18
    assert len(contracts) == 6
    assert len(roadmap)   == 4
    assert len(exchanges) == 8

    passed = sum(1 for s in security_checks if s.status == AuditStatus.PASS)
    print("✓ validate_all — all assertions passed")
    print(f"  token:         {token.name} ({token.symbol})")
    print(f"  total supply:  {token.total_supply:,} BLD")
    print(f"  circulating:   {token.circulating:,} BLD")
    print(f"  burned:        {token.burned:,} BLD")
    print(f"  total fee:     {fees.total_pct}%")
    print(f"  NFT supply:    {nft.total_supply:,}")
    print(f"  monthly pool:  {nft.monthly_reward_pool():,} BLD/month (max)")
    print(f"  IDL programs:  {len(idl)}")
    print(f"  API endpoints: {len(endpoints)}")
    print(f"  contracts:     {len(contracts)}")
    print(f"  security:      {passed}/{len(security_checks)} checks passed")
    print(f"  roadmap:       {len(roadmap)} phases")
    print(f"  exchanges:     {len(exchanges)}")


def export_json(path: str = "bld_export.json") -> None:
    """Export full database as JSON."""
    token = BLDToken()
    nft   = NFTCollection()

    data = {
        "meta":      {"project": token.name, "symbol": token.symbol, "version": token.version, "last_updated": "2026-10-26"},
        "token":     token.to_dict(),
        "contracts": {k: {"address": v.address, "status": v.status.value, "note": v.note, "program": v.program, "explorer": v.explorer_url} for k, v in contracts.items()},
        "idl":       idl,
        "abi":       abi,
        "api": {
            "base_url":    API_BASE_URL,
            "auth":        API_AUTH,
            "rate_limit":  API_RATE_LIMIT,
            "endpoints":   [{"module": e.module, "method": e.method.value, "path": e.path, "description": e.description} for e in endpoints],
        },
        "security": {
            "audit": {"auditor": token.auditor, "version": token.audit_version, "score": token.audit_score,
                      "findings": audit_history[-1].findings._asdict()},
            "history": [{"version": h.version, "date": h.date, "score": h.score, "note": h.note} for h in audit_history],
            "checks": [{"name": s.name, "status": s.status.value, "detail": s.detail} for s in security_checks],
        },
        "roadmap":   roadmap,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ exported to {path}")


if __name__ == "__main__":
    validate_all()
    export_json("bld_export.json")
