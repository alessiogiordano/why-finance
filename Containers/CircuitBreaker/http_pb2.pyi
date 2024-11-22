from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HTTPMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HTTP_GET: _ClassVar[HTTPMethod]
    HTTP_HEAD: _ClassVar[HTTPMethod]
    HTTP_POST: _ClassVar[HTTPMethod]
    HTTP_PUT: _ClassVar[HTTPMethod]
    HTTP_DELETE: _ClassVar[HTTPMethod]
    HTTP_CONNECT: _ClassVar[HTTPMethod]
    HTTP_OPTIONS: _ClassVar[HTTPMethod]
    HTTP_TRACE: _ClassVar[HTTPMethod]
    HTTP_PATCH: _ClassVar[HTTPMethod]

class HTTPStatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BREAKER_UNKNOWN: _ClassVar[HTTPStatusCode]
    HTTP_CONTINUE: _ClassVar[HTTPStatusCode]
    HTTP_SWITCHING_PROTOCOLS: _ClassVar[HTTPStatusCode]
    HTTP_PROCESSING: _ClassVar[HTTPStatusCode]
    HTTP_EARLY_HINTS: _ClassVar[HTTPStatusCode]
    HTTP_OK: _ClassVar[HTTPStatusCode]
    HTTP_CREATED: _ClassVar[HTTPStatusCode]
    HTTP_ACCEPTED: _ClassVar[HTTPStatusCode]
    HTTP_NON_AUTHORITATIVE_INFORMATION: _ClassVar[HTTPStatusCode]
    HTTP_NO_CONTENT: _ClassVar[HTTPStatusCode]
    HTTP_RESET_CONTENT: _ClassVar[HTTPStatusCode]
    HTTP_PARTIAL_CONTENT: _ClassVar[HTTPStatusCode]
    HTTP_MULTI_STATUS: _ClassVar[HTTPStatusCode]
    HTTP_ALREADY_REPORTED: _ClassVar[HTTPStatusCode]
    HTTP_IM_USED: _ClassVar[HTTPStatusCode]
    HTTP_MULTIPLE_CHOICES: _ClassVar[HTTPStatusCode]
    HTTP_MOVED_PERMANENTLY: _ClassVar[HTTPStatusCode]
    HTTP_FOUND: _ClassVar[HTTPStatusCode]
    HTTP_SEE_OTHER: _ClassVar[HTTPStatusCode]
    HTTP_NOT_MODIFIED: _ClassVar[HTTPStatusCode]
    HTTP_USE_PROXY: _ClassVar[HTTPStatusCode]
    HTTP_TEMPORARY_REDIRECT: _ClassVar[HTTPStatusCode]
    HTTP_PERMANENT_REDIRECT: _ClassVar[HTTPStatusCode]
    HTTP_BAD_REQUEST: _ClassVar[HTTPStatusCode]
    HTTP_UNAUTHORIZED: _ClassVar[HTTPStatusCode]
    HTTP_PAYMENT_REQUIRED: _ClassVar[HTTPStatusCode]
    HTTP_FORBIDDEN: _ClassVar[HTTPStatusCode]
    HTTP_NOT_FOUND: _ClassVar[HTTPStatusCode]
    HTTP_METHOD_NOT_ALLOWED: _ClassVar[HTTPStatusCode]
    HTTP_NOT_ACCEPTABLE: _ClassVar[HTTPStatusCode]
    HTTP_PROXY_AUTHENTICATION_REQUIRED: _ClassVar[HTTPStatusCode]
    HTTP_REQUEST_TIMEOUT: _ClassVar[HTTPStatusCode]
    HTTP_CONFLICT: _ClassVar[HTTPStatusCode]
    HTTP_GONE: _ClassVar[HTTPStatusCode]
    HTTP_LENGTH_REQUIRED: _ClassVar[HTTPStatusCode]
    HTTP_PRECONDITION_FAILED: _ClassVar[HTTPStatusCode]
    HTTP_CONTENT_TOO_LARGE: _ClassVar[HTTPStatusCode]
    HTTP_URI_TOO_LONG: _ClassVar[HTTPStatusCode]
    HTTP_UNSUPPORTED_MEDIA_TYPE: _ClassVar[HTTPStatusCode]
    HTTP_RANGE_NOT_SATISFIABLE: _ClassVar[HTTPStatusCode]
    HTTP_EXPECTATION_FAILED: _ClassVar[HTTPStatusCode]
    HTTP_IM_A_TEAPOT: _ClassVar[HTTPStatusCode]
    HTTP_MISDIRECTED_REQUEST: _ClassVar[HTTPStatusCode]
    HTTP_UNPROCESSABLE_CONTENT: _ClassVar[HTTPStatusCode]
    HTTP_LOCKED: _ClassVar[HTTPStatusCode]
    HTTP_FAILED_DEPENDENCY: _ClassVar[HTTPStatusCode]
    HTTP_TOO_EARLY: _ClassVar[HTTPStatusCode]
    HTTP_UPGRADE_REQUIRED: _ClassVar[HTTPStatusCode]
    HTTP_PRECONDITION_REQUIRED: _ClassVar[HTTPStatusCode]
    HTTP_TOO_MANY_REQUESTS: _ClassVar[HTTPStatusCode]
    HTTP_REQUEST_HEADER_FIELDS_TOO_LARGE: _ClassVar[HTTPStatusCode]
    HTTP_UNAVAILABLE_FOR_LEGAL_REASONS: _ClassVar[HTTPStatusCode]
    HTTP_INTERNAL_SERVER_ERROR: _ClassVar[HTTPStatusCode]
    HTTP_NOT_IMPLEMENTED: _ClassVar[HTTPStatusCode]
    HTTP_BAD_GATEWAY: _ClassVar[HTTPStatusCode]
    HTTP_SERVICE_UNAVAILABLE: _ClassVar[HTTPStatusCode]
    HTTP_GATEWAY_TIMEOUT: _ClassVar[HTTPStatusCode]
    HTTP_VERSION_NOT_SUPPORTED: _ClassVar[HTTPStatusCode]
    HTTP_VARIANT_ALSO_NEGOTIATES: _ClassVar[HTTPStatusCode]
    HTTP_INSUFFICIENT_STORAGE: _ClassVar[HTTPStatusCode]
    HTTP_LOOP_DETECTED: _ClassVar[HTTPStatusCode]
    HTTP_NOT_EXTENDED: _ClassVar[HTTPStatusCode]
    HTTP_NETWORK_AUTHENTICATION_REQUIRED: _ClassVar[HTTPStatusCode]
    BREAKER_CIRCUIT_OPEN: _ClassVar[HTTPStatusCode]
    BREAKER_CIRCUIT_HALF_OPEN: _ClassVar[HTTPStatusCode]
