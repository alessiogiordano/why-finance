#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 21/11/24.
#

from os import environ # Environment Variables
from urllib.parse import urlparse # Get host component from URL
from time import time # Get timestamp for half-opening the circuit
import redis
import grpc

from http_pb2 import HTTPMethod, HTTPStatusCode, HTTPRequest, HTTPResponse
from circuit_breaker_pb2 import CircuitBreakerStatus
from circuit_breaker_pb2 import CircuitBreakerRequest, CircuitBreakerResponse
from circuit_breaker_pb2_grpc import CircuitBreakerServicer
from circuit_breaker_pb2_grpc import add_CircuitBreakerServicer_to_server

import concurrent.futures
import requests

# Avoid key collisions in Redis database
cache_prefix = "cb_cache_"
state_prefix = "cb_state_"

#
# Send HTTP Requests from/to protobuf representation through "requests"
#
def send_http_request(request, timeout=30):
    method = 'GET'
    if request.method is HTTPMethod.HTTP_HEAD:
        method = 'HEAD'
    elif request.method is HTTPMethod.HTTP_POST:
        method = 'POST'
    elif request.method is HTTPMethod.HTTP_PUT:
        method = 'PUT'
    elif request.method is HTTPMethod.HTTP_DELETE:
        method = 'DELETE'
    elif request.method is HTTPMethod.HTTP_CONNECT:
        method = 'CONNECT'
    elif request.method is HTTPMethod.HTTP_OPTIONS:
        method = 'OPTIONS'
    elif request.method is HTTPMethod.HTTP_TRACE:
        method = 'TRACE'
    elif request.method is HTTPMethod.HTTP_PATCH:
        method = 'PATCH'
    #
    print(method + " " + request.url)
    response = requests.request(method, request.url, headers=request.headers, data=request.body, timeout=timeout)
    print("Response: " + str(response.status_code))
    #
    status = HTTPStatusCode.HTTP_UNKNOWN
    try:
        status = HTTPStatusCode.Value(HTTPStatusCode.Name(response.status_code))
    except:
        pass
    #
    return HTTPResponse(status=status, headers=response.headers, body=response.text)

#
# gRPC server implementation
#
class CircuitBreaker(CircuitBreakerServicer):
    def send(self, request, context):
        # Check state of the circuit
        host = urlparse(request.request.url).netloc
        host_state = redis_server.get(state_prefix + host)
        #
        status = CircuitBreakerStatus.CircuitBreaker_CLOSED
        failures = 0
        wait = 0
        #
        # 'host_state' is an integer that represents the number of consecutive
        # failures if less than the threshold, or the timestamp in the future when
        # the circuit will half-close (only 1 successful request will then close it)
        if host_state is not None:
            try:
                failures = int(host_state)
                # Check if circuit is not closed
                now = int(time())
                if failures > request.threshold:
                    # 'failures' here represents the timestamp before which the circuit is opened
                    if failures > now:
                        # Open Circuit
                        status = CircuitBreakerStatus.CircuitBreaker_OPEN
                        wait = now - failures
                    else:
                        # Half-Open Circuit
                        status = CircuitBreakerStatus.CircuitBreaker_HALF_OPEN
                # else Closed Circuit
            except:
                # Corrupted state, assume closed circuit
                pass
        if status is CircuitBreakerStatus.CircuitBreaker_OPEN:
            return CircuitBreakerResponse(id=request.id, status=status, wait=wait, http=HTTPResponse())
        # Request can occur
        try:
            # Return cached message (at-most-once)
            circuit_breaker_response = CircuitBreakerResponse()
            serialized_response = redis_server.get(cache_prefix + request.id)
            circuit_breaker_response.ParseFromString(serialized_response)
            print("Cached Request " + request.id)
            return circuit_breaker_response
        except:
            # Send HTTP request
            print("Request " + request.id)
            http_response = send_http_request(request.http, request.timeout)
            # Request is successful as far as the circuit breaker is concerned if no HTTP status code is provided in the 'expected' list of the request object (and no state is ever set in Redis)
            if len(request.expected) > 0:
                if http_response.status not in request.expected:
                    # Circuit breaker transition logic
                    if status is CircuitBreakerStatus.CircuitBreaker_HALF_OPEN:
                        # Re-open the circuit
                        redis_server.set(state_prefix + host, int(time()) + request.recovery)
                    else:
                        failures += 1
                        print("Failure of " + request.id + " [count=" + str(failures) + "]")
                        if failures > request.threshold:
                            # Open the circuit
                            redis_server.set(state_prefix + host, int(time()) + request.recovery)
                        else:
                            # Keep the circuit closed, but increase the consecutive failure count
                            redis_server.set(state_prefix + host, failures)
                else:
                    # Successful request, reset the circuit breaker
                    # Covers both transition from half_open and closed consecutive count reset
                    redis_server.set(state_prefix + host, 0)
            # Make response object
            circuit_breaker_response = CircuitBreakerResponse(id=request.id, status=status, wait=0, http=http_response)
            # Cache response
            redis_server.set(cache_prefix + request.id, circuit_breaker_response.SerializeToString())
            # Done
            return circuit_breaker_response

#
# Main
#
if __name__ == '__main__':
    redis_port = int(environ['REDIS_PORT'])
    circuit_breaker_port = str(int(environ['CIRCUIT_BREAKER_PORT']))
    #
    global redis_server
    redis_server = redis.Redis(host='localhost', port=redis_port, decode_responses=True)
    #
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    add_CircuitBreakerServicer_to_server(CircuitBreaker(), server)
    server.add_insecure_port('[::]:' + circuit_breaker_port)
    server.start()
    print("Circuit Breaker microservice is ready")
    server.wait_for_termination()