#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

FROM python:3.12

WORKDIR /why-finance/crawler

COPY . .
RUN mkdir ./logs
RUN touch ./logs/app.log


RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./crawler.py"]
