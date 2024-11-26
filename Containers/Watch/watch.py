#
#  watch.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

import redis
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
    "host": os.environ.get('DB_HOST', 'mysql'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', 'root'),
    "database": os.environ.get('DB_NAME', 'dsbd_homework1'),
    "port": int(os.environ.get('DB_PORT', '3306'))
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
            logger.info("Il server gRPC è avviato con successo.")
            logger.info("\n" + "="*50)
            logger.info("Database Statistics:")
            logger.info(f"Total Users: {user_count}")
            logger.info(f"Total Stock Data Records: {stock_data_count}")
            if last_stock:
                logger.info(f"Last Stock Update: {last_stock[0]} - Value: {last_stock[1]} at {last_stock[2]}")
            logger.info("="*50 + "\n")
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            logger.info(f"Error accessing database: {err}")

    def GetLastStockValue(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = watch_pb2.StockResponse()
                serialized_response = redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        #
        try:
            logger.info(f"Received GetLastStockValue request for ticker: {request.ticker}")
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute(
                """
                SELECT value 
                FROM stock_data 
                WHERE ticker = %s 
                ORDER BY timestamp DESC 
                LIMIT 1
                """,
                (request.ticker,)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                logger.info(f"Stock value retrieved for {request.ticker}: {result[0]}")
                response = watch_pb2.StockResponse(value=result[0])
                if request_id is not None:
                    # Store in cache
                    redis_server.set(request_id, response.SerializeToString())
                return response
            else:
                logger.warning(f"No stock data found for ticker: {request.ticker}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No stock data found for this user")
                return watch_pb2.StockResponse(value=0.0)
            
        except mysql.connector.Error as err:
            logger.error(f"Database error while fetching stock value for {request.ticker}: {err}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return watch_pb2.StockResponse(value=0.0)

    def CalculateAverageStockValue(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = watch_pb2.StockResponse()
                serialized_response = redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        #
        try:
            logger.info(f"Received CalculateAverageStockValue request for ticker: {request.ticker}, count: {request.count}")
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
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
                (request.ticker, request.count)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result[0] is not None:
                logger.info(f"Calculated average stock value for {request.ticker}: {result[0]}")
                response = watch_pb2.StockResponse(value=float(result[0]))
                if request_id is not None:
                    # Store in cache
                    redis_server.set(request_id, response.SerializeToString())
                return response
            else:
                logger.warning(f"No stock data found for ticker: {request.ticker}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No stock data found for this user")
                return watch_pb2.StockResponse(value=0.0)
            
        except mysql.connector.Error as err:
            logger.error(f"Database error while calculating average stock value for {request.ticker}: {err}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return watch_pb2.StockResponse(value=0.0)

    
def serve():
    #
    global redis_server
    redis_port = int(os.environ['REDIS_PORT'])
    redis_server = redis.Redis(host='user_redis', port=redis_port, decode_responses=True)
    print(redis_server.ping())
    #
    watch_server_port = str(int(os.environ['WATCH_SERVER_PORT']))
    #
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    watch_pb2_grpc.add_WatchServiceServicer_to_server(WatchService(), server)
    server.add_insecure_port('[::]:' + watch_server_port)
    server.start()
    logger.info(f"gRPC Server started at {datetime.now()}")
    logger.info("Listening on port " + watch_server_port)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
