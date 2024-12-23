#
#  service.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 18/12/24.
#

from utils.logger import logger
from utils.broadcast import broadcast
from handlers.users import queries as QueryHandler
from handlers.users import commands as CommandHandler

import grpc
import users_pb2
import users_pb2_grpc

class UserService(users_pb2_grpc.UserServiceServicer):
    def __init__(self, redis_server = None):
        self.redis_server = redis_server
        self.query_handler = QueryHandler()
        self.command_handler = CommandHandler()
    #-------------------------------------------------------------------------------------
    def RegisterUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = users_pb2.UserResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        ###
        try:
            self.command_handler.register_user(
                request.device_id,
                request.ticker,
                None if request.device_token == "" else request.device_token,
                None if request.high_value <= 0.0 else request.high_value,
                None if request.low_value <= 0.0 else request.low_value
            )
            logger.info(f"New user registered: {request.device_id} for ticker {request.ticker}")
            broadcast('crawler', request.ticker)
            response = users_pb2.UserResponse(message=f"User {request.device_id} registered successfully")
            if request_id is not None:
                # Store in cache
                self.redis_server.set(request_id, response.SerializeToString())
            return response
        ###
        except Exception as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(err))
            return users_pb2.UserResponse(message=f"Error: {err}")
    #-------------------------------------------------------------------------------------
    def UpdateUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = users_pb2.UserResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        ###
        try:
            #successful =
            self.command_handler.update_user(
                request.device_id,
                request.ticker,
                None if request.device_token == "" else request.device_token,
                None if request.high_value <= 0.0 else request.high_value,
                None if request.low_value <= 0.0 else request.low_value
            )
            #if not successful:
            #    raise Exception(f"No user found with {request.device_id}")
            message = f"User {request.device_id} updated successfully"
            broadcast('crawler', request.ticker)
            response = users_pb2.UserResponse(message=message)
            if request_id is not None:
                # Store in cache
                self.redis_server.set(request_id, response.SerializeToString())
            return response
        ###
        except Exception as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(err))
            return users_pb2.UserResponse(message=f"Error: {err}")
    #-------------------------------------------------------------------------------------
    def DeleteUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = users_pb2.UserResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        ###
        try:
            #successful =
            self.command_handler.delete_user(request.device_id)
            #if not successful:
            #    raise Exception(f"No user found with {request.device_id}")
            message = f"User {request.device_id} deleted successfully"
            response = users_pb2.UserResponse(message=message)
            if request_id is not None:
                # Store in cache
                self.redis_server.set(request_id, response.SerializeToString())
            return response
        ###
        except Exception as err:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(err))
            return users_pb2.UserResponse(message=f"Error: {err}")
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
