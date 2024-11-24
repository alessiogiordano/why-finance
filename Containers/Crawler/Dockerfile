FROM python:3.12

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x wait_for_mysql.sh

#CMD ["./wait_for_mysql.sh"] 
#ENTRYPOINT ["python", "./migrations/create_table_stock_data_and_users.py", "./migrations/test_user_data_seeder.py", "crawler.py"]
ENTRYPOINT ["python", "./crawler.py"]
