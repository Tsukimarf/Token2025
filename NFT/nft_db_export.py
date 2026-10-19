"""
NFT Project 2025 — MySQL Database Manager
Handles contract data, tokenomics, roadmap, revenue model
Exports to both SQL dump and JSON
"""

import json
import os
import datetime
import mysql.connector
from mysql.connector import Error

# ── CONFIG ─────────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "database": os.getenv("DB_NAME", "nft_project"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "your_password_here"),
}

SOLANA_NETWORK   = "mainnet-beta"
CONTRACT_ADDRESS = "YOUR_SOLANA_PUBLICKEY_HERE"   # <-- replace with your public key
EXPORT_DIR       = "./exports"
# ───────────────────────────────────────────────────────────────────────────────


PROJECT_DATA = {
    "contract": {
        "address":  CONTRACT_ADDRESS,
        "network":  SOLANA_NETWORK,
        "standard": "Metaplex NFT",
        "program":  "Token Metadata v3",
        "status":   "active",
    },
    "tokenomics": [
        {"category": "Public Mint",        "percentage": 60, "supply": 6000},
        {"category": "Team & Dev",         "percentage": 15, "supply": 1500},
        {"category": "Community Rewards",  "percentage": 15, "supply": 1500},
        {"category": "Reserve / Treasury", "percentage": 10, "supply": 1000},
    ],
    "revenue_model": {
        "total_supply":         10000,
        "mint_price_sol":       1.5,
        "max_revenue_sol":      15000.0,
        "royalty_percent":      7.5,
        "marketplace":          ["Magic Eden", "Tensor"],
        "community_fund_pct":   10,
        "dev_allocation_pct":   15,
    },
    "roadmap": [
        {"quarter": "Q1 2025", "milestone": "Contract deploy",   "status": "done",   "description": "Smart contract deployed on Solana Mainnet"},
        {"quarter": "Q2 2025", "milestone": "Whitelist mint",    "status": "done",   "description": "Whitelist holders minted at 1.0 SOL"},
        {"quarter": "Q3 2025", "milestone": "Public mint",       "status": "active", "description": "Open mint at 1.5 SOL, marketplace listings live"},
        {"quarter": "Q4 2025", "milestone": "Staking & utility", "status": "next",   "description": "Holder staking rewards + token airdrop"},
        {"quarter": "Q1 2026", "milestone": "V2 collection",     "status": "next",   "description": "Second collection drop with revenue share to V1 holders"},
    ],
}


# ── DATABASE SETUP ─────────────────────────────────────────────────────────────

CREATE_TABLES_SQL = """
CREATE DATABASE IF NOT EXISTS nft_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nft_project;

CREATE TABLE IF NOT EXISTS contract_info (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    address         VARCHAR(64)  NOT NULL,
    network         VARCHAR(32)  NOT NULL,
    standard        VARCHAR(64),
    program         VARCHAR(64),
    status          VARCHAR(16)  DEFAULT 'active',
    created_at      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tokenomics (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    category        VARCHAR(64)  NOT NULL,
    percentage      DECIMAL(5,2) NOT NULL,
    supply          INT          NOT NULL
);

CREATE TABLE IF NOT EXISTS revenue_model (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    total_supply          INT            NOT NULL,
    mint_price_sol        DECIMAL(10,4)  NOT NULL,
    max_revenue_sol       DECIMAL(15,4)  NOT NULL,
    royalty_percent       DECIMAL(5,2)   NOT NULL,
    marketplace           JSON,
    community_fund_pct    INT,
    dev_allocation_pct    INT
);

CREATE TABLE IF NOT EXISTS roadmap (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    quarter         VARCHAR(16)  NOT NULL,
    milestone       VARCHAR(128) NOT NULL,
    status          ENUM('done','active','next') DEFAULT 'next',
    description     TEXT
);
"""


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def setup_database(conn):
    cursor = conn.cursor()
    for statement in CREATE_TABLES_SQL.strip().split(";"):
        s = statement.strip()
        if s:
            cursor.execute(s)
    conn.commit()
    cursor.close()
    print("✓ Tables created / verified")


