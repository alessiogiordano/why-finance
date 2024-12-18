from database.connection import connect_to_db

class QueryHandler:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all_tickers(self):
        """
        Recupera tutti i ticker univoci dal database.
        """
        conn = connect_to_db(self.db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ticker FROM users")
        tickers = [row[0] for row in cursor.fetchall()] #TODO: review this row, because the original query is: tickers = cursor.fetchall()
        conn.close()
        return tickers