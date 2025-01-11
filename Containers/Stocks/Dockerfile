#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

FROM alpine:latest

WORKDIR /why-finance/stocks

COPY Protos/.build .
COPY Sources .
COPY Containers/Stocks/ .
RUN mkdir ./logs
RUN touch ./logs/app.log

RUN apk update
RUN apk upgrade
RUN apk add python3 py3-pip py3-grpcio
RUN pip3 install -r requirements.txt --break-system-packages

CMD [ "python3", "main.py" ]
