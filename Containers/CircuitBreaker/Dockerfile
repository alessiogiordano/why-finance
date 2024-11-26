#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 23/11/24.
#

FROM alpine:latest

WORKDIR /why-finance/circuit-breaker

COPY . .
RUN mkdir ./logs
RUN touch ./logs/app.log

RUN apk update
RUN apk upgrade
RUN apk add python3 py3-pip py3-grpcio
RUN pip3 install -r requirements.txt --break-system-packages

ENTRYPOINT [ "python3", "main.py"]