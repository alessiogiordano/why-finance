import os
from circuit_breaker_pb2 import CircuitBreakerStatusRequest

USER_DB_CONFIG = {
    "host": os.environ.get('USER_DB_HOST', 'mysql_user'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', 'root'),
    "database": os.environ.get('USER_DB_NAME', 'user_db'),
    "port": int(os.environ.get('DB_PORT', '3306'))
}

TICKER_DB_CONFIG = {
    "host": os.environ.get('TICKER_DB_HOST', 'mysql_ticker'),
    "user": os.environ.get('DB_USER', 'root'),
    "password": os.environ.get('DB_PASSWORD', 'root'),
    "database": os.environ.get('TICKER_DB_NAME', 'ticker_db'),
    "port": int(os.environ.get('DB_PORT', '3306'))
}

CIRCUIT_BREAKER_HOST = f"circuit_breaker:{os.environ.get('CIRCUIT_BREAKER_PORT', '5000')}"
CRAWLER_TIME_INTERVAL = int(os.environ.get('CRAWLER_TIME_INTERVAL', '3600'))

yfinance_circuit_breaker_req = CircuitBreakerStatusRequest(
    host="finance.yahoo.com",
    threshold=3,
    recovery=30
)
