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
import stocks_pb2_grpc
from concurrent import futures
from datetime import datetime

from utils.logger import logger

from service import StockService

if __name__ == '__main__':
    redis_port = int(os.environ['REDIS_PORT'])
    redis_server = redis.Redis(host='stocks_redis', port=redis_port, decode_responses=True)
    logger.info(redis_server.ping())
    #
    stocks_port = str(int(os.environ['STOCKS_PORT']))
    #
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stocks_pb2_grpc.add_StockServiceServicer_to_server(StockService(redis_server), server)
    server.add_insecure_port('[::]:' + stocks_port)
    server.start()
    logger.info(f"gRPC Server started at {datetime.now()}")
    logger.info("Listening on port " + stocks_port)
    server.wait_for_termination()
#-----------------------------------------------------------------------------------------