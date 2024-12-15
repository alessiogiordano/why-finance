CREATE DATABASE IF NOT EXISTS migration_db;

USE migration_db;

CREATE TABLE IF NOT EXISTS migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL,
    target_database VARCHAR(255) NOT NULL,
    status ENUM('pending', 'run', 'error') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    error_message TEXT NULL
);
