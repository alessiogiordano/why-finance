#
#  breaker.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 21/12/24.
#

import grpc
from circuit_breaker_pb2 import CircuitBreakerStatus
from circuit_breaker_pb2 import CircuitBreakerStatusRequest, CircuitBreakerStatusResponse
from circuit_breaker_pb2_grpc import CircuitBreakerStub
from os import environ # Environment Variables

# Usage: import utils.breaker
# ------ with utils.breaker.context("example.com") as circuit_breaker:
# ---------- # Code goes here
# Or:    from utils.breaker import context as circuit_breaker
# ------ with circuit_breaker("example.com"):
# ---------- # Code goes here
class context:
    def __init__(self, host, threshold=3, recovery=30, **kwargs):
        if (type(host) is not str) or (type(threshold) is not int) or (type(recovery) is not int):
            raise ValueError("Provide 3 arguments: a host string and integer threshold and recovery values")
        self.manual = True if ('manual' in kwargs) and (kwargs['manual'] == True) else False
        self.insecure_channel = None
        self.circuit_breaker = None
        self.status_request = CircuitBreakerStatusRequest(host=host, threshold=threshold, recovery=recovery)
    #-------------------------------------------------------------------------------------
    def assert_closed_or_half_open(self):
        response = self.circuit_breaker.status(self.status_request)
        assert response.status is not CircuitBreakerStatus.CircuitBreaker_OPEN
    #-------------------------------------------------------------------------------------
    def report_successful_connection(self):
        self.circuit_breaker.success(self.status_request)
    #-------------------------------------------------------------------------------------
    def report_failed_connection(self):
        self.circuit_breaker.failure(self.status_request)
    #-------------------------------------------------------------------------------------
    def __enter__(self):
        circuit_breaker_host = "circuit_breaker:" + str(int(environ['CIRCUIT_BREAKER_PORT']))
        self.insecure_channel = grpc.insecure_channel(circuit_breaker_host)
        self.circuit_breaker = CircuitBreakerStub(self.insecure_channel)
        if not self.manual:
            self.assert_closed_or_half_open()
        return self
    #-------------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc, exc_tb):
        if not self.manual:
            if exc is None:
                self.report_successful_connection()
            else:
                self.report_failed_connection()
            self.insecure_channel.close()
            return True # Suppress exceptions
        else:
            self.insecure_channel.close()
            return False # Rethrow exceptions
    #-------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------