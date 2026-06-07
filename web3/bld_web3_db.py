"""
BLD Token — Web3 Full Database Manager
Solana Mainnet-Beta | Version 2.0
github.com/Tsukimarf/Token2025
"""

from __future__ import annotations
import json, os, datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List
from enum import Enum

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("⚠  mysql-connector-python not installed. Run: pip install mysql-connector-python")

# ── CONFIG ────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "bld_token"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "your_password_here"),
}

CONTRACT_ADDRESS  = "YOUR_SOLANA_PUBLICKEY_HERE"
CANDY_MACHINE     = "YOUR_CANDY_MACHINE_ADDRESS_HERE"
SOLANA_NETWORK    = "mainnet-beta"
EXPORT_DIR        = "./exports"
# ─────────────────────────────────────────────────────────────────


class Network(Enum):
    MAINNET = "mainnet-beta"
    DEVNET  = "devnet"

class RoadmapStatus(Enum):
    DONE    = "done"
    ACTIVE  = "active"
    PENDING = "pending"


@dataclass(frozen=True)
class TokenInfo:
    name:             str  = "Bit Laner Deth"
    symbol:           str  = "BLD"
    network:          str  = SOLANA_NETWORK
    decimals:         int  = 9
    total_supply:     int  = 1_000_000_000_000
    circulating:      int  = 600_000_000_000
    contract_address: str  = CONTRACT_ADDRESS
    version:          str  = "2.0"
    status:           str  = "pre-mainnet"
    audit_score:      int  = 94
    auditor:          str  = "OtterSec"

    @property
    def burned(self) -> int:
        return self.total_supply - self.circulating


@dataclass
class NFTCollection:
    name:           str   = "BLD Skull Series"
    supply:         int   = 10_000
    mint_price:     float = 0.1
    wl_price:       float = 0.08
    royalty:        float = 5.0
    staking_reward: int   = 50_000
    burn_claim:     int   = 5_000_000
    candy_machine:  str   = CANDY_MACHINE
    rarity: List[dict] = field(default_factory=lambda: [
        {"tier": "Common",    "supply": 5500, "probability": 0.55},
        {"tier": "Rare",      "supply": 2800, "probability": 0.28},
        {"tier": "Epic",      "supply": 1200, "probability": 0.12},
        {"tier": "Legendary", "supply": 500,  "probability": 0.05},
    ])


TOKEN = TokenInfo()
NFT   = NFTCollection()

TOKENOMICS = [
    {"bucket": "Burned at launch",  "pct": 40, "amount": 400_000_000_000, "locked": False, "vested": False},
    {"bucket": "Locked liquidity",  "pct": 30, "amount": 300_000_000_000, "locked": True,  "vested": False},
    {"bucket": "Community airdrop", "pct": 20, "amount": 200_000_000_000, "locked": False, "vested": False},
    {"bucket": "Dev and team",      "pct": 10, "amount": 100_000_000_000, "locked": False, "vested": True },
]

ROADMAP = [
    {"phase": 1, "name": "Kebangkitan Tengkorak", "tasks": "Token launch, Website, Telegram, Airdrop 1M BLD", "status": "pending"},
    {"phase": 2, "name": "Meme Menyerang",        "tasks": "DEX listing, Meme contest, DAO partnership",     "status": "pending"},
    {"phase": 3, "name": "Deth to the Moon",      "tasks": "CMC listing, Burn event #1, NFTs release",       "status": "pending"},
    {"phase": 4, "name": "DETHCENOMICS",           "tasks": "DAO voting, Merchandise, Multi-chain",           "status": "pending"},
]

CONTRACTS = [
    {"label": "BLD SPL Token",         "address": CONTRACT_ADDRESS, "network": SOLANA_NETWORK, "status": "pending"},
    {"label": "NFT Candy Machine v3",  "address": CANDY_MACHINE,   "network": SOLANA_NETWORK, "status": "pending"},
    {"label": "Raydium Liquidity Pool","address": "pending",        "network": SOLANA_NETWORK, "status": "pending"},
    {"label": "Treasury Squads v4",    "address": "pending",        "network": SOLANA_NETWORK, "status": "pending"},
]


