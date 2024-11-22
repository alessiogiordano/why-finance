#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 21/11/24.
#

import grpc

from http_pb2 import HTTPMethod, HTTPStatusCode, HTTPRequest, HTTPResponse
import circuit_breaker_pb2
import circuit_breaker_pb2_grpc

import concurrent.futures
import requests

class CircuitBreaker(circuit_breaker_pb2_grpc.CircuitBreakerServicer):
	def send(self, request, context):
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
		# match...case is only available from 3.10 (you're on 3.9)
		#
		print(method + " " + request.url)
		response = requests.request(method, request.url, headers=request.headers, data=request.body)
		print("Response: " + str(response.status_code))
		#
		status = HTTPStatusCode.BREAKER_UNKNOWN
		try:
		    status = HTTPStatusCode.Value(HTTPStatusCode.Name(response.status_code))
		except:
			pass
		if response.status_code >= 400:
			print("TODO: Breaker functionality here")
			print("TODO: Let client decide the valid status codes")
		#
		return HTTPResponse(status=status, headers=response.headers, body=response.text)

if __name__ == '__main__':
	server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=4))
	circuit_breaker_pb2_grpc.add_CircuitBreakerServicer_to_server(CircuitBreaker(), server)
	server.add_insecure_port('[::]:60600')
	server.start()
	print("Circuit Breaker microservice is ready")
	server.wait_for_termination()
