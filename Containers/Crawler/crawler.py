import yfinance as yf
import mysql.connector
from datetime import datetime
import time

DB_CONFIG = {
    "host": "mysql",
    "user": "root",
    "password": "root",
    "database": "dsbd_homework1",
    "port": 3306
}

def connect_to_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def fetch_users():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT email, ticker FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def save_stock_data(email, ticker, value, timestamp):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stock_data (email, ticker, value, timestamp) VALUES (%s, %s, %s, %s)",
        (email, ticker, value, timestamp)
    )
    conn.commit()
    conn.close()
    
    
#TODO: ricordiamoc di implementare qui il circuit breaker come servizio esterno
def fetch_stock_price(ticker, max_retries=1, cooldown=60):
    retries = 0
    while retries < max_retries:
        try:
            stock = yf.Ticker(ticker)
            
            history = stock.history(period="1d")
            if history.empty:
                print(f"Il simbolo {ticker} non ha dati disponibili. Potrebbe essere delisted o non valido.")
                return None

            current_price = history['Close'].iloc[-1]
            print(f"Recuperato stock: {ticker} ---- Prezzo corrente: {current_price}")
            return current_price
        except Exception as e:
            print(f"Errore nel recupero dei dati per {ticker}: {e}")
            retries += 1
            time.sleep(cooldown)
    print(f"Errore persistente: superato il numero massimo di tentativi per {ticker}")
    return None


def collect_data():
    users = fetch_users()
    for email, ticker in users:
        price = fetch_stock_price(ticker)
        if price is not None:
            timestamp = datetime.now()
            save_stock_data(email, ticker, price, timestamp)
            print(f"Dati salvati per {email} - {ticker}: {price} a {timestamp}")

def fetch_and_save_stocks():
    try:
        print("Inizio recupero delle azioni...")
    
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        conn = connect_to_db()
        cursor = conn.cursor()

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                name = stock.info.get("shortName", "Unknown")
                cursor.execute(
                    """
                    INSERT IGNORE INTO stocks_list (ticker, name)
                    VALUES (%s, %s)
                    """,
                    (ticker, name)
                )
                print(f"Azione salvata: {ticker} - {name}")
            except Exception as e:
                print(f"Errore durante il recupero delle informazioni per {ticker}: {e}")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Errore durante il recupero e il salvataggio delle azioni: {e}")

def wait_for_mysql():
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            conn.close()
            print("Connesso con successo al database!")
            break
        except mysql.connector.Error as e:
            print("In attesa del database MySQL... Riprovo in 5 secondi.")
            print("La configuraizone è: {DB_CONFIG}")
            time.sleep(5)
            


if __name__ == "__main__":
    count = 0
    wait_for_mysql()
    fetch_and_save_stocks()
    while True:
        collect_data()
        print("Ciclo di inserimento n. {}".format(count))
        time.sleep(3) #TODO: cambiare in ogni ora ??? Adesso sono 3 secondi per debuggare meglio 
        
        count += 1
        