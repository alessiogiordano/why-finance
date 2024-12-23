from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserDataRequest(_message.Message):
    __slots__ = ("device_id", "ticker", "device_token", "low_value", "high_value")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    ticker: str
    device_token: str
    low_value: float
    high_value: float
    def __init__(self, device_id: _Optional[str] = ..., ticker: _Optional[str] = ..., device_token: _Optional[str] = ..., low_value: _Optional[float] = ..., high_value: _Optional[float] = ...) -> None: ...

class UserDeletionRequest(_message.Message):
    __slots__ = ("device_id",)
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    device_id: str
    def __init__(self, device_id: _Optional[str] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
