import logging
from database.connection import connect_to_db

logger = logging.getLogger(__name__)

class QueryHandler:
    def __init__(self):
        # Creazione di connessioni distinte
        self.user_conn = connect_to_db('user')
        self.ticker_conn = connect_to_db('ticker')

    def get_last_stock_value(self, ticker):
        """
        Query per ottenere l'ultimo valore di una stock dal database ticker.
        """
        try:
            cursor = self.ticker_conn.cursor()
            cursor.execute(
                """
                SELECT value 
                FROM stock_data 
                WHERE ticker = %s 
                ORDER BY timestamp DESC 
                LIMIT 1
                """,
                (ticker,)
            )
            result = cursor.fetchone()
            cursor.close()
            logger.info(f"Ultimo valore della stock {ticker}: {result[0] if result else 'N/A'}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Errore durante la query di stock data: {e}")
            raise

    def calculate_average_stock_value(self, ticker, count):
        """
        Query per calcolare il valore medio di una stock.
        """
        try:
            cursor = self.ticker_conn.cursor()
            cursor.execute(
                """
                SELECT AVG(value) 
                FROM (
                    SELECT value 
                    FROM stock_data 
                    WHERE ticker = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                ) as recent_values
                """,
                (ticker, count)
            )
            result = cursor.fetchone()
            cursor.close()
            logger.info(f"Valore medio calcolato per la stock {ticker}: {result[0] if result else 'N/A'}")
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Errore durante il calcolo del valore medio: {e}")
            raise

    def get_user_statistics(self):
        """
        Query per ottenere statistiche degli utenti dal database user.
        """
        try:
            cursor = self.user_conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            cursor.close()
            logger.info(f"Numero totale di utenti: {user_count}")
            return user_count
        except Exception as e:
            logger.error(f"Errore durante il recupero delle statistiche degli utenti: {e}")
            raise
