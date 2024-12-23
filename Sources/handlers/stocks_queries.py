#
#  stocks_queries.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 18/12/24.
#

from utils.database import connect

class QueryHandler:
    def __init__(self, db_config = None):
        self.db_config = db_config
    #-------------------------------------------------------------------------------------
    def get_last_stock_value(self, ticker):
        conn = connect(self.db_config)
        cursor = self.ticker_conn.cursor()
        cursor.execute(
            """
            SELECT value 
            FROM stocks 
            WHERE ticker = %s 
            ORDER BY timestamp DESC 
            LIMIT 1
            """,
            (ticker,)
        )
        result = cursor.fetchone()
        cursor.close()
        logger.info(f"LAST STOCK VALUE FOR {ticker}: {result[0] if result else 'N/A'}")
        conn.close()
        return result[0] if result else None
    #-------------------------------------------------------------------------------------
    def calculate_average_stock_value(self, ticker, count):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT AVG(value) 
            FROM (
                SELECT value 
                FROM stocks 
                WHERE ticker = %s 
                ORDER BY timestamp DESC 
                LIMIT %s
            ) as recent_values
            """,
            (ticker, count)
        )
        result = cursor.fetchone()
        cursor.close()
        logger.info(f"AVERAGE STOCK VALUE FOR {ticker}: {result[0] if result else 'N/A'}")
        conn.close()
        return result[0] if result else None
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------