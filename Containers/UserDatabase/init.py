#
#  init.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

from utils.database import initialize_database

if __name__ == "__main__":
    initialize_database('users', """
        CREATE TABLE IF NOT EXISTS users (
            device_id VARCHAR(255) PRIMARY KEY,
            ticker VARCHAR(16) NOT NULL,
            device_token VARCHAR(255),
            high_value DECIMAL(10, 2),
            low_value DECIMAL(10, 2)
        );
    """)
#-----------------------------------------------------------------------------------------