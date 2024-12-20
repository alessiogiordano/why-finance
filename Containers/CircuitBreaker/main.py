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
from circuit_breaker_pb2 import CircuitBreakerStatusRequest, CircuitBreakerStatusResponse
from circuit_breaker_pb2 import CircuitBreakerHTTPRequest, CircuitBreakerHTTPResponse
from circuit_breaker_pb2_grpc import CircuitBreakerServicer
from circuit_breaker_pb2_grpc import add_CircuitBreakerServicer_to_server

import concurrent.futures
import requests

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
# Circuit Breaker
#

# Avoid key collisions in Redis database
cache_prefix = "cb_cache_"
state_prefix = "cb_state_"

def get_circuit_state_for_hostname(host, threshold):
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
            if failures > threshold:
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
    return tuple([status, failures, wait])
#-----------------------------------------------------------------------------------------
def change_circuit_state_for_hostname(host, status, failures, threshold, recovery):
    # Circuit breaker transition logic
    if status is CircuitBreakerStatus.CircuitBreaker_HALF_OPEN:
        # Re-open the circuit
        redis_server.set(state_prefix + host, int(time()) + recovery)
        return CircuitBreakerStatus.CircuitBreaker_OPEN
    else:
        failures += 1
        logger.info("Failure of " + host + " [count=" + str(failures) + "]")
        if failures > threshold:
            # Open the circuit
            redis_server.set(state_prefix + host, int(time()) + recovery)
            return CircuitBreakerStatus.CircuitBreaker_OPEN
        else:
            # Keep the circuit closed, but increase the consecutive failure count
            redis_server.set(state_prefix + host, failures)
            return CircuitBreakerStatus.CircuitBreaker_CLOSED
#-----------------------------------------------------------------------------------------
def reset_circuit_state_for_hostname(host):
    # Successful request, reset the circuit breaker
    # Covers both transition from half_open and closed consecutive count reset
    redis_server.set(state_prefix + host, 0)
#-----------------------------------------------------------------------------------------

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
    logger.info(method + " " + request.url)
    response = requests.request(method, request.url, headers=request.headers, data=request.body, timeout=timeout)
    logger.info("Response: " + str(response.status_code))
    #
    status = HTTPStatusCode.HTTP_UNKNOWN
    try:
        status = HTTPStatusCode.Value(HTTPStatusCode.Name(response.status_code))
    except:
        pass
    #
    return HTTPResponse(status=status, headers=response.headers, body=response.text)
#-----------------------------------------------------------------------------------------

#
# gRPC server implementation
#
class CircuitBreaker(CircuitBreakerServicer):
    #################################
    def status(self, request, context):
        assert len(request.host) > 0
        (status, failures, wait) = get_circuit_state_for_hostname(request.host, request.threshold)
        return CircuitBreakerStatusResponse(host=request.host, status=status, wait=wait)
    #-------------------------------------------------------------------------------------
    def success(self, request, context):
        assert len(request.host) > 0
        reset_circuit_state_for_hostname(request.host)
        status = CircuitBreakerStatus.CircuitBreaker_CLOSED
        return CircuitBreakerStatusResponse(host=request.host, status=status, wait=0)
    #-------------------------------------------------------------------------------------
    def failure(self, request, context):
        assert len(request.host) > 0
        (status, failures, wait) = get_circuit_state_for_hostname(request.host, request.threshold)
        status = change_circuit_state_for_hostname(request.host, status, failures, request.threshold, request.recovery)
        return CircuitBreakerStatusResponse(host=request.host, status=status, wait=request.recovery)
    #################################
    def send(self, request, context):
        # Check state of the circuit
        host = urlparse(request.http.url).netloc
        (status, failures, wait) = get_circuit_state_for_hostname(host, request.threshold)
        if status is CircuitBreakerStatus.CircuitBreaker_OPEN:
            return CircuitBreakerHTTPResponse(id=request.id, status=status, wait=wait, http=HTTPResponse())
        # Request can occur
        try:
            # Return cached message (at-most-once)
            circuit_breaker_response = CircuitBreakerHTTPResponse()
            serialized_response = redis_server.get(cache_prefix + request.id)
            circuit_breaker_response.ParseFromString(serialized_response)
            logger.info("Cached Request " + request.id)
            return circuit_breaker_response
        except:
            # Send HTTP request
            logger.info("Request " + request.id)
            http_response = send_http_request(request.http, request.timeout)
            # Request is successful as far as the circuit breaker is concerned if no HTTP status code is provided in the 'expected' list of the request object (and no state is ever set in Redis)
            if len(request.expected) > 0:
                if http_response.status not in request.expected:
                    change_circuit_state_for_hostname(host, status, failures, request.threshold, request.recovery)
                else:
                    reset_circuit_state_for_hostname(host)
            # Make response object
            circuit_breaker_response = CircuitBreakerHTTPResponse(id=request.id, status=status, wait=0, http=http_response)
            # Cache response
            redis_server.set(cache_prefix + request.id, circuit_breaker_response.SerializeToString())
            # Done
            return circuit_breaker_response
#-----------------------------------------------------------------------------------------

#
# Main
#
if __name__ == '__main__':
    redis_port = int(environ['REDIS_PORT'])
    circuit_breaker_port = str(int(environ['CIRCUIT_BREAKER_PORT']))
    #
    global redis_server
    redis_server = redis.Redis(host='circuit_breaker_redis', port=redis_port, decode_responses=True)
    logger.info(redis_server.ping())
    #
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    add_CircuitBreakerServicer_to_server(CircuitBreaker(), server)
    server.add_insecure_port('[::]:' + circuit_breaker_port)
    server.start()
    logger.info("Circuit Breaker microservice is ready")
    server.wait_for_termination()