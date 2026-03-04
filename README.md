-- Webhook table
CREATE TABLE webhooks (
    id INT PRIMARY KEY,
    branch_id INT NOT NULL,
    workstation_id INT NOT NULL,
    rawdata TEXT NOT NULL
);

-- Operator table
CREATE TABLE operators (
    id SERIAL PRIMARY KEY,
    branch_id INT NOT NULL,
    workstation_id INT NOT NULL UNIQUE,
    laptop_ip TEXT NOT NULL,
    laptop_port INT NOT NULL
);

-- Audio table
CREATE TABLE audios (
    id SERIAL PRIMARY KEY,
    operator_id INT NOT NULL REFERENCES operators(id),
    webhook_id INT NOT NULL UNIQUE REFERENCES webhooks(id),
    audio TEXT,
    status TEXT NOT NULL
);