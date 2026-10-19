-- ═══════════════════════════════════════════════════════════════════
-- BIT LANER DETH ($BLD) — Full Database
-- Network : Solana Mainnet-Beta
-- Version : 2.0
-- GitHub  : github.com/Tsukimarf/Token2025
-- ═══════════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS bld_token
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE bld_token;

-- ── TABLES ────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS token_info (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  name             VARCHAR(64)   NOT NULL,
  symbol           VARCHAR(16)   NOT NULL,
  network          VARCHAR(64)   NOT NULL,
  decimals         TINYINT       DEFAULT 9,
  total_supply     BIGINT        NOT NULL,
  circulating      BIGINT        NOT NULL,
  burned           BIGINT        AS (total_supply - circulating) STORED,
  contract_address VARCHAR(64),
  mint_authority   VARCHAR(64),
  freeze_authority VARCHAR(64),
  version          VARCHAR(8)    DEFAULT '2.0',
  status           VARCHAR(32)   DEFAULT 'pre-mainnet',
  audit_score      TINYINT,
  auditor          VARCHAR(64),
  updated_at       DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tokenomics (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  bucket   VARCHAR(64)    NOT NULL,
  pct      DECIMAL(5,2)   NOT NULL,
  amount   BIGINT         NOT NULL,
  locked   BOOLEAN        DEFAULT FALSE,
  vested   BOOLEAN        DEFAULT FALSE,
  notes    TEXT
);

CREATE TABLE IF NOT EXISTS tx_fees (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  fee_type    VARCHAR(64)   NOT NULL,
  pct         DECIMAL(5,2)  NOT NULL,
  destination VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS nft_collection (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  collection_name  VARCHAR(128),
  total_supply     INT,
  mint_price_sol   DECIMAL(10,4),
  wl_price_sol     DECIMAL(10,4),
  royalty_pct      DECIMAL(5,2),
  staking_reward   BIGINT,
  burn_claim       BIGINT,
  max_monthly_emit BIGINT,
  candy_machine    VARCHAR(64),
  standard         VARCHAR(64),
  storage          VARCHAR(32),
  status           VARCHAR(32)   DEFAULT 'pre-deploy'
);

CREATE TABLE IF NOT EXISTS nft_rarity (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  tier        VARCHAR(32)  NOT NULL,
  supply      INT          NOT NULL,
  probability DECIMAL(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS nft_mint_phases (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  phase       TINYINT      NOT NULL,
  name        VARCHAR(64),
  supply      INT,
  price_sol   DECIMAL(10,4),
  window_hrs  INT,
  status      VARCHAR(32)  DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS roadmap (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  phase    TINYINT      NOT NULL,
  name     VARCHAR(128) NOT NULL,
  tasks    TEXT,
  status   ENUM('done','active','pending') DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS contract_addresses (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  label    VARCHAR(64),
  address  VARCHAR(64),
  network  VARCHAR(32),
  status   VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS dex_listings (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  exchange    VARCHAR(64),
  chain       VARCHAR(32),
  type        ENUM('dex','cex','analytics'),
  status      VARCHAR(32)  DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS security_checks (
  id       INT AUTO_INCREMENT PRIMARY KEY,
  item     VARCHAR(128) NOT NULL,
  status   ENUM('pass','mitigated','pending','fail') DEFAULT 'pending',
  version  VARCHAR(8),
  notes    TEXT
);

CREATE TABLE IF NOT EXISTS api_endpoints (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  category    VARCHAR(32),
  method      ENUM('GET','POST','PUT','DELETE') NOT NULL,
  path        VARCHAR(128) NOT NULL,
  description VARCHAR(256)
);

-- ── DATA ──────────────────────────────────────────────────────────

INSERT INTO token_info
  (name,symbol,network,decimals,total_supply,circulating,contract_address,
   version,status,audit_score,auditor)
VALUES (
  'Bit Laner Deth','BLD','Solana mainnet-beta',9,
  1000000000000,600000000000,'YOUR_SOLANA_PUBLICKEY_HERE',
  '2.0','pre-mainnet',94,'OtterSec'
);

INSERT INTO tokenomics (bucket,pct,amount,locked,vested,notes) VALUES
  ('Burned at launch',  40, 400000000000, FALSE, FALSE, 'Genesis burn — permanent'),
  ('Locked liquidity',  30, 300000000000, TRUE,  FALSE, 'Raydium LP locked, cannot be withdrawn'),
  ('Community airdrop', 20, 200000000000, FALSE, FALSE, 'NFT rewards + airdrops'),
  ('Dev and team',      10, 100000000000, FALSE, TRUE,  '12-month vesting schedule');

INSERT INTO tx_fees (fee_type,pct,destination) VALUES
  ('Holder redistribution',    5, 'All BLD holders proportional'),
  ('Liquidity pool',           3, 'Raydium auto-add'),
  ('Marketing & meme warfare', 2, 'Community campaigns');

INSERT INTO nft_collection
  (collection_name,total_supply,mint_price_sol,wl_price_sol,royalty_pct,
   staking_reward,burn_claim,max_monthly_emit,candy_machine,standard,storage,status)
VALUES (
  'BLD Skull Series',10000,0.1000,0.0800,5.00,
  50000,5000000,500000000,
  'YOUR_CANDY_MACHINE_ADDRESS_HERE',
  'Metaplex NFT v1.1','Arweave/IPFS','pre-deploy'
);

INSERT INTO nft_rarity (tier,supply,probability) VALUES
  ('Common',    5500, 55.00),
  ('Rare',      2800, 28.00),
  ('Epic',      1200, 12.00),
  ('Legendary',  500,  5.00);

INSERT INTO nft_mint_phases (phase,name,supply,price_sol,window_hrs,status) VALUES
  (1, 'Whitelist',      500,  0.08, 48,   'pending'),
  (2, 'Public Mint',    9000, 0.10, NULL, 'pending'),
  (3, 'Staking Live',   NULL, NULL, NULL, 'pending'),
  (4, 'Burn Event #1',  NULL, NULL,  720, 'pending');

INSERT INTO roadmap (phase,name,tasks,status) VALUES
  (1,'Kebangkitan Tengkorak','Token launch, Website, Telegram & Twitter, Airdrop 1M BLD','pending'),
  (2,'Meme Menyerang','DEX listing Raydium, Global meme contest, Meme DAO partnership','pending'),
  (3,'Deth to the Moon','CMC & CoinGecko listing, Burn event #1, Skull NFTs release, Staking live','pending'),
  (4,'DETHCENOMICS','DAO voting Realms, Merchandise store, Multi-chain BNB, Second audit','pending');

INSERT INTO contract_addresses (label,address,network,status) VALUES
  ('BLD SPL Token',         'YOUR_SOLANA_PUBLICKEY_HERE',      'mainnet-beta', 'pending'),
  ('NFT Candy Machine v3',  'YOUR_CANDY_MACHINE_ADDRESS_HERE', 'mainnet-beta', 'pending'),
  ('Raydium Liquidity Pool','pending',                         'mainnet-beta', 'pending'),
  ('Treasury Squads v4',    'pending',                         'mainnet-beta', 'pending');

INSERT INTO dex_listings (exchange,chain,type,status) VALUES
  ('Raydium',       'Solana',    'dex',       'pending'),
  ('Jupiter',       'Solana',    'dex',       'pending'),
  ('Orca',          'Solana',    'dex',       'pending'),
  ('PancakeSwap',   'BNB Chain', 'dex',       'planned'),
  ('CoinMarketCap', 'CEX',       'cex',       'planned'),
  ('CoinGecko',     'CEX',       'cex',       'planned'),
  ('DEXTools',      'Analytics', 'analytics', 'planned'),
  ('Birdeye',       'Analytics', 'analytics', 'planned');

INSERT INTO security_checks (item,status,version,notes) VALUES
  ('Mint authority disabled',             'pass',      '2.0', NULL),
  ('Freeze authority revoked',            'pass',      '2.0', NULL),
  ('Reentrancy protection',               'pass',      '2.0', NULL),
  ('PDA ownership validated',             'pass',      '2.0', NULL),
  ('Signer verification',                 'pass',      '2.0', NULL),
  ('Integer overflow checked_add/sub',    'pass',      '2.0', NULL),
  ('On-chain verification solana-verify', 'pass',      '2.0', NULL),
  ('Reward vault drain limit',            'mitigated', '2.1', 'Rate limiter 500M BLD/epoch'),
  ('NFT metadata mutability',             'pending',   '2.1', 'Freeze post-reveal');

INSERT INTO api_endpoints (category,method,path,description) VALUES
  ('token',   'GET',  '/v1/token/info',              'Token metadata'),
  ('token',   'GET',  '/v1/token/supply',             'Supply breakdown'),
  ('token',   'GET',  '/v1/token/balance/{wallet}',   'Wallet BLD balance'),
  ('token',   'POST', '/v1/token/transfer',           'Send BLD'),
  ('nft',     'GET',  '/v1/nft/collection',           'Collection info'),
  ('nft',     'GET',  '/v1/nft/{mint_address}',       'Single NFT metadata'),
  ('nft',     'GET',  '/v1/nft/wallet/{wallet}',      'NFTs owned by wallet'),
  ('nft',     'POST', '/v1/nft/mint',                 'Mint skull NFT'),
  ('staking', 'POST', '/v1/staking/stake',            'Stake NFT'),
  ('staking', 'POST', '/v1/staking/unstake',          'Unstake NFT'),
  ('staking', 'GET',  '/v1/staking/pending/{wallet}', 'Pending BLD rewards'),
  ('staking', 'POST', '/v1/staking/claim',            'Claim rewards'),
  ('burn',    'POST', '/v1/burn/claim',               'Burn NFT receive 5M BLD'),
  ('burn',    'GET',  '/v1/burn/history/{wallet}',    'Burn history'),
  ('burn',    'GET',  '/v1/burn/vault',               'Vault balance');
