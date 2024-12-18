#
#  user.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

import os
import grpc
import redis
import mysql.connector
import user_pb2_grpc
from concurrent import futures
from services.user_service import UserService
from utils.logger import logger
#-----------------------------------------------------------------------------------------

def serve():
    try:
        global redis_server
        redis_port = int(os.environ['REDIS_PORT'])
        redis_server = redis.Redis(host='user_redis', port=redis_port, decode_responses=True)
        logger.info(redis_server.ping())

        user_server_port = str(int(os.environ['USER_SERVER_PORT']))
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(redis_server), server)
        server.add_insecure_port('[::]:' + user_server_port)
        server.start()
        logger.info("Server started")
        logger.info("Il server gRPC è avviato con successo alla porta " + user_server_port)
        server.wait_for_termination()
    except Exception as e:
        logger.error(f"Errore durante l'avvio del server: {e}")

if __name__ == '__main__':
    serve()
