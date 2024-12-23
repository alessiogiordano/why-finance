#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

import os
import redis

import grpc
import users_pb2_grpc
from concurrent import futures
from datetime import datetime

from utils.logger import logger
from service import UserService

if __name__ == '__main__':
    global redis_server
    redis_port = int(os.environ['REDIS_PORT'])
    redis_server = redis.Redis(host='users_redis', port=redis_port, decode_responses=True)
    logger.info(redis_server.ping())
    #
    users_server_port = str(int(os.environ['USERS_PORT']))
    #
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(UserService(redis_server), server)
    server.add_insecure_port('[::]:' + users_server_port)
    server.start()
    logger.info(f"gRPC Server started at {datetime.now()}")
    logger.info("Listening on port " + users_server_port)
    server.wait_for_termination()
#-----------------------------------------------------------------------------------------