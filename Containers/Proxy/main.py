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
from utils.monitor import monitor

#
# 'At-Most-Once' gRPC Services
#

stocks_service_host = "stocks:" + str(int(environ['STOCKS_PORT']))
users_service_host = "users:" + str(int(environ['USERS_PORT']))

# From: https://grpc.io/docs/guides/retry/
retry_configuration = [
    ('grpc.service_config', '{"retryPolicy": {"maxAttempts": 3, "initialBackoff": "0.1s", "maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE"]}}')
]

import uuid
def generateMetadata():
    return [ ('request_id', uuid.uuid4().hex) ]
#-----------------------------------------------------------------------------------------

#
# Prometheus Monitoring
#

monitoring = monitor.context({
    "counter": "proxy_request_count",
    "gauge": "proxy_request_duration"
}, {
    "counter": "The number of served requests",
    "gauge": "The duration in seconds of a request to the proxy"
}, "method", "path", "status", manual=True)

#
# Flask
#
app = Flask( __name__)

# GET /stocks/ticker
# GET /stocks/ticker?avg=<num>
@app.route('/stocks/<ticker>', methods=['GET'])
def stocks_get_ticker(ticker):
    with monitoring:
        with grpc.insecure_channel(stocks_service_host, options=retry_configuration) as channel:
            stocks_service = StockServiceStub(channel)
            average_count = request.args.get("avg")
            if average_count is None:
                try: # Fetch and return last value
                    req = StockRequest(ticker=ticker)
                    response = stocks_service.GetLastStockValue(req, metadata=generateMetadata())
                    logger.info("STOCK " + ticker + "=" + str(response.value))
                    monitoring.report(method='GET', path='/stocks/<ticker>', status='200')
                    return make_response(str(response.value), 200) # OK
                except Exception as e:
                    monitoring.report(method='GET', path='/stocks/<ticker>', status='500')
                    return make_response(str(e), 500) # Internal Server Error
            else:
                try: # Fetch and return average of last n values
                    req = AverageStockRequest(ticker=ticker, count=int(average_count))
                    response = stocks_service.CalculateAverageStockValue(req, metadata=generateMetadata())
                    logger.info("STOCK " + ticker + " average(" + average_count + ")=" + str(response.value))
                    monitoring.report(method='GET', path='/stocks/<ticker>?avg=<num>', status='200')
                    return make_response(str(response.value), 200) # OK
                except ValueError as e:
                    # Bad Request
                    monitoring.report(method='GET', path='/stocks/<ticker>?avg=<num>', status='400')
                    return make_response("Provide the number of samples to average over as the query string", 400)
                except Exception as e:
                    monitoring.report(method='GET', path='/stocks/<ticker>?avg=<num>', status='500')
                    return make_response(str(e), 500) # Internal Server Error
#-----------------------------------------------------------------------------------------

# PUT /users/device_id
# -- ticker
# -- { "ticker": _, "device_token": _, "low_value": _, "high_value": _ }
@app.route('/users/<device_id>', methods=['PUT'])
def user_put_user_data(device_id):
    with monitoring:
        content_length = request.content_length
        content_type = request.headers['content-type']
        if content_length is None:
            # Bad Request
            monitoring.report(method='PUT', path='/users/<device_id>', status='400')
            return make_response('Provide a ticker or a user object as the body of the request', 400) 
        #---------------------------------------------------------------------------------
        
        if content_type == "application/json":
            data = request.get_json()
            if 'ticker' not in data:
                # Bad Request
                monitoring.report(method='PUT', path='/users/<device_id>', status='400')
                return make_response('The user object must contain the ticker at least', 400)
            #
            ticker = str(data['ticker'])
            device_token = str(data['device_token']) if ('device_token' in data) else ""
            high_value = float(data['high_value']) if ('high_value' in data) else 0.0
            low_value = float(data['low_value']) if ('low_value' in data) else 0.0
            #
            if len(ticker) > 16:
                # Twice the length of NASDAQ's maximum ticker symbol length (8)
                # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
                # Content Too Large
                monitoring.report(method='PUT', path='/users/<device_id>', status='413')
                return make_response('Tickers longer than 16 characters are not supported', 413)
            elif len(ticker) == 0:
                # Bad Request
                monitoring.report(method='PUT', path='/users/<device_id>', status='400')
                return make_response('The user object cannot contain an empty ticker', 400)
        elif content_type == "text/plain":
            if content_length > 16:
                # Twice the length of NASDAQ's maximum ticker symbol length (8)
                # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
                # Content Too Large
                monitoring.report(method='PUT', path='/users/<device_id>', status='413')
                return make_response('Tickers longer than 16 characters are not supported', 413)
            else:
                ticker = request.get_data(as_text=True)
                device_token = ""
                high_value = 0.0
                low_value = 0.0
        else:
            # Unsupported Content-Type
            monitoring.report(method='PUT', path='/users/<device_id>', status='415')
            return make_response('Unsupported Content-Type: only "text/plain" or "application/json" are accepted', 415)
        #---------------------------------------------------------------------------------
        
        if high_value > 0.0 and low_value > high_value:
            # Bad Request
            monitoring.report(method='PUT', path='/users/<device_id>', status='400')
            return make_response('high_value must be higher than low_value', 400)
        #---------------------------------------------------------------------------------
        
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
                    monitoring.report(method='PUT', path='/users/<device_id>', status='500')
                    return make_response(str(e), 500) # Internal Server Error
            logger.info("PUT " + device_id + " for " + ticker)
            monitoring.report(method='PUT', path='/users/<device_id>', status='204')
            return make_response('', 204) # No Content
#-----------------------------------------------------------------------------------------

# DELETE /users/device_id
@app.route('/users/<device_id>', methods=['DELETE'])
def user_delete_user_data(device_id):
    with monitoring:
        with grpc.insecure_channel(users_service_host, options=retry_configuration) as channel:
            user_service = UserServiceStub(channel)
            req = UserDeletionRequest(device_id=device_id)
            try: # Remove existing record
                response = user_service.DeleteUser(req, metadata=generateMetadata())
                logger.info("DELETE " + device_id)
                monitoring.report(method='DELETE', path='/users/<device_id>', status='204')
                return make_response('', 204) # No Content
            except Exception as e:
                monitoring.report(method='DELETE', path='/users/<device_id>', status='500')
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
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=int(environ['PROXY_PORT']))