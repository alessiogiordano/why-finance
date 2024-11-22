#
#  test.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

import grpc

from http_pb2 import HTTPMethod, HTTPStatusCode, HTTPRequest, HTTPResponse
import circuit_breaker_pb2
import circuit_breaker_pb2_grpc

if __name__ == "__main__":
	with grpc.insecure_channel('localhost:60600') as channel:
		circuit_breaker = circuit_breaker_pb2_grpc.CircuitBreakerStub(channel)
		request = HTTPRequest(url="https://example.com/")
		print("Sending request to " + request.url)
		response = circuit_breaker.send(request)
		print("Response: " + str(response.status))
