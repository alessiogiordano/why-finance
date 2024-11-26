#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 25/11/24.
#

FROM alpine:latest

WORKDIR /why-finance/database

COPY . .
RUN mkdir ./logs
RUN touch ./logs/app.log

RUN apk update
RUN apk upgrade
RUN apk add python3 py3-pip
# In order to reuse an existing Python script of ours, we query the database through the Python connector
RUN pip3 install mysql-connector-python --break-system-packages

ENTRYPOINT [ "python3", "create_tables.py" ]