HTTP_GET: HTTPMethod
HTTP_HEAD: HTTPMethod
HTTP_POST: HTTPMethod
HTTP_PUT: HTTPMethod
HTTP_DELETE: HTTPMethod
HTTP_CONNECT: HTTPMethod
HTTP_OPTIONS: HTTPMethod
HTTP_TRACE: HTTPMethod
HTTP_PATCH: HTTPMethod
BREAKER_UNKNOWN: HTTPStatusCode
HTTP_CONTINUE: HTTPStatusCode
HTTP_SWITCHING_PROTOCOLS: HTTPStatusCode
HTTP_PROCESSING: HTTPStatusCode
HTTP_EARLY_HINTS: HTTPStatusCode
HTTP_OK: HTTPStatusCode
HTTP_CREATED: HTTPStatusCode
HTTP_ACCEPTED: HTTPStatusCode
HTTP_NON_AUTHORITATIVE_INFORMATION: HTTPStatusCode
HTTP_NO_CONTENT: HTTPStatusCode
HTTP_RESET_CONTENT: HTTPStatusCode
HTTP_PARTIAL_CONTENT: HTTPStatusCode
HTTP_MULTI_STATUS: HTTPStatusCode
HTTP_ALREADY_REPORTED: HTTPStatusCode
HTTP_IM_USED: HTTPStatusCode
HTTP_MULTIPLE_CHOICES: HTTPStatusCode
HTTP_MOVED_PERMANENTLY: HTTPStatusCode
HTTP_FOUND: HTTPStatusCode
HTTP_SEE_OTHER: HTTPStatusCode
HTTP_NOT_MODIFIED: HTTPStatusCode
HTTP_USE_PROXY: HTTPStatusCode
HTTP_TEMPORARY_REDIRECT: HTTPStatusCode
HTTP_PERMANENT_REDIRECT: HTTPStatusCode
HTTP_BAD_REQUEST: HTTPStatusCode
HTTP_UNAUTHORIZED: HTTPStatusCode
HTTP_PAYMENT_REQUIRED: HTTPStatusCode
HTTP_FORBIDDEN: HTTPStatusCode
HTTP_NOT_FOUND: HTTPStatusCode
HTTP_METHOD_NOT_ALLOWED: HTTPStatusCode
HTTP_NOT_ACCEPTABLE: HTTPStatusCode
HTTP_PROXY_AUTHENTICATION_REQUIRED: HTTPStatusCode
HTTP_REQUEST_TIMEOUT: HTTPStatusCode
HTTP_CONFLICT: HTTPStatusCode
HTTP_GONE: HTTPStatusCode
HTTP_LENGTH_REQUIRED: HTTPStatusCode
HTTP_PRECONDITION_FAILED: HTTPStatusCode
HTTP_CONTENT_TOO_LARGE: HTTPStatusCode
HTTP_URI_TOO_LONG: HTTPStatusCode
HTTP_UNSUPPORTED_MEDIA_TYPE: HTTPStatusCode
HTTP_RANGE_NOT_SATISFIABLE: HTTPStatusCode
HTTP_EXPECTATION_FAILED: HTTPStatusCode
HTTP_IM_A_TEAPOT: HTTPStatusCode
HTTP_MISDIRECTED_REQUEST: HTTPStatusCode
HTTP_UNPROCESSABLE_CONTENT: HTTPStatusCode
HTTP_LOCKED: HTTPStatusCode
HTTP_FAILED_DEPENDENCY: HTTPStatusCode
HTTP_TOO_EARLY: HTTPStatusCode
HTTP_UPGRADE_REQUIRED: HTTPStatusCode
HTTP_PRECONDITION_REQUIRED: HTTPStatusCode
HTTP_TOO_MANY_REQUESTS: HTTPStatusCode
HTTP_REQUEST_HEADER_FIELDS_TOO_LARGE: HTTPStatusCode
HTTP_UNAVAILABLE_FOR_LEGAL_REASONS: HTTPStatusCode
HTTP_INTERNAL_SERVER_ERROR: HTTPStatusCode
HTTP_NOT_IMPLEMENTED: HTTPStatusCode
HTTP_BAD_GATEWAY: HTTPStatusCode
HTTP_SERVICE_UNAVAILABLE: HTTPStatusCode
HTTP_GATEWAY_TIMEOUT: HTTPStatusCode
HTTP_VERSION_NOT_SUPPORTED: HTTPStatusCode
HTTP_VARIANT_ALSO_NEGOTIATES: HTTPStatusCode
HTTP_INSUFFICIENT_STORAGE: HTTPStatusCode
HTTP_LOOP_DETECTED: HTTPStatusCode
HTTP_NOT_EXTENDED: HTTPStatusCode
HTTP_NETWORK_AUTHENTICATION_REQUIRED: HTTPStatusCode
BREAKER_CIRCUIT_OPEN: HTTPStatusCode
BREAKER_CIRCUIT_HALF_OPEN: HTTPStatusCode

class HTTPRequest(_message.Message):
    __slots__ = ("method", "url", "headers", "body")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    METHOD_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    method: HTTPMethod
    url: str
    headers: _containers.ScalarMap[str, str]
    body: str
    def __init__(self, method: _Optional[_Union[HTTPMethod, str]] = ..., url: _Optional[str] = ..., headers: _Optional[_Mapping[str, str]] = ..., body: _Optional[str] = ...) -> None: ...

class HTTPResponse(_message.Message):
    __slots__ = ("status", "headers", "body")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    status: HTTPStatusCode
    headers: _containers.ScalarMap[str, str]
    body: str
    def __init__(self, status: _Optional[_Union[HTTPStatusCode, str]] = ..., headers: _Optional[_Mapping[str, str]] = ..., body: _Optional[str] = ...) -> None: ...
