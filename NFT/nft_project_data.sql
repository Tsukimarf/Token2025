-- NFT Project 2025 — SQL Data Export
-- Network: Solana Mainnet-Beta
-- Generated: 2025-06-07T00:00:00Z

CREATE DATABASE IF NOT EXISTS nft_project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nft_project;

-- ── TABLES ────────────────────────────────────────────────────────────────────

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

-- ── DATA ──────────────────────────────────────────────────────────────────────

INSERT INTO contract_info (address, network, standard, program, status) VALUES
  ('YOUR_SOLANA_PUBLICKEY_HERE', 'mainnet-beta', 'Metaplex NFT', 'Token Metadata v3', 'active');

INSERT INTO tokenomics (category, percentage, supply) VALUES
  ('Public Mint',        60.00, 6000),
  ('Team & Dev',         15.00, 1500),
  ('Community Rewards',  15.00, 1500),
  ('Reserve / Treasury', 10.00, 1000);

INSERT INTO revenue_model (total_supply, mint_price_sol, max_revenue_sol, royalty_percent, marketplace, community_fund_pct, dev_allocation_pct) VALUES
  (10000, 1.5000, 15000.0000, 7.50, '["Magic Eden", "Tensor"]', 10, 15);

INSERT INTO roadmap (quarter, milestone, status, description) VALUES
  ('Q1 2025', 'Contract deploy',   'done',   'Smart contract deployed on Solana Mainnet'),
  ('Q2 2025', 'Whitelist mint',    'done',   'Whitelist holders minted at 1.0 SOL'),
  ('Q3 2025', 'Public mint',       'active', 'Open mint at 1.5 SOL, marketplace listings live'),
  ('Q4 2025', 'Staking & utility', 'next',   'Holder staking rewards + token airdrop'),
  ('Q1 2026', 'V2 collection',     'next',   'Second collection drop with revenue share to V1 holders');
