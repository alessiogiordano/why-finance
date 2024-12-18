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
    def __init__(self):
        self.query_handler = QueryHandler(USER_DB_CONFIG)
        self.command_handler = CommandHandler(USER_DB_CONFIG)

    def RegisterUser(self, request, context):
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
            return user_pb2.UserResponse(message=f"User {request.device_id} registered successfully")
        except Exception as e:
            logger.error(f"Errore durante la registrazione: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse(message=f"Errore: {e}")

    def UpdateUser(self, request, context):
        try:
            success = self.command_handler.update_user(
                request.device_id,
                request.ticker,
                request.device_token,
                request.low_value,
                request.high_value,
            )
            if success:
                return user_pb2.UserResponse(message=f"User {request.device_id} updated successfully")
            else:
                return user_pb2.UserResponse(message=f"No user found with device_id {request.device_id}")
        except Exception as e:
            logger.error(f"Errore durante l'aggiornamento: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse(message=f"Errore: {e}")

    def DeleteUser(self, request, context):
        try:
            success = self.command_handler.delete_user(request.device_id)
            if success:
                return user_pb2.UserResponse(message=f"User {request.device_id} deleted successfully")
            else:
                return user_pb2.UserResponse(message=f"No user found with device_id {request.device_id}")
        except Exception as e:
            logger.error(f"Errore durante l'eliminazione: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.UserResponse(message=f"Errore: {e}")