# ── DATABASE SETUP ────────────────────────────────────────────────

def setup_db(conn):
    cursor = conn.cursor()
    stmts = [
        """CREATE TABLE IF NOT EXISTS token_info (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(64), symbol VARCHAR(16), network VARCHAR(64),
          decimals TINYINT DEFAULT 9, total_supply BIGINT, circulating BIGINT,
          contract_address VARCHAR(64), version VARCHAR(8), status VARCHAR(32),
          audit_score TINYINT, auditor VARCHAR(64),
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)""",

        """CREATE TABLE IF NOT EXISTS tokenomics (
          id INT AUTO_INCREMENT PRIMARY KEY,
          bucket VARCHAR(64), pct DECIMAL(5,2), amount BIGINT,
          locked BOOLEAN DEFAULT FALSE, vested BOOLEAN DEFAULT FALSE)""",

        """CREATE TABLE IF NOT EXISTS nft_collection (
          id INT AUTO_INCREMENT PRIMARY KEY,
          collection_name VARCHAR(128), total_supply INT,
          mint_price_sol DECIMAL(10,4), wl_price_sol DECIMAL(10,4),
          royalty_pct DECIMAL(5,2), staking_reward BIGINT,
          burn_claim BIGINT, candy_machine VARCHAR(64),
          standard VARCHAR(64), storage VARCHAR(32))""",

        """CREATE TABLE IF NOT EXISTS roadmap (
          id INT AUTO_INCREMENT PRIMARY KEY,
          phase TINYINT, name VARCHAR(128), tasks TEXT,
          status ENUM('done','active','pending') DEFAULT 'pending')""",

        """CREATE TABLE IF NOT EXISTS contract_addresses (
          id INT AUTO_INCREMENT PRIMARY KEY,
          label VARCHAR(64), address VARCHAR(64),
          network VARCHAR(32), status VARCHAR(32))""",
    ]
    for s in stmts:
        cursor.execute(s)
    conn.commit()
    cursor.close()
    print("✓ Tables ready")


def insert_all(conn):
    cur = conn.cursor()

    cur.execute("DELETE FROM token_info")
    cur.execute("""INSERT INTO token_info
        (name,symbol,network,decimals,total_supply,circulating,
         contract_address,version,status,audit_score,auditor) VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (TOKEN.name, TOKEN.symbol, TOKEN.network, TOKEN.decimals,
         TOKEN.total_supply, TOKEN.circulating, TOKEN.contract_address,
         TOKEN.version, TOKEN.status, TOKEN.audit_score, TOKEN.auditor))

    cur.execute("DELETE FROM tokenomics")
    for t in TOKENOMICS:
        cur.execute("INSERT INTO tokenomics (bucket,pct,amount,locked,vested) VALUES (%s,%s,%s,%s,%s)",
                    (t["bucket"], t["pct"], t["amount"], t["locked"], t["vested"]))

    cur.execute("DELETE FROM nft_collection")
    cur.execute("""INSERT INTO nft_collection
        (collection_name,total_supply,mint_price_sol,wl_price_sol,royalty_pct,
         staking_reward,burn_claim,candy_machine,standard,storage) VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (NFT.name, NFT.supply, NFT.mint_price, NFT.wl_price, NFT.royalty,
         NFT.staking_reward, NFT.burn_claim, NFT.candy_machine,
         "Metaplex NFT v1.1", "Arweave/IPFS"))

    cur.execute("DELETE FROM roadmap")
    for r in ROADMAP:
        cur.execute("INSERT INTO roadmap (phase,name,tasks,status) VALUES (%s,%s,%s,%s)",
                    (r["phase"], r["name"], r["tasks"], r["status"]))

    cur.execute("DELETE FROM contract_addresses")
    for c in CONTRACTS:
        cur.execute("INSERT INTO contract_addresses (label,address,network,status) VALUES (%s,%s,%s,%s)",
                    (c["label"], c["address"], c["network"], c["status"]))

    conn.commit()
    cur.close()
    print("✓ All data inserted")


