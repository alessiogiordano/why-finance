#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

from os import environ # Environment Variables

import yfinance as yf
import mysql.connector
from datetime import datetime
import time

from utils.breaker import context as circuit_breaker
from utils.logger import logger
from utils.broadcast import broadcast
from utils.subscribe import subscribe
from utils.monitor import monitor

from handlers.users import queries as QueryHandler
from handlers.stocks import commands as CommandHandler

query_handler = QueryHandler('users')
command_handler = CommandHandler('stocks')

def fetch_stock_price(ticker):
    with circuit_breaker("finance.yahoo.com"):
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        if history.empty:
            logger.info(f"STOCK NOT FOUND:\t{ticker}")
            return None
        current_price = history['Close'].iloc[-1]
        logger.info(f"FETCHED STOCK:\t{ticker}\t{current_price}")
        return current_price
    logger.error(f"ERROR FETCHING:\t{ticker}")
    return None
#-----------------------------------------------------------------------------------------

def crawl_ticker(ticker):
    price = fetch_stock_price(ticker)
    if price is not None:
        timestamp = datetime.now()
        command_handler.save_stock_data(ticker, price, timestamp)
        logger.info(f"STORED UPDATED:\t{ticker}\t{price}\t{timestamp}")
        broadcast('alert', {
            'ticker': ticker,
            'price': price,
            'timestamp': timestamp.isoformat()
        })
#-----------------------------------------------------------------------------------------

def crawl_tickers():
    tickers = query_handler.get_all_tickers()
    for element in tickers:
        crawl_ticker(element[0])
#-----------------------------------------------------------------------------------------

def crawl_tickers_at_interval():
    # these global variables should be initialized in __main__
    global interval, count, timestamp
    start_time = time.time()
    if (int(start_time) - timestamp) >= interval:
        logger.info("WILL BEGIN CYCLE #{}".format(count))
        crawl_tickers()
        finishing_time = time.time()
        logger.info("DID COMPLETE CYCLE #{}".format(count))
        #
        global count_monitor, duration_monitor
        count_monitor.inc()
        duration_monitor.set(finishing_time - start_time)
        #
        timestamp = int(finishing_time)
        count += 1
#-----------------------------------------------------------------------------------------

if __name__ == "__main__":
    global interval, count, timestamp
    interval = int(environ.get('CRAWLER_TIME_INTERVAL', '3600')) # Defaults to 1 hour
    count = 0
    timestamp = int(time.time()) - interval # Crawl immediately
    #
    global count_monitor, duration_monitor
    count_monitor = monitor.counter("crawler_cycle_count", "The number of completed crawling cycles")
    duration_monitor = monitor.gauge("crawler_cycle_duration", "The duration in seconds of a crawling cycle")
    #
    subscribe(before=crawl_tickers_at_interval, callback=crawl_ticker, log=True)
#-----------------------------------------------------------------------------------------