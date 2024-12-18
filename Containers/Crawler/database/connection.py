#
# Database configurations
#
import mysql.connector
import os
import time
from utils.logger import logger

def get_db_config(db_type):
    """
    Retrieve the database configuration based on the db_type parameter.
    """
    if db_type == 'user':
        return {
            "host": os.environ.get('USER_DB_HOST', 'mysql_user'),
            "user": os.environ.get('DB_USER', 'root'),
            "password": os.environ.get('DB_PASSWORD', 'root'),
            "database": os.environ.get('USER_DB_NAME', 'user_db'),
            "port": int(os.environ.get('DB_PORT', '3306'))
        }
    elif db_type == 'ticker':
        return {
            "host": os.environ.get('TICKER_DB_HOST', 'mysql_ticker'),
            "user": os.environ.get('DB_USER', 'root'),
            "password": os.environ.get('DB_PASSWORD', 'root'),
            "database": os.environ.get('TICKER_DB_NAME', 'ticker_db'),
            "port": int(os.environ.get('DB_PORT', '3306'))
        }
    else:
        raise ValueError("Invalid database type specified. Use 'user' or 'ticker'.")

def wait_for_mysql(db_type):
    while True:
        try:
            conn = connect_to_db(db_type)
            conn.close()
            logger.info(f"Connesso con successo al database {db_type}!")
            break
        except mysql.connector.Error as e:
            logger.info(f"In attesa del database {db_type}... Riprovo in 5 secondi.")
            time.sleep(5)

def connect_to_db(db_type):
    """
    Establish a connection to a MySQL database.
    """
    try:
        config = get_db_config(db_type)
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Database connection error for {config.get('database', 'unknown')}: {err}")
        raise Exception(f"Database connection error: {err}")