from os import environ
import mysql.connector
import time

# Logging
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

# Configurazioni per i database
USER_DB_CONFIG = {
    "host": environ.get('USER_DB_HOST', 'mysql_user'),
    "user": environ.get('DB_USER', 'root'),
    "password": environ.get('DB_PASSWORD', 'root'),
    "database": environ.get('USER_DB_NAME', 'user_db'),
    "port": int(environ.get('DB_PORT', '3306'))
}

TICKER_DB_CONFIG = {
    "host": environ.get('TICKER_DB_HOST', 'mysql_ticker'),
    "user": environ.get('DB_USER', 'root'),
    "password": environ.get('DB_PASSWORD', 'root'),
    "database": environ.get('TICKER_DB_NAME', 'ticker_db'),
    "port": int(environ.get('DB_PORT', '3306'))
}

# Funzione per attendere MySQL
def wait_for_mysql(db_config, max_retries=30, delay=2):
    for i in range(max_retries):
        try:
            logger.info(f"Tentativo di connessione a {db_config['host']} {i+1}/{max_retries}")
            conn = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                port=db_config["port"]
            )
            logger.info(f"Connessione a {db_config['host']} stabilita con successo!")
            return conn
        except mysql.connector.Error as err:
            logger.error(f"Errore di connessione: {err}")
            if i < max_retries - 1:
                logger.info(f"Riprovo tra {delay} secondi...")
                time.sleep(delay)
    raise Exception(f"Impossibile connettersi al database {db_config['host']} dopo i tentativi massimi.")

# Funzione per verificare o creare database
def ensure_database_exists(db_config):
    try:
        conn = wait_for_mysql(db_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        logger.info(f"Database '{db_config['database']}' creato o già esistente su {db_config['host']}.")
        conn.close()
    except Exception as e:
        logger.error(f"Errore durante la creazione del database {db_config['database']}: {e}")
        raise

# Funzione per creare le tabelle
def create_tables(db_config, table_definitions):
    try:
        ensure_database_exists(db_config)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for table_name, table_sql in table_definitions.items():
            cursor.execute(table_sql)
            logger.info(f"Tabella '{table_name}' creata o già esistente su {db_config['database']}.")

        conn.commit()
        logger.info(f"Tabelle per il database '{db_config['database']}' inizializzate con successo.")
    except Exception as e:
        logger.error(f"Errore durante la creazione delle tabelle su {db_config['database']}: {e}")
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            logger.info(f"Connessione al database '{db_config['database']}' chiusa.")

if __name__ == "__main__":
    try:
        # Definizioni delle tabelle per user_db
        user_table_definitions = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    device_id INT AUTO_INCREMENT PRIMARY KEY,
                    ticker VARCHAR(10) NOT NULL,
                    device_token VARCHAR(255),
                    low_value DECIMAL(10, 2),
                    high_value DECIMAL(10, 2)
                );
            """
        }

        # Definizioni delle tabelle per ticker_db
        ticker_table_definitions = {
            "tickers": """
                CREATE TABLE IF NOT EXISTS stock_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ticker VARCHAR(10),
                value DECIMAL(10, 2),
                timestamp DATETIME
            );
            """
        }

        # Creazione tabelle per user_db
        logger.info("Inizializzazione tabelle per 'user_db'.")
        create_tables(USER_DB_CONFIG, user_table_definitions)

        # Creazione tabelle per ticker_db
        logger.info("Inizializzazione tabelle per 'ticker_db'.")
        create_tables(TICKER_DB_CONFIG, ticker_table_definitions)

    except Exception as e:
        logger.error(f"Errore fatale durante l'inizializzazione: {e}")
        exit(1)
