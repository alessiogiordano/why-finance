#
#  stocks_commands.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 18/12/24.
#

from utils.database import connect
from utils.logger import logger

class CommandHandler:
    def __init__(self, db_config = None):
        self.db_config = db_config
    #-------------------------------------------------------------------------------------
    def save_stock_data(self, ticker, value, timestamp):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stocks (ticker, value, timestamp) VALUES (%s, %s, %s)",
            (ticker, value, timestamp)
        )
        conn.commit()
        conn.close()
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------