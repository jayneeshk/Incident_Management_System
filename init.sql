CREATE TABLE IF NOT EXISTS incidents (
    incident_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(255),
    severity VARCHAR(50),
    description TEXT,
    status VARCHAR(50)
);