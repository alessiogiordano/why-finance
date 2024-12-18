from utils.logger import logger
from services.query_handler import QueryHandler
from services.command_handler import CommandHandler
from database.connection import USER_DB_CONFIG

import grpc
import user_pb2
import user_pb2_grpc
#
# gRPC Server
#



class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, redis_server):
        self.query_handler = QueryHandler(USER_DB_CONFIG)
        self.command_handler = CommandHandler(USER_DB_CONFIG)
        self.redis_server = redis_server
        
    def RegisterUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        
        if request_id is not None:
            try:
                # Return cached message (at-most-once)
                response = user_pb2.UserResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        #
        try:
            user_exists = self.query_handler.user_exists(request.device_id)
            if user_exists:
                return self.UpdateUser(request, context)

            self.command_handler.register_user(
                request.device_id,
                request.ticker,
                request.device_token,
                request.low_value,
                request.high_value,
            )
            
            response = user_pb2.UserResponse(message=f"User {request.device_id} registered successfully")
            if request_id is not None:
                # Store in cache
                self.redis_server.set(request_id, response.SerializeToString())
            return response
        
        except Exception as e:
            logger.error(f"Errore durante la registrazione: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse(message=f"Errore: {e}")

    def UpdateUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = user_pb2.UserResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        #
        try:
            success = self.command_handler.update_user(
                request.device_id,
                request.ticker,
                request.device_token,
                request.low_value,
                request.high_value,
            )
            if success:
                response = user_pb2.UserResponse(message=f"User {request.device_id} updated successfully")
            else:
                response = user_pb2.UserResponse(message=f"No user found with device_id {request.device_id}")
            if request_id is not None:
                # Store in cache
                self.redis_server.set(request_id, response.SerializeToString())
            return response
        
        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse(message=f"Errore: {e}")

    def DeleteUser(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = user_pb2.UserResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        #
        try:
            success = self.command_handler.delete_user(request.device_id)
            if success:
                response = user_pb2.UserResponse(message=f"User {request.device_id} deleted successfully")
            else:
                response = user_pb2.UserResponse(message=f"No user found with device_id {request.device_id}")
            
            if request_id is not None:
                # Store in cache
                self.redis_server.set(request_id, response.SerializeToString())
            return response
        
        except Exception as e:
            logger.error(f"Errore durante l'eliminazione: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse(message=f"Errore: {e}")
