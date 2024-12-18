from services.query_handler import QueryHandler
from services.command_handler import CommandHandler
from utils.fetcher import fetch_stock_price
from utils.circuit_breaker_utils import CircuitBreaker
from utils.config import CIRCUIT_BREAKER_HOST, CRAWLER_TIME_INTERVAL
from utils.logger import logger
from database.connection import wait_for_mysql
from datetime import datetime
from utils.config import USER_DB_CONFIG, TICKER_DB_CONFIG

class CrawlerService:
    def __init__(self):
        self.query_handler = QueryHandler('user')
        self.command_handler = CommandHandler('ticker')
        self.crawler_time_interval = CRAWLER_TIME_INTERVAL
        self.circuit_breaker = CircuitBreaker(
            host=CIRCUIT_BREAKER_HOST,
            threshold=3,
            recovery=30
        )

        # Attende la disponibilità dei database
        # wait_for_mysql("user")
        # wait_for_mysql("ticker")

    def collect_data(self):
        """
        Recupera i ticker dal database, ottiene i prezzi e salva i dati.
        """
        tickers = self.query_handler.get_all_tickers()
        for ticker in tickers:
            try:
                price = fetch_stock_price(ticker, self.circuit_breaker)
                if price is not None:
                    timestamp = datetime.now()
                    self.command_handler.save_stock_data(ticker, price, timestamp)
                    logger.info(f"Dati salvati per {ticker}: {price} a {timestamp}")
            except Exception as e:
                logger.error(f"Errore nel processo per {ticker}: {e}")
