#
#  create_tables.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

from os import environ # Environment Variables
import mysql.connector
import time

DB_CONFIG = {
    "host": environ.get('DB_HOST', 'mysql'),
    "user": environ.get('DB_USER', 'root'),
    "password": environ.get('DB_PASSWORD', 'root'),
    "database": environ.get('DB_NAME', 'dsbd_homework1'),
    "port": int(environ.get('DB_PORT', '3306'))
}

def wait_for_mysql(max_retries=30, delay=2):
    for i in range(max_retries):
        try:
            print(f"Tentativo di connessione a MySQL {i+1}/{max_retries}")
            conn = mysql.connector.connect(**DB_CONFIG)
            print("Connessione a MySQL stabilita con successo!")
            return conn
        except mysql.connector.Error as err:
            print(f"Errore di connessione: {err}")
            if i < max_retries - 1:
                print(f"Riprovo tra {delay} secondi...")
                time.sleep(delay)
    raise Exception("Impossibile connettersi al database dopo i tentativi massimi")

def create_tables():
    try:
        conn = wait_for_mysql()
        cursor = conn.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email VARCHAR(255) PRIMARY KEY,
                ticker VARCHAR(10) NOT NULL
            );
        """)
        print("Tabella 'users' creata o già esistente.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ticker VARCHAR(10),
                value DECIMAL(10, 2),
                timestamp DATETIME
            );
        """)
        print("Tabella 'stocks' creata o già esistente.")

        conn.commit()
        print("Database inizializzato con successo!")

    except Exception as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Connessione al database chiusa.")


if __name__ == "__main__":
    try:
        create_tables()
    except Exception as e:
        print(f"Errore fatale: {e}")
        exit(1)