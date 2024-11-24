import grpc
from concurrent import futures
import mysql.connector
import os
from datetime import datetime
import logging

import watch_pb2
import watch_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log")
    ]
)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "dsbd_homework1"),
    "port": int(os.getenv("DB_PORT", 3306))
}

class WatchService(watch_pb2_grpc.WatchServiceServicer):
    def __init__(self):
        self.print_db_stats()

    def print_db_stats(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM stock_data")
            stock_data_count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT ticker, value, timestamp 
                FROM stock_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            last_stock = cursor.fetchone()
            
            logger.info("Database Statistics:")
            logger.info(f"Total Users: {user_count}")
            logger.info(f"Total Stock Data Records: {stock_data_count}")
            if last_stock:
                logger.info(f"Last Stock Update: {last_stock[0]} - Value: {last_stock[1]} at {last_stock[2]}")
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            logger.error(f"Error accessing database: {err}")

    def GetLastStockValue(self, request, context):
        try:
            logger.info(f"Received GetLastStockValue request for email: {request.email}")
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT value 
                FROM stock_data 
                WHERE email = %s 
                ORDER BY timestamp DESC 
                LIMIT 1
                """,
                (request.email,)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                logger.info(f"Stock value retrieved for {request.email}: {result[0]}")
                return watch_pb2.StockResponse(value=result[0])
            else:
                logger.warning(f"No stock data found for email: {request.email}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No stock data found for this user")
                return watch_pb2.StockResponse(value=0.0)
            
        except mysql.connector.Error as err:
            logger.error(f"Database error while fetching stock value for {request.email}: {err}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return watch_pb2.StockResponse(value=0.0)

    def CalculateAverageStockValue(self, request, context):
        try:
            logger.info(f"Received CalculateAverageStockValue request for email: {request.email}, count: {request.count}")
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT AVG(value) 
                FROM (
                    SELECT value 
                    FROM stock_data 
                    WHERE email = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                ) as recent_values
                """,
                (request.email, request.count)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result[0] is not None:
                logger.info(f"Calculated average stock value for {request.email}: {result[0]}")
                return watch_pb2.StockResponse(value=float(result[0]))
            else:
                logger.warning(f"No stock data found for email: {request.email}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No stock data found for this user")
                return watch_pb2.StockResponse(value=0.0)
            
        except mysql.connector.Error as err:
            logger.error(f"Database error while calculating average stock value for {request.email}: {err}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return watch_pb2.StockResponse(value=0.0)

    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    watch_pb2_grpc.add_WatchServiceServicer_to_server(WatchService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logger.info(f"gRPC Server started at {datetime.now()}")
    logger.info("Listening on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
