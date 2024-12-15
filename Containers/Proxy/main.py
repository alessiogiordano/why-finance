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
from user_pb2 import UserDataRequest, UserDeletionRequest
from user_pb2_grpc import UserServiceStub
from watch_pb2 import StockRequest, AverageStockRequest
from watch_pb2_grpc import WatchServiceStub

# From: https://grpc.io/docs/guides/retry/
retry_configuration = [
    ('grpc.service_config', '{"retryPolicy": {"maxAttempts": 3, "initialBackoff": "0.1s", "maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE"]}}')
]


#
# Logging
#
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log")
    ]
)
logger = logging.getLogger(__name__)
#-----------------------------------------------------------------------------------------

#
# Flask
#
app = Flask( __name__)
watch_service_host = "watch_server:" + str(int(environ['WATCH_SERVER_PORT']))
user_service_host = "user_server:" + str(int(environ['USER_SERVER_PORT']))

import uuid
def generateMetadata():
    return [ ('request_id', uuid.uuid4().hex) ]

# GET /watch/ticker
# GET /watch/ticker?avg=<num>
@app.route('/watch/<ticker>', methods=['GET'])
def watch_get_ticker(ticker):
    with grpc.insecure_channel(watch_service_host, options=retry_configuration) as channel:
        watch_service = WatchServiceStub(channel)
        average_count = request.args.get("avg")
        if average_count is None:
            try: # Fetch and return last value
                req = StockRequest(ticker=ticker)
                response = watch_service.GetLastStockValue(req, metadata=generateMetadata())
                logger.info("WATCH " + ticker + "=" + str(response.value))
                return make_response(str(response.value), 200) # OK
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
        else:
            try: # Fetch and return average of last n values
                req = AverageStockRequest(ticker=ticker, count=int(average_count))
                response = watch_service.CalculateAverageStockValue(req, metadata=generateMetadata())
                logger.info("WATCH " + ticker + " average(" + average_count + ")=" + str(response.value))
                return make_response(str(response.value), 200) # OK
            except ValueError as e:
                return make_response("Provide the number of samples to average over as the query string", 400) # Bad Request
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
#-----------------------------------------------------------------------------------------

# PUT /users/email
# -- ticker
# PUT /users/<device_id>
# Body: JSON { "ticker": "<ticker>", "device_token": "<device_token>", "low_value": <low_value>, "high_value": <high_value> }
@app.route('/users/<device_id>', methods=['PUT'])
def user_put_user_data(device_id):
    if not request.is_json:
        return make_response('Request body must be in JSON format', 400)  # Bad Request

    data = request.get_json()

    # Validazione dei parametri richiesti
    required_fields = ['ticker', 'device_token', 'low_value', 'high_value']
    for field in required_fields:
        if field not in data:
            return make_response(f"Missing required field: {field}", 400)  # Bad Request

    # Estrarre i valori dal JSON
    ticker = data['ticker']
    device_token = data['device_token']
    low_value = data['low_value']
    high_value = data['high_value']

    # Controlli sulla lunghezza del ticker
    if len(ticker) > 16:
        # Twice the length of NASDAQ's maximum ticker symbol length (8)
        # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
        return make_response('Tickers longer than 16 characters are not supported', 413)  # Content Too Large

    # Creare la richiesta gRPC
    with grpc.insecure_channel(user_service_host, options=retry_configuration) as channel:
        user_service = UserServiceStub(channel)
        req = UserDataRequest(
            device_id=device_id,
            ticker=ticker,
            device_token=device_token,
            low_value=low_value,
            high_value=high_value
        )
        try:
            # Add new record
            response = user_service.RegisterUser(req, metadata=generateMetadata())
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                try:
                    # Update existing record 
                    response = user_service.UpdateUser(req, metadata=generateMetadata())
                except grpc.RpcError as update_error:
                    return make_response(f"Update failed: {update_error.details()}", 500)  # Internal Server Error
            else:
                return make_response(f"Registration failed: {e.details()}", 500)  # Internal Server Error

    logger.info(f"PUT {device_id} for {ticker}")
    return make_response('', 204)  # Success
#-----------------------------------------------------------------------------------------

# DELETE /users/email
@app.route('/users/<device_id>', methods=['DELETE'])
def user_delete_user_data(device_id):
    with grpc.insecure_channel(user_service_host, options=retry_configuration) as channel:
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