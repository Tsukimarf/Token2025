CREATE TABLE pythagoras_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    wallet_address VARCHAR(42) NOT NULL,
    side_a DOUBLE NOT NULL,
    side_b DOUBLE NOT NULL,
    hypotenuse_c DOUBLE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO pythagoras_records (wallet_address, side_a, side_b, hypotenuse_c) 
VALUES ('0x0000000000000000000000000000000000000000', 3, 4, 5);
