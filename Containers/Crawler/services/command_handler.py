from database.connection import connect_to_db

class CommandHandler:
    def __init__(self, db_config):
        self.db_config = db_config

    def save_stock_data(self, ticker, value, timestamp):
        """
        Salva i dati di uno stock nel database.
        """
        conn = connect_to_db(self.db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stock_data (ticker, value, timestamp) VALUES (%s, %s, %s)",
            (ticker, value, timestamp)
        )
        conn.commit()
        conn.close()
