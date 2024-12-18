import yfinance as yf
import time
from utils.logger import logger


def fetch_stock_price(ticker, circuit_breaker):
    """
    Recupera il prezzo dello stock per un determinato ticker.
    :param ticker: Simbolo dello stock (es. 'AAPL').
    :param circuit_breaker: Istanza del Circuit Breaker.
    :return: Prezzo corrente dello stock o None in caso di errore.
    """
    try:
        # Controllo dello stato del Circuit Breaker
        circuit_breaker.assert_closed_or_half_open()
    except Exception as e:
        logger.error(f"Circuit Breaker bloccato: {e}")
        return None

    retries = 0
    max_retries = 3
    cooldown = 5  # secondi

    while retries < max_retries:
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")

            if history.empty:
                logger.warning(f"Nessun dato disponibile per il ticker {ticker}.")
                return None

            current_price = history['Close'].iloc[-1]
            circuit_breaker.report_success()  # Segnala successo
            logger.info(f"Prezzo corrente di {ticker}: {current_price}")
            return current_price

        except Exception as e:
            retries += 1
            circuit_breaker.report_failure()  # Segnala fallimento
            logger.error(f"Errore durante il recupero di {ticker}: {e}. Tentativo {retries}/{max_retries}.")
            time.sleep(cooldown)

    logger.error(f"Superato il numero massimo di tentativi per {ticker}.")
    return None
