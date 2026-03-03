-- Webhook table
CREATE TABLE webhooks (
    id INT PRIMARY KEY,
    branch_id INT NOT NULL,
    workstation_id INT NOT NULL,
    rawdata TEXT NOT NULL
);

-- Operator table
CREATE TABLE operators (
    id INT PRIMARY KEY,
    branch_id INT NOT NULL,
    workstation_id INT NOT NULL,
    laptop_ip TEXT NOT NULL,
    laptop_port INT NOT NULL
);

-- Audio table
CREATE TABLE audio (
    id INT PRIMARY KEY,
    operator_id INT NOT NULL,
    audio TEXT NOT NULL,
    status TEXT NOT NULL
);