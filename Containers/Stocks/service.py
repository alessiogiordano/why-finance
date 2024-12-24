#
#  service.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 18/12/24.
#

import stocks_pb2
import stocks_pb2_grpc
import grpc
from handlers.stocks import queries as QueryHandler
from utils.logger import logger

class StockService(stocks_pb2_grpc.StockServiceServicer):
    def __init__(self, redis_server = None):
        self.redis_server = redis_server
        self.query_handler = QueryHandler()
    #-------------------------------------------------------------------------------------
    def GetLastStockValue(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = stocks_pb2.StockResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        ###
        try:
            logger.info(f"Received GetLastStockValue request for ticker: {request.ticker}")
            result = self.query_handler.get_last_stock_value(request.ticker)
            if result is not None:
                response = stocks_pb2.StockResponse(value=result)
                if request_id is not None:
                    # Store in cache
                    self.redis_server.set(request_id, response.SerializeToString())
                return response
            else:
                logger.warning(f"No stock data found for ticker: {request.ticker}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No stock data found for ticker: {request.ticker}")
                return stocks_pb2.StockResponse(value=0.0)
        ###
        except Exception as err:
            logger.error(f"Error while fetching stock value for {request.ticker}: {err}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(err))
            return stocks_pb2.StockResponse(value=0.0)
    #-------------------------------------------------------------------------------------
    def CalculateAverageStockValue(self, request, context):
        metadata = dict(context.invocation_metadata())
        request_id = metadata.get('request_id', None)
        if request_id is not None:
            # Check request in cache
            try:
                # Return cached message (at-most-once)
                response = stocks_pb2.StockResponse()
                serialized_response = self.redis_server.get(request_id)
                response.ParseFromString(serialized_response)
                logger.info(f"Cached Request: {request_id}")
                return response
            except:
                pass
        ###
        try:
            logger.info(f"Received CalculateAverageStockValue request for ticker: {request.ticker}, count: {request.count}")
            result = self.query_handler.get_last_stock_value(request.ticker)
            if result is not None:
                logger.info(f"Calculated average stock value for {request.ticker}: {result}")
                response = stocks_pb2.StockResponse(value=float(result))
                if request_id is not None:
                    # Store in cache
                    self.redis_server.set(request_id, response.SerializeToString())
                return response
            else:
                logger.warning(f"No stock data found for ticker: {request.ticker}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No stock data found for ticker: {request.ticker}")
                return stocks_pb2.StockResponse(value=0.0)
        ###
        except Exception as err:
            logger.error(f"Error while calculating average stock value for {request.ticker}: {err}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(err))
            return stocks_pb2.StockResponse(value=0.0)
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------