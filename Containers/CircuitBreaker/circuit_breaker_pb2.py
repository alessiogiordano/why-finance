# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: circuit_breaker.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'circuit_breaker.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import http_pb2 as http__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63ircuit_breaker.proto\x1a\nhttp.proto25\n\x0e\x43ircuitBreaker\x12#\n\x04send\x12\x0c.HTTPRequest\x1a\r.HTTPResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'circuit_breaker_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CIRCUITBREAKER']._serialized_start=37
  _globals['_CIRCUITBREAKER']._serialized_end=90
# @@protoc_insertion_point(module_scope)