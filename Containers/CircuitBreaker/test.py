#
#  test.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

import sys
import uuid
import grpc

from http_pb2 import HTTPMethod, HTTPStatusCode, HTTPRequest, HTTPResponse
from circuit_breaker_pb2 import CircuitBreakerStatus
from circuit_breaker_pb2 import CircuitBreakerRequest
from circuit_breaker_pb2_grpc import CircuitBreakerStub

# From: https://grpc.io/docs/guides/retry/
retry_configuration = [
    ('grpc.service_config', '{"retryPolicy": {"maxAttempts": 3, "initialBackoff": "0.1s", "maxBackoff": "1s", "backoffMultiplier": 2, "retryableStatusCodes": ["UNAVAILABLE"]}}')
]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: test.py 10.0.0.16:30112")
        exit()
    with grpc.insecure_channel(sys.argv[1], options=retry_configuration) as channel:
        circuit_breaker = CircuitBreakerStub(channel)
        http_request = HTTPRequest(url="https://example.com/")
        print("Sending request to " + http_request.url)
        request = CircuitBreakerRequest(id=uuid.uuid4().hex, expected=[200], timeout=30, threshold=3, recovery=30, http=http_request)
        response = circuit_breaker.send(request, timeout=60) # twice the HTTP request timeout
        print("Response: " + CircuitBreakerStatus.Name(response.status) + " " + str(response.http.status))