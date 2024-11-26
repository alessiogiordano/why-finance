#
#  wait_for_mysql.sh
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

set -e

echo "Starting wait_for_mysql script..."
echo "Environment variables:"
echo "DB_HOST: $DB_HOST"
echo "DB_USER: $DB_USER"
echo "DB_PASSWORD: $DB_PASSWORD"
echo "DB_NAME: $DB_NAME"

cat > check_mysql.py << EOF
import mysql.connector
import os
import time
import sys

print("Starting MySQL connection check...")

config = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'dsbd_homework1'),
    'port': int(os.getenv('DB_PORT', 3306))
}

print(f"Attempting to connect with config: {config}")

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        print(f"Attempt {retry_count + 1}/{max_retries}")
        conn = mysql.connector.connect(**config)
        conn.close()
        print("MySQL connection successful!")
        sys.exit(0)
    except mysql.connector.Error as err:
        print(f"MySQL Connection Error: {err}")
        retry_count += 1
        if retry_count < max_retries:
            print(f"Waiting 2 seconds before retry...")
            time.sleep(2)

print("Max retries reached. Exiting...")
sys.exit(1)
EOF

python check_mysql.py

if [ $? -eq 0 ]; then
    echo "MySQL is up - executing migration and starting data collector"
    
    echo "Running database migrations..."
    python migrations/create_table_stock_data_and_users.py
    
    echo "Starting data collector..."
    python data_collector.py
else
    echo "Failed to connect to MySQL after maximum retries"
    exit 1
fi