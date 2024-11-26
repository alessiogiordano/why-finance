#
#  crawler.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

from os import environ # Environment Variables
import grpc
from circuit_breaker_pb2 import CircuitBreakerStatus
from circuit_breaker_pb2 import CircuitBreakerStatusRequest, CircuitBreakerStatusResponse
from circuit_breaker_pb2_grpc import CircuitBreakerStub

import yfinance as yf
import mysql.connector
from datetime import datetime
import time

#
# Logging
#
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log")
    ]
)
logger = logging.getLogger(__name__)
#-----------------------------------------------------------------------------------------

#
# Database
#
DB_CONFIG = {
    "host": environ.get('DB_HOST', 'mysql'),
    "user": environ.get('DB_USER', 'root'),
    "password": environ.get('DB_PASSWORD', 'root'),
    "database": environ.get('DB_NAME', 'dsbd_homework1'),
    "port": int(environ.get('DB_PORT', '3306'))
}
def connect_to_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
#-----------------------------------------------------------------------------------------
def fetch_tickers():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ticker from users")
    tickers = cursor.fetchall()
    conn.close()
    return tickers
#-----------------------------------------------------------------------------------------
def save_stock_data(ticker, value, timestamp):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stock_data (ticker, value, timestamp) VALUES (%s, %s, %s)",
        (ticker, value, timestamp)
    )
    conn.commit()
    conn.close()
#-----------------------------------------------------------------------------------------


#
# Circuit Breaker
#
circuit_breaker_host = "circuit_breaker:" + str(int(environ['CIRCUIT_BREAKER_PORT']))
yfinance_circuit_breaker = CircuitBreakerStatusRequest(host="finance.yahoo.com", threshold=3, recovery=30)
def assert_closed_or_half_open(circuit_breaker):
    response = circuit_breaker.status(yfinance_circuit_breaker)
    assert response.status is not CircuitBreakerStatus.CircuitBreaker_OPEN
#-----------------------------------------------------------------------------------------
def report_successful_connection(circuit_breaker):
    circuit_breaker.success(yfinance_circuit_breaker)
#-----------------------------------------------------------------------------------------
def report_failed_connection(circuit_breaker):
    circuit_breaker.failure(yfinance_circuit_breaker)
#-----------------------------------------------------------------------------------------


def fetch_stock_price(ticker, max_retries=1, cooldown=60):
    with grpc.insecure_channel(circuit_breaker_host) as channel:
        circuit_breaker = CircuitBreakerStub(channel)
        try:
            assert_closed_or_half_open(circuit_breaker) # Circuit Breaker
        except Exception as e:
            logger.info(f"Circuit Breaker is Open: " + str(e))
            return None
        #
        retries = 0
        while retries < max_retries:
            try:
                stock = yf.Ticker(ticker)
                report_successful_connection(circuit_breaker) # Circuit Breaker
                
                history = stock.history(period="1d")
                if history.empty:
                    logger.info(f"Il simbolo {ticker} non ha dati disponibili. Potrebbe essere delisted o non valido.")
                    return None
    
                current_price = history['Close'].iloc[-1]
                logger.info(f"Recuperato stock: {ticker} ---- Prezzo corrente: {current_price}")
                return current_price
            except Exception as e:
                report_failed_connection(circuit_breaker)
                logger.info(f"Errore nel recupero dei dati per {ticker}: {e}")
                retries += 1
                time.sleep(cooldown)
        logger.info(f"Errore persistente: superato il numero massimo di tentativi per {ticker}")
        return None


def collect_data():
    tickers = fetch_tickers()
    for element in tickers:
        ticker = element[0]
        price = fetch_stock_price(ticker)
        if price is not None:
            timestamp = datetime.now()
            save_stock_data(ticker, price, timestamp)
            logger.info(f"Dati salvati per {ticker}: {price} a {timestamp}")

def wait_for_mysql():
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            conn.close()
            logger.info("Connesso con successo al database!")
            break
        except mysql.connector.Error as e:
            logger.info("In attesa del database MySQL... Riprovo in 5 secondi.")
            logger.info("La configuraizone è: {DB_CONFIG}")
            time.sleep(5)

if __name__ == "__main__":
    count = 0
    wait_for_mysql()
    while True:
        collect_data()
        logger.info("Ciclo di inserimento n. {}".format(count))
        time.sleep(int(environ.get('CRAWLER_TIME_INTERVAL', '3600'))) # Defaults to 1 hour
        count += 1