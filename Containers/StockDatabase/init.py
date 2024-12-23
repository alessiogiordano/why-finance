#
#  create_tables.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

from utils.database import initialize_database

if __name__ == "__main__":
    initialize_database('stocks', """
        CREATE TABLE IF NOT EXISTS stocks (
            ticker VARCHAR(16),
            value DECIMAL(10, 2),
            timestamp DATETIME
    );
    """)
#-----------------------------------------------------------------------------------------