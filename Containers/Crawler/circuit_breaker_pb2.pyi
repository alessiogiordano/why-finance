import http_pb2 as _http_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CircuitBreakerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CircuitBreaker_CLOSED: _ClassVar[CircuitBreakerStatus]
    CircuitBreaker_HALF_OPEN: _ClassVar[CircuitBreakerStatus]
    CircuitBreaker_OPEN: _ClassVar[CircuitBreakerStatus]
CircuitBreaker_CLOSED: CircuitBreakerStatus
CircuitBreaker_HALF_OPEN: CircuitBreakerStatus
CircuitBreaker_OPEN: CircuitBreakerStatus

class CircuitBreakerStatusRequest(_message.Message):
    __slots__ = ("host", "threshold", "recovery")
    HOST_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_FIELD_NUMBER: _ClassVar[int]
    host: str
    threshold: int
    recovery: int
    def __init__(self, host: _Optional[str] = ..., threshold: _Optional[int] = ..., recovery: _Optional[int] = ...) -> None: ...

class CircuitBreakerStatusResponse(_message.Message):
    __slots__ = ("host", "status", "wait")
    HOST_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WAIT_FIELD_NUMBER: _ClassVar[int]
    host: str
    status: CircuitBreakerStatus
    wait: int
    def __init__(self, host: _Optional[str] = ..., status: _Optional[_Union[CircuitBreakerStatus, str]] = ..., wait: _Optional[int] = ...) -> None: ...

class CircuitBreakerHTTPRequest(_message.Message):
    __slots__ = ("id", "expected", "timeout", "threshold", "recovery", "http")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    id: str
    expected: _containers.RepeatedScalarFieldContainer[_http_pb2.HTTPStatusCode]
    timeout: int
    threshold: int
    recovery: int
    http: _http_pb2.HTTPRequest
    def __init__(self, id: _Optional[str] = ..., expected: _Optional[_Iterable[_Union[_http_pb2.HTTPStatusCode, str]]] = ..., timeout: _Optional[int] = ..., threshold: _Optional[int] = ..., recovery: _Optional[int] = ..., http: _Optional[_Union[_http_pb2.HTTPRequest, _Mapping]] = ...) -> None: ...

class CircuitBreakerHTTPResponse(_message.Message):
    __slots__ = ("id", "status", "wait", "http")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WAIT_FIELD_NUMBER: _ClassVar[int]
    HTTP_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: CircuitBreakerStatus
    wait: int
    http: _http_pb2.HTTPResponse
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[CircuitBreakerStatus, str]] = ..., wait: _Optional[int] = ..., http: _Optional[_Union[_http_pb2.HTTPResponse, _Mapping]] = ...) -> None: ...
