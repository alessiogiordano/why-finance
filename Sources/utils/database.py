#
#  database.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 18/12/24.
#

import mysql.connector
from utils.logger import logger
import os

def get_db_config_by_string(db_type):
    """
    Retrieve the database configuration based on the db_type parameter.
    """
    if db_type == 'users':
        return {
            "host": os.environ.get('USERS_DB_HOST', 'users-database'),
            "port": int(os.environ.get('USERS_DB_PORT', '3306')),
            "user": os.environ.get('USERS_DB_USER', 'root'),
            "password": os.environ.get('USERS_DB_PASSWORD', 'root'),
            "database": os.environ.get('USERS_DB_NAME', 'whyfinance_users')
        }
    elif db_type == 'stocks':
        return {
            "host": os.environ.get('STOCKS_DB_HOST', 'stocks-database'),
            "port": int(os.environ.get('STOCKS_DB_PORT', '3306')),
            "user": os.environ.get('STOCKS_DB_USER', 'root'),
            "password": os.environ.get('STOCKS_DB_PASSWORD', 'root'),
            "database": os.environ.get('STOCKS_DB_NAME', 'whyfinance_stocks')
        }
    elif db_type is None:
        return {
            "host": os.environ.get('DB_HOST', 'database'),
            "port": int(os.environ.get('DB_PORT', '3306')),
            "user": os.environ.get('DB_USER', 'root'),
            "password": os.environ.get('DB_PASSWORD', 'root'),
            "database": os.environ.get('DB_NAME', 'whyfinance')
        }
    else:
        raise ValueError("Invalid database type specified. Provide 'users' or 'stocks'.")
#-----------------------------------------------------------------------------------------

def get_db_config(target = None):
    configuration = None
    if type(target) is dict:
        configuration = target
    elif (type(target) is str) or (target is None):
        configuration = get_db_config_by_string(target)
    else:
        raise ValueError("Invalid database configuration.")
    return configuration
#-----------------------------------------------------------------------------------------

# 'wait_for_mysql' and 'connect_to_db' are merged as one
def connect(target = None, max_retries=1, delay=0, log=False):
    """
    Establish a connection to a MySQL database.
    """
    try:
        configuration = get_db_config(target)
        for i in range(max_retries):
            try:
                if (max_retries > 1) and (log):
                    logger.info(f"CONNECTION ATTEMPT {i+1}/{max_retries}\t{configuration['host']}")
                conn = mysql.connector.connect(**configuration)
                if log:
                    logger.info(f"CONNECTED TO\t{configuration['host']}")
                return conn
            except mysql.connector.Error as err:
                logger.error(f"MYSQL CONNECTION ERROR: {err}")
                if i < max_retries - 1:
                    logger.info(f"WILL RETRY IN {delay} SECONDS")
                    time.sleep(delay)
        raise Exception(f"UNABLE TO CONNECT TO {configuration['host']}")
    except ValueError as err:
        logger.error(str(err))
        raise err # rethrows
    except:
        logger.error(str(err))
        raise err # rethrows
#-----------------------------------------------------------------------------------------

#                                      SQL queries
def initialize_database(target = None, *kargs):
    try:
        configuration = get_db_config(target)
        conn = connect(configuration)
        # Create database if it does not exist already
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {configuration['database']}")
        logger.info(f"DATABASE '{configuration['database']}' CREATED OR ALREADY IN PLACE")
        # Create tables if they do not exist already
        for query in kargs:
            cursor.execute(query)
        if len(kargs) > 0:
            logger.info(f"{len(kargs)} TABLE(S) CREATED OR ALREADY IN PLACE")
        else:
            logger.info("NO TABLE WAS PROVIDED AS ARGUMENT IN *kargs")
        conn.commit()
        logger.info("DATABASE '{configuration['database']}' INITIALIZED")
    except Exception as err:
        logger.error(f"ERROR DURING INITIALIZATION OF {configuration['database']}: {err}")
        raise err
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
#-----------------------------------------------------------------------------------------