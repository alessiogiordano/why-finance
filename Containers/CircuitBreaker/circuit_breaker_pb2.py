# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: circuit_breaker.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import http_pb2 as http__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63ircuit_breaker.proto\x1a\nhttp.proto\"P\n\x1b\x43ircuitBreakerStatusRequest\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x11\n\tthreshold\x18\x02 \x01(\r\x12\x10\n\x08recovery\x18\x03 \x01(\r\"a\n\x1c\x43ircuitBreakerStatusResponse\x12\x0c\n\x04host\x18\x01 \x01(\t\x12%\n\x06status\x18\x02 \x01(\x0e\x32\x15.CircuitBreakerStatus\x12\x0c\n\x04wait\x18\x03 \x01(\r\"\x9c\x01\n\x19\x43ircuitBreakerHTTPRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12!\n\x08\x65xpected\x18\x02 \x03(\x0e\x32\x0f.HTTPStatusCode\x12\x0f\n\x07timeout\x18\x03 \x01(\r\x12\x11\n\tthreshold\x18\x04 \x01(\r\x12\x10\n\x08recovery\x18\x05 \x01(\r\x12\x1a\n\x04http\x18\x06 \x01(\x0b\x32\x0c.HTTPRequest\"z\n\x1a\x43ircuitBreakerHTTPResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12%\n\x06status\x18\x02 \x01(\x0e\x32\x15.CircuitBreakerStatus\x12\x0c\n\x04wait\x18\x03 \x01(\r\x12\x1b\n\x04http\x18\x04 \x01(\x0b\x32\r.HTTPResponse*h\n\x14\x43ircuitBreakerStatus\x12\x19\n\x15\x43ircuitBreaker_CLOSED\x10\x00\x12\x1c\n\x18\x43ircuitBreaker_HALF_OPEN\x10\x01\x12\x17\n\x13\x43ircuitBreaker_OPEN\x10\x02\x32\xa8\x02\n\x0e\x43ircuitBreaker\x12\x45\n\x06status\x12\x1c.CircuitBreakerStatusRequest\x1a\x1d.CircuitBreakerStatusResponse\x12\x46\n\x07success\x12\x1c.CircuitBreakerStatusRequest\x1a\x1d.CircuitBreakerStatusResponse\x12\x46\n\x07\x66\x61ilure\x12\x1c.CircuitBreakerStatusRequest\x1a\x1d.CircuitBreakerStatusResponse\x12?\n\x04send\x12\x1a.CircuitBreakerHTTPRequest\x1a\x1b.CircuitBreakerHTTPResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'circuit_breaker_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CIRCUITBREAKERSTATUS']._serialized_start=501
  _globals['_CIRCUITBREAKERSTATUS']._serialized_end=605
  _globals['_CIRCUITBREAKERSTATUSREQUEST']._serialized_start=37
  _globals['_CIRCUITBREAKERSTATUSREQUEST']._serialized_end=117
  _globals['_CIRCUITBREAKERSTATUSRESPONSE']._serialized_start=119
  _globals['_CIRCUITBREAKERSTATUSRESPONSE']._serialized_end=216
  _globals['_CIRCUITBREAKERHTTPREQUEST']._serialized_start=219
  _globals['_CIRCUITBREAKERHTTPREQUEST']._serialized_end=375
  _globals['_CIRCUITBREAKERHTTPRESPONSE']._serialized_start=377
  _globals['_CIRCUITBREAKERHTTPRESPONSE']._serialized_end=499
  _globals['_CIRCUITBREAKER']._serialized_start=608
  _globals['_CIRCUITBREAKER']._serialized_end=904
# @@protoc_insertion_point(module_scope)
