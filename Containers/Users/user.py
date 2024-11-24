import grpc
from concurrent import futures
import mysql.connector
import os
from datetime import datetime

import user_pb2
import user_pb2_grpc


import logging
from logging.handlers import RotatingFileHandler



log_file = "./logs/app.log"

file_handler = RotatingFileHandler(
    log_file, maxBytes=5*1024*1024, backupCount=5 
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "dsbd_homework1"),
    "port": int(os.getenv("DB_PORT", 3306))
}

class UserService(user_pb2_grpc.UserServiceServicer):
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

    def RegisterUser(self, request, context):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO users (email, ticker) VALUES (%s, %s)",
                (request.email, request.ticker)
            )
            conn.commit()
            
            logger.info(f"New user registered: {request.email} for ticker {request.ticker}")
            self.print_db_stats()  
            
            cursor.close()
            conn.close()
            
            return user_pb2.UserResponse(message=f"User {request.email} registered successfully")
            
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return user_pb2.UserResponse(message=f"Error: {err}")

    def UpdateUser(self, request, context):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET ticker = %s WHERE email = %s",
                (request.new_ticker, request.email)
            )
            conn.commit()
            
            if cursor.rowcount > 0:
                message = f"User {request.email} updated successfully"
                self.print_db_stats() 
            else:
                message = f"No user found with email {request.email}"
            
            cursor.close()
            conn.close()
            
            return user_pb2.UserResponse(message=message)
            
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return user_pb2.UserResponse(message=f"Error: {err}")

    def DeleteUser(self, request, context):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            logger.info("Delete users")
            cursor.execute(
                "DELETE FROM users WHERE email = %s",
                (request.email,)
            )
            conn.commit()
            
            if cursor.rowcount > 0:
                message = f"User {request.email} deleted successfully"
                self.print_db_stats() 
            else:
                message = f"No user found with email {request.email}"
            
            cursor.close()
            conn.close()
            
            return user_pb2.UserResponse(message=message)
            
        except mysql.connector.Error as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Database error: {err}")
            return user_pb2.UserResponse(message=f"Error: {err}")


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        logger.info("Server started")
        logger.info("Il server gRPC è avviato con successo.")
        server.wait_for_termination()
    except Exception as e:
        logger.info(f"Errore durante l'avvio del server: {e}")


if __name__ == '__main__':
    serve()