def insert_data(conn):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contract_info")
    c = PROJECT_DATA["contract"]
    cursor.execute(
        "INSERT INTO contract_info (address, network, standard, program, status) VALUES (%s,%s,%s,%s,%s)",
        (c["address"], c["network"], c["standard"], c["program"], c["status"])
    )

    cursor.execute("DELETE FROM tokenomics")
    for t in PROJECT_DATA["tokenomics"]:
        cursor.execute(
            "INSERT INTO tokenomics (category, percentage, supply) VALUES (%s,%s,%s)",
            (t["category"], t["percentage"], t["supply"])
        )

    cursor.execute("DELETE FROM revenue_model")
    r = PROJECT_DATA["revenue_model"]
    cursor.execute(
        "INSERT INTO revenue_model (total_supply, mint_price_sol, max_revenue_sol, royalty_percent, marketplace, community_fund_pct, dev_allocation_pct) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (r["total_supply"], r["mint_price_sol"], r["max_revenue_sol"], r["royalty_percent"],
         json.dumps(r["marketplace"]), r["community_fund_pct"], r["dev_allocation_pct"])
    )

    cursor.execute("DELETE FROM roadmap")
    for item in PROJECT_DATA["roadmap"]:
        cursor.execute(
            "INSERT INTO roadmap (quarter, milestone, status, description) VALUES (%s,%s,%s,%s)",
            (item["quarter"], item["milestone"], item["status"], item["description"])
        )

    conn.commit()
    cursor.close()
    print("✓ Data inserted into all tables")


# ── EXPORTS ────────────────────────────────────────────────────────────────────

def export_json():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    payload = {
        "exported_at": datetime.datetime.utcnow().isoformat() + "Z",
        "project":     "Token2025 NFT",
        "data":        PROJECT_DATA,
    }
    path = os.path.join(EXPORT_DIR, "nft_project_data.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON exported → {path}")
    return path


def export_sql():
    os.makedirs(EXPORT_DIR, exist_ok=True)
    lines = [
        "-- NFT Project 2025 — SQL Data Export",
        f"-- Generated: {datetime.datetime.utcnow().isoformat()}Z",
        "",
        CREATE_TABLES_SQL,
        "",
        "-- ── DATA ────────────────────────────────────────────────────────────",
        "",
    ]

    c = PROJECT_DATA["contract"]
    lines.append("INSERT INTO contract_info (address, network, standard, program, status) VALUES")
    lines.append(f"  ('{c['address']}', '{c['network']}', '{c['standard']}', '{c['program']}', '{c['status']}');")
    lines.append("")

    lines.append("INSERT INTO tokenomics (category, percentage, supply) VALUES")
    rows = [f"  ('{t['category']}', {t['percentage']}, {t['supply']})" for t in PROJECT_DATA["tokenomics"]]
    lines.append(",\n".join(rows) + ";")
    lines.append("")

    r = PROJECT_DATA["revenue_model"]
    mp = json.dumps(r["marketplace"]).replace("'", "\\'")
    lines.append("INSERT INTO revenue_model (total_supply, mint_price_sol, max_revenue_sol, royalty_percent, marketplace, community_fund_pct, dev_allocation_pct) VALUES")
    lines.append(f"  ({r['total_supply']}, {r['mint_price_sol']}, {r['max_revenue_sol']}, {r['royalty_percent']}, '{mp}', {r['community_fund_pct']}, {r['dev_allocation_pct']});")
    lines.append("")

    lines.append("INSERT INTO roadmap (quarter, milestone, status, description) VALUES")
    rrows = [f"  ('{i['quarter']}', '{i['milestone']}', '{i['status']}', '{i['description']}')" for i in PROJECT_DATA["roadmap"]]
    lines.append(",\n".join(rrows) + ";")

    path = os.path.join(EXPORT_DIR, "nft_project_data.sql")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ SQL exported → {path}")
    return path


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    print("── NFT Project DB Manager ──────────────────────────────")

    # Always export files (no DB needed for this)
    export_json()
    export_sql()

    # Try DB connection (optional — skip if no DB configured)
    try:
        print("\nConnecting to MySQL...")
        conn = get_connection()
        setup_database(conn)
        insert_data(conn)
        conn.close()
        print("✓ Database sync complete")
    except Error as e:
        print(f"⚠  MySQL not available ({e}) — files exported only")

    print("\n── Done ─────────────────────────────────────────────────")


if __name__ == "__main__":
    main()
