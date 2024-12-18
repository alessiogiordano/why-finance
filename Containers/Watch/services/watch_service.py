import watch_pb2
import watch_pb2_grpc
import grpc
from services.query_handler import QueryHandler
from utils.logger import logger

class WatchService(watch_pb2_grpc.WatchServiceServicer):
    def __init__(self):
        # Inizializziamo il query handler
        self.query_handler = QueryHandler()
        self.print_db_stats()

    def print_db_stats(self):
        """
        Stampa alcune statistiche del database all'avvio del server.
        """
        try:
            user_count = self.query_handler.get_user_statistics()
            # Eseguiamo query direttamente tramite QueryHandler per statistiche stock
            conn = self.query_handler.ticker_conn
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM stock_data")
            stock_data_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT ticker, value, timestamp 
                FROM stock_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            last_stock = cursor.fetchone()

            logger.info("\n" + "="*50)
            logger.info("Statistiche del Database:")
            logger.info(f"Totale utenti: {user_count}")
            logger.info(f"Totale record di stock data: {stock_data_count}")
            if last_stock:
                logger.info(f"Ultima stock registrata: {last_stock[0]} - Valore: {last_stock[1]} at {last_stock[2]}")
            logger.info("="*50 + "\n")

            cursor.close()

        except Exception as e:
            logger.error(f"Errore durante il recupero delle statistiche del database: {e}")

    def GetLastStockValue(self, request, context):
        """
        Metodo gRPC per ottenere l'ultimo valore di una stock.
        """
        try:
            logger.info(f"Ricevuta richiesta GetLastStockValue per ticker: {request.ticker}")
            value = self.query_handler.get_last_stock_value(request.ticker)
            if value is not None:
                return watch_pb2.StockResponse(value=value)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Nessun dato trovato per questa stock")
                return watch_pb2.StockResponse(value=0.0)
        except Exception as e:
            logger.error(f"Errore durante GetLastStockValue: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Errore: {e}")
            return watch_pb2.StockResponse(value=0.0)

    def CalculateAverageStockValue(self, request, context):
        """
        Metodo gRPC per calcolare il valore medio di una stock.
        """
        try:
            logger.info(f"Ricevuta richiesta CalculateAverageStockValue per ticker: {request.ticker}, count: {request.count}")
            average_value = self.query_handler.calculate_average_stock_value(request.ticker, request.count)
            if average_value is not None:
                return watch_pb2.StockResponse(value=average_value)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Nessun dato trovato per questa stock")
                return watch_pb2.StockResponse(value=0.0)
        except Exception as e:
            logger.error(f"Errore durante CalculateAverageStockValue: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Errore: {e}")
            return watch_pb2.StockResponse(value=0.0)
