from database.connection import connect_to_db

class CommandHandler:
    def __init__(self, db_config):
        self.db_config = db_config

    def register_user(self, device_id, ticker, device_token, low_value, high_value):
        if low_value is not None and high_value is not None and low_value >= high_value:
            raise ValueError("Il valore low_value deve essere minore di high_value.")
        conn = connect_to_db(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (device_id, ticker, device_token, low_value, high_value) VALUES (%s, %s, %s, %s, %s)",
            (device_id, ticker, device_token, low_value, high_value),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def update_user(self, device_id, ticker, device_token, low_value, high_value):
        if low_value is not None and high_value is not None and low_value >= high_value:
            raise ValueError("Il valore low_value deve essere minore di high_value.")
        conn = connect_to_db(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET ticker = %s, device_token = %s, low_value = %s, high_value = %s WHERE device_id = %s",
            (ticker, device_token, low_value, high_value, device_id),
        )
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success

    def delete_user(self, device_id):
        conn = connect_to_db(self.db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE device_id = %s", (device_id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return success
