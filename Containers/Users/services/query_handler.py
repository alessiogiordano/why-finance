from database.connection import connect_to_db

class QueryHandler:
    def __init__(self, db_config):
        self.db_config = db_config

    def user_exists(self, device_id):
        conn = connect_to_db(self.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE device_id = %s", (device_id,))
        exists = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()
        return exists
