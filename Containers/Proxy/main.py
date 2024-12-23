#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

from os import environ # Environment Variables
from flask import Flask, make_response, request

import grpc
from users_pb2 import UserDataRequest, UserDeletionRequest
from users_pb2_grpc import UserServiceStub
from stocks_pb2 import StockRequest, AverageStockRequest
from stocks_pb2_grpc import StockServiceStub

from utils.logger import logger

#
# Flask
#
app = Flask( __name__)
stocks_service_host = "stocks:" + str(int(environ['STOCKS_PORT']))
users_service_host = "users:" + str(int(environ['USERS_PORT']))

# From: https://grpc.io/docs/guides/retry/
retry_configuration = [
    ('grpc.service_config', '{"retryPolicy": {"maxAttempts": 3, "initialBackoff": "0.1s", "maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE"]}}')
]

import uuid
def generateMetadata():
    return [ ('request_id', uuid.uuid4().hex) ]

# GET /stocks/ticker
# GET /stocks/ticker?avg=<num>
@app.route('/stocks/<ticker>', methods=['GET'])
def stocks_get_ticker(ticker):
    with grpc.insecure_channel(stocks_service_host, options=retry_configuration) as channel:
        stocks_service = StockServiceStub(channel)
        average_count = request.args.get("avg")
        if average_count is None:
            try: # Fetch and return last value
                req = StockRequest(ticker=ticker)
                response = stocks_service.GetLastStockValue(req, metadata=generateMetadata())
                logger.info("STOCK " + ticker + "=" + str(response.value))
                return make_response(str(response.value), 200) # OK
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
        else:
            try: # Fetch and return average of last n values
                req = AverageStockRequest(ticker=ticker, count=int(average_count))
                response = stocks_service.CalculateAverageStockValue(req, metadata=generateMetadata())
                logger.info("STOCK " + ticker + " average(" + average_count + ")=" + str(response.value))
                return make_response(str(response.value), 200) # OK
            except ValueError as e:
                return make_response("Provide the number of samples to average over as the query string", 400) # Bad Request
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
#-----------------------------------------------------------------------------------------

# PUT /users/device_id
# -- ticker
# -- { "ticker": _, "device_token": _, "low_value": _, "high_value": _ }
@app.route('/users/<device_id>', methods=['PUT'])
def user_put_user_data(device_id):
    content_length = request.content_length
    content_type = request.headers['content-type']
    if content_length is None:
        return make_response('Provide a ticker or a user object as the body of the request', 400) # Bad Request
    #-------------------------------------------------------------------------------------
    
    if content_type == "application/json":
        data = request.get_json()
        if 'ticker' not in data:
            return make_response('The user object must contain the ticker at least', 400) # Bad Request
        #
        ticker = str(data['ticker'])
        device_token = str(data['device_token']) if ('device_token' in data) else ""
        high_value = float(data['high_value']) if ('high_value' in data) else 0.0
        low_value = float(data['low_value']) if ('low_value' in data) else 0.0
        #
        if len(ticker) > 16:
            # Twice the length of NASDAQ's maximum ticker symbol length (8)
            # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
            return make_response('Tickers longer than 16 characters are not supported', 413) # Content Too Large
        elif len(ticker) == 0:
            return make_response('The user object cannot contain an empty ticker', 400) # Bad Request
    elif content_type == "text/plain":
        if content_length > 16:
            # Twice the length of NASDAQ's maximum ticker symbol length (8)
            # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
            return make_response('Tickers longer than 16 characters are not supported', 413) # Content Too Large
        else:
            ticker = request.get_data(as_text=True)
            device_token = ""
            high_value = 0.0
            low_value = 0.0
    else:
        return make_response('Unsupported Content-Type: only "text/plain" or "application/json" are accepted', 415)
    #-------------------------------------------------------------------------------------
    
    if high_value > 0.0 and low_value > high_value:
        return make_response('high_value must be higher than low_value', 400) # Bad Request
    #-------------------------------------------------------------------------------------
    
    with grpc.insecure_channel(users_service_host, options=retry_configuration) as channel:
        user_service = UserServiceStub(channel)
        req = UserDataRequest(
            device_id=device_id,
            ticker=ticker,
            device_token=device_token,
            low_value=low_value,
            high_value=high_value
        )
        try: # Add new record
            response = user_service.RegisterUser(req, metadata=generateMetadata())
        except:
            try: # Update existing record
                response = user_service.UpdateUser(req, metadata=generateMetadata())
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
        logger.info("PUT " + device_id + " for " + ticker)
        return make_response('', 204) # No Content
#-----------------------------------------------------------------------------------------

# DELETE /users/device_id
@app.route('/users/<device_id>', methods=['DELETE'])
def user_delete_user_data(device_id):
    with grpc.insecure_channel(users_service_host, options=retry_configuration) as channel:
        user_service = UserServiceStub(channel)
        req = UserDeletionRequest(device_id=device_id)
        try: # Remove existing record
            response = user_service.DeleteUser(req, metadata=generateMetadata())
            logger.info("DELETE " + device_id)
            return make_response('', 204) # No Content
        except Exception as e:
            return make_response(str(e), 500) # Internal Server Error
#-----------------------------------------------------------------------------------------

# GET /health
@app.route('/health', methods=['GET'])
def get_proxy_health():
    return make_response('', 204) # No Content
#-----------------------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return make_response(str(e), 404) # Not Found
#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=int(environ['PROXY_PORT']))