import mysql.connector
from dotenv import load_dotenv

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT"))
}

def connect_to_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def insert_test_data():

    test_users = [
        ("user1@example.com", "AAPL"),
        ("user2@example.com", "GOOGL"),
        ("user3@example.com", "MSFT"),
        ("user4@example.com", "TSLA"),
        ("user5@example.com", "AMZN")
    ]

    conn = connect_to_db()
    cursor = conn.cursor()

    for email, ticker in test_users:
        try:
            cursor.execute("INSERT INTO users (email, ticker) VALUES (%s, %s)", (email, ticker))
            print(f"Inserito utente: {email} con ticker: {ticker}")
        except mysql.connector.IntegrityError:
            print(f"Utente {email} già esistente, salto l'inserimento.")

    conn.commit()
    conn.close()
    print("Dati di test inseriti con successo.")

if __name__ == "__main__":
    insert_test_data()
