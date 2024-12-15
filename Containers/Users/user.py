#
#  user.py
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

import user_pb2
import user_pb2_grpc

#
# Logging
#
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log")
    ]
)
logger = logging.getLogger(__name__)
#-----------------------------------------------------------------------------------------

#
# gRPC Server
#

USER_DB_CONFIG = {
    "host": os.environ.get('USER_DB_HOST', 'mysql_user'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', 'root'),
    "database": os.environ.get('USER_DB_NAME', 'user_db'),
    "port": int(os.environ.get('USER_DB_PORT', '3306'))
}

TICKER_DB_CONFIG = {
    "host": os.environ.get('TICKER_DB_HOST', 'mysql_ticker'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', 'root'),
    "database": os.environ.get('TICKER_DB_NAME', 'ticker_db'),
    "port": int(os.environ.get('TICKER_DB_PORT', '3306'))
}

def connect_to_db(config):
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Errore di connessione al database {config['database']}: {err}")
        raise

class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.print_user_db_stats()
        self.print_ticker_db_stats()

    def print_user_db_stats(self):
        try:
            conn = connect_to_db(USER_DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            logger.info(f"Database User - Total Users: {user_count}")
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            logger.error(f"Error accessing user database: {err}")

    def print_ticker_db_stats(self):
        try:
            conn = connect_to_db(TICKER_DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tickers")
            ticker_count = cursor.fetchone()[0]
            logger.info(f"Database Ticker - Total Tickers: {ticker_count}")
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            logger.error(f"Error accessing ticker database: {err}")

    def RegisterUser(self, request, context):
        try:
            conn = connect_to_db(USER_DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE device_id = %s", (request.device_id,))
            user_exists = cursor.fetchone()[0] > 0
            if user_exists:
                #Update existing user
                return self.UpdateUser(request, context)

            # Register new user
            cursor.execute(
                "INSERT INTO users (device_id, ticker, device_token, low_value, high_value) VALUES (%s, %s, %s, %s, %s)",
                (request.device_id, request.ticker, request.device_token, request.low_value, request.high_value)
            )
            conn.commit()
            logger.info(f"New user registered: {request.device_id} for ticker {request.ticker}")
            self.print_user_db_stats()
            cursor.close()
            conn.close()
            return user_pb2.UserResponse(message=f"User {request.device_id} registered successfully")
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return user_pb2.UserResponse(message=f"Error: {err}")

    def UpdateUser(self, request, context):
        try:
            conn = connect_to_db(USER_DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET ticker = %s, device_token = %s, low_value = %s, high_value = %s WHERE device_id = %s",
                (request.ticker, request.device_token, request.low_value, request.high_value, request.device_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                message = f"User {request.device_id} updated successfully"
                self.print_user_db_stats()
            else:
                message = f"No user found with device_id {request.device_id}"
            cursor.close()
            conn.close()
            return user_pb2.UserResponse(message=message)
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return user_pb2.UserResponse(message=f"Error: {err}")

    def DeleteUser(self, request, context):
        try:
            conn = connect_to_db(USER_DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM users WHERE device_id = %s",
                (request.device_id,)
            )
            conn.commit()
            if cursor.rowcount > 0:
                message = f"User {request.device_id} deleted successfully"
                self.print_user_db_stats()
            else:
                message = f"No user found with device_id {request.device_id}"
            cursor.close()
            conn.close()
            return user_pb2.UserResponse(message=message)
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return user_pb2.UserResponse(message=f"Error: {err}")

def serve():
    try:
        global redis_server
        redis_port = int(os.environ['REDIS_PORT'])
        redis_server = redis.Redis(host='user_redis', port=redis_port, decode_responses=True)
        logger.info(redis_server.ping())

        user_server_port = str(int(os.environ['USER_SERVER_PORT']))
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
        server.add_insecure_port('[::]:' + user_server_port)
        server.start()
        logger.info("Server started")
        logger.info("Il server gRPC è avviato con successo alla porta " + user_server_port)
        server.wait_for_termination()
    except Exception as e:
        logger.error(f"Errore durante l'avvio del server: {e}")

if __name__ == '__main__':
    serve()
