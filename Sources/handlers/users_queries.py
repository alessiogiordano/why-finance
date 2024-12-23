#
#  users_queries.py
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
    def user_exists(self, device_id):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE device_id = %s", (device_id,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
    #-------------------------------------------------------------------------------------
    def get_all_tickers(self):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ticker FROM users")
        tickers = cursor.fetchall()
        conn.close()
        return tickers
    #-------------------------------------------------------------------------------------
    def foreach_user_with_ticker(self, ticker, callback):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT device_id, ticker, device_token, high_value, low_value from users WHERE ticker = %s", (ticker,))
        while True:
            users = cursor.fetchmany(1000)
            if len(users) == 0:
                break
            for user in users:
                callback({
                    'device_id': user[0],
                    'ticker': user[1],
                    'device_token': user[2],
                    'high_value': user[3],
                    'low_value': user[4]
                })
        conn.close()
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------