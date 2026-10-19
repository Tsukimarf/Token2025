CREATE TABLE pythagoras_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    wallet_address VARCHAR(64) NOT NULL,
    side_a DOUBLE NOT NULL,
    side_b DOUBLE NOT NULL,
    hypotenuse_c DOUBLE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO pythagoras_records (wallet_address, side_a, side_b, hypotenuse_c) 
-- Add seed data only after a valid Solana public key is available.