# ── EXPORTS ───────────────────────────────────────────────────────

def export_json():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    payload = {
        "meta": {
            "project": TOKEN.name,
            "symbol":  TOKEN.symbol,
            "version": TOKEN.version,
            "exported_at": datetime.datetime.utcnow().isoformat() + "Z",
            "github": "github.com/Tsukimarf/Token2025",
        },
        "token":      {
            "name":             TOKEN.name,
            "symbol":           TOKEN.symbol,
            "network":          TOKEN.network,
            "decimals":         TOKEN.decimals,
            "total_supply":     TOKEN.total_supply,
            "circulating":      TOKEN.circulating,
            "burned":           TOKEN.burned,
            "contract_address": TOKEN.contract_address,
            "version":          TOKEN.version,
            "audit_score":      TOKEN.audit_score,
        },
        "tokenomics": TOKENOMICS,
        "nft":        {"name": NFT.name, "supply": NFT.supply,
                       "mint_price": NFT.mint_price, "staking_reward": NFT.staking_reward,
                       "burn_claim": NFT.burn_claim, "rarity": NFT.rarity},
        "roadmap":    ROADMAP,
        "contracts":  CONTRACTS,
    }
    path = os.path.join(EXPORT_DIR, "bld_database.json")
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"✓ JSON → {path}")
    return path


def export_sql():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, "bld_database.sql")
    with open(path, "w") as f:
        f.write(f"-- BLD Token Database Export\n-- {datetime.datetime.utcnow().isoformat()}Z\n\n")
        f.write(f"INSERT INTO token_info (name,symbol,network,decimals,total_supply,circulating,contract_address,version) VALUES\n")
        f.write(f"  ('{TOKEN.name}','{TOKEN.symbol}','{TOKEN.network}',{TOKEN.decimals},{TOKEN.total_supply},{TOKEN.circulating},'{TOKEN.contract_address}','{TOKEN.version}');\n\n")
        f.write("INSERT INTO tokenomics (bucket,pct,amount,locked,vested) VALUES\n")
        rows = [f"  ('{t['bucket']}',{t['pct']},{t['amount']},{int(t['locked'])},{int(t['vested'])})" for t in TOKENOMICS]
        f.write(",\n".join(rows) + ";\n\n")
        f.write("INSERT INTO roadmap (phase,name,tasks,status) VALUES\n")
        rows = [f"  ({r['phase']},'{r['name']}','{r['tasks']}','{r['status']}')" for r in ROADMAP]
        f.write(",\n".join(rows) + ";\n")
    print(f"✓ SQL  → {path}")
    return path


# ── MAIN ──────────────────────────────────────────────────────────

def main():
    print("── BLD Web3 DB Manager ─────────────────────────────────")
    print(f"   Token:    {TOKEN.name} ({TOKEN.symbol})")
    print(f"   Supply:   {TOKEN.total_supply:,}")
    print(f"   Burned:   {TOKEN.burned:,}")
    print(f"   Address:  {TOKEN.contract_address}")
    print(f"   Network:  {TOKEN.network}\n")

    export_json()
    export_sql()

    if MYSQL_AVAILABLE:
        try:
            print("\nConnecting to MySQL...")
            conn = mysql.connector.connect(**DB_CONFIG)
            setup_db(conn)
            insert_all(conn)
            conn.close()
            print("✓ MySQL sync complete")
        except Exception as e:
            print(f"⚠  MySQL unavailable ({e}) — files exported only")

    print("\n── Done 💀 ─────────────────────────────────────────────")


if __name__ == "__main__":
    main()
