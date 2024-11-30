#
#  create_tables.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Updated by OpenAI Assistant
#

from os import environ  # Environment Variables
import mysql.connector
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
# -----------------------------------------------------------------------------------------

#
# Database
#

DB_CONFIG = {
    "host": environ.get('DB_HOST', 'mysql'),
    "user": environ.get('DB_USER', 'root'),
    "password": environ.get('DB_PASSWORD', 'root'),
    "database": environ.get('DB_NAME', 'whyfinance_hw1'),
    "port": int(environ.get('DB_PORT', '3306'))
}

def wait_for_mysql(max_retries=30, delay=2):
    for i in range(max_retries):
        try:
            logger.info(f"Tentativo di connessione a MySQL {i+1}/{max_retries}")
            conn = mysql.connector.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                port=DB_CONFIG["port"]
            )
            logger.info("Connessione a MySQL stabilita con successo!")
            return conn
        except mysql.connector.Error as err:
            logger.error(f"Errore di connessione: {err}")
            if i < max_retries - 1:
                logger.info(f"Riprovo tra {delay} secondi...")
                time.sleep(delay)
    raise Exception("Impossibile connettersi al database dopo i tentativi massimi")

def ensure_database_exists():
    try:
        conn = wait_for_mysql()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        logger.info(f"Database '{DB_CONFIG['database']}' creato o già esistente.")
        conn.close()
    except Exception as e:
        logger.error(f"Errore durante la creazione del database: {e}")
        raise

def create_tables():
    try:
        ensure_database_exists()
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email VARCHAR(255) PRIMARY KEY,
                ticker VARCHAR(10) NOT NULL
            );
        """)
        logger.info("Tabella 'users' creata o già esistente.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ticker VARCHAR(10),
                value DECIMAL(10, 2),
                timestamp DATETIME
            );
        """)
        logger.info("Tabella 'stock_data' creata o già esistente.")

        conn.commit()
        logger.info("Database inizializzato con successo!")
    except Exception as e:
        logger.error(f"Errore durante la creazione delle tabelle: {e}")
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            logger.info("Connessione al database chiusa.")

if __name__ == "__main__":
    try:
        create_tables()
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        exit(1)
