#
#  watch.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#
import os
import redis
import grpc
import watch_pb2_grpc

from services.watch_service import WatchService
from concurrent import futures
from datetime import datetime


from utils.logger import logger
#-----------------------------------------------------------------------------------------
#
# gRPC Server
#
    
def serve():
    #
    global redis_server
    redis_port = int(os.environ['REDIS_PORT'])
    redis_server = redis.Redis(host='user_redis', port=redis_port, decode_responses=True)
    logger.info(redis_server.ping())
    #
    watch_server_port = str(int(os.environ['WATCH_SERVER_PORT']))
    #
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    watch_pb2_grpc.add_WatchServiceServicer_to_server(WatchService(redis_server), server)
    server.add_insecure_port('[::]:' + watch_server_port)
    server.start()
    logger.info(f"gRPC Server started at {datetime.now()}")
    logger.info("Listening on port " + watch_server_port)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
