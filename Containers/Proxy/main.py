#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

from os import environ # Environment Variables
from flask import Flask, make_response, abort, request, jsonify

import grpc
from user_pb2 import UserDataRequest, UserDeletionRequest
from user_pb2_grpc import UserServiceStub
from watch_pb2 import StockRequest, AverageStockRequest
from watch_pb2_grpc import WatchServiceStub

app = Flask( __name__)

watch_service_host = "watch_server:" + str(int(environ['WATCH_SERVER_PORT']))
user_service_host = "user_server:" + str(int(environ['USER_SERVER_PORT']))

# GET /watch/ticker
# GET /watch/ticker?avg=<num>
@app.route('/watch/<ticker>', methods=['GET'])
def watch_get_ticker(ticker):
    with grpc.insecure_channel(watch_service_host) as channel:
        watch_service = WatchServiceStub(channel)
        average_count = request.args.get("avg")
        if average_count is None:
            try: # Fetch and return last value
                req = StockRequest(ticker=ticker)
                response = watch_service.GetLastStockValue(req)
                print("WATCH " + ticker + "=" + str(response.value))
                return make_response(str(response.value), 200) # OK
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
        else:
            try: # Fetch and return average of last n values
                req = AverageStockRequest(ticker=ticker, count=int(average_count))
                response = watch_service.CalculateAverageStockValue(req)
                print("WATCH " + ticker + " average(" + average_count + ")=" + str(response.value))
                return make_response(str(response.value), 200) # OK
            except ValueError as e:
                return make_response("Provide the number of samples to average over as the query string", 400) # Bad Request
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
#-----------------------------------------------------------------------------------------

# PUT /users/email
# -- ticker
@app.route('/users/<email>', methods=['PUT'])
def user_put_user_data(email):
    content_length = request.content_length
    if content_length is None:
        return make_response('Provide a ticker as the body of the request', 400) # Bad Request
    if content_length > 16:
        # Twice the length of NASDAQ's maximum ticker symbol length (8)
        # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
        abort(413) # Content Too Large
    with grpc.insecure_channel(user_service_host) as channel:
        user_service = UserServiceStub(channel)
        ticker = request.get_data(as_text=True)
        req = UserDataRequest(email=email, ticker=ticker)
        try: # Add new record
            response = user_service.RegisterUser(req)
        except:
            try: # Update existing record
                response = user_service.UpdateUser(req)
            except Exception as e:
                return make_response(str(e), 500) # Internal Server Error
        print("PUT " + email + " for " + ticker)
        return make_response('', 204) # No Content
#-----------------------------------------------------------------------------------------

# DELETE /users/email
@app.route('/users/<email>', methods=['DELETE'])
def user_delete_user_data(email):
    with grpc.insecure_channel(user_service_host) as channel:
        user_service = UserServiceStub(channel)
        req = UserDeletionRequest(email=email)
        try: # Remove existing record
            response = user_service.DeleteUser(req)
            print("DELETE " + email)
            return make_response('', 204) # No Content
        except Exception as e:
            return make_response(str(e), 500) # Internal Server Error
#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=int(environ['PROXY_PORT']))