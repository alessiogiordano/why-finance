from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StockRequest(_message.Message):
    __slots__ = ("ticker",)
    TICKER_FIELD_NUMBER: _ClassVar[int]
    ticker: str
    def __init__(self, ticker: _Optional[str] = ...) -> None: ...

class AverageStockRequest(_message.Message):
    __slots__ = ("ticker", "count")
    TICKER_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ticker: str
    count: int
    def __init__(self, ticker: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class StockResponse(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: float
    def __init__(self, value: _Optional[float] = ...) -> None: ...
