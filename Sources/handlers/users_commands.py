#
#  users_commands.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 18/12/24.
#

from utils.database import connect

class CommandHandler:
    def __init__(self, db_config = None):
        self.db_config = db_config
    #-------------------------------------------------------------------------------------
    def register_user(self, device_id, ticker, device_token, high_value, low_value):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (device_id, ticker, device_token, low_value, high_value) VALUES (%s, %s, %s, %s, %s)",
            (device_id, ticker, device_token, low_value, high_value),
        )
        conn.commit()
        cursor.close()
        conn.close()
    #-------------------------------------------------------------------------------------
    def update_user(self, device_id, ticker, device_token, high_value, low_value):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET ticker = %s, device_token = %s, low_value = %s, high_value = %s WHERE device_id = %s",
            (ticker, device_token, low_value, high_value, device_id),
        )
        conn.commit()
        #success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        #return success
    #-------------------------------------------------------------------------------------
    def delete_user(self, device_id):
        conn = connect(self.db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE device_id = %s", (device_id,))
        conn.commit()
        #success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        #return success
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------