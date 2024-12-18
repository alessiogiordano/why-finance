import mysql.connector
from utils.logger import logger

USER_DB_CONFIG = {
    "host": "mysql_user",
    "user": "root",
    "password": "root",
    "database": "user_db",
    "port": 3306,
}

def connect_to_db(config):
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        logger.error(f"Errore di connessione al database: {err}")
        raise
