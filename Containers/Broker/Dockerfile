#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 15/12/24.
#

FROM alpine:latest

WORKDIR /why-finance/broker

COPY Protos/.build .
COPY Sources .
COPY Containers/Broker/ .
RUN mkdir ./logs
RUN touch ./logs/app.log

RUN apk update
RUN apk upgrade
RUN apk add python3 py3-pip
# beware that 'kafka-python' is not maintained anymore
RUN pip3 install kafka-python --break-system-packages

ENTRYPOINT [ "python3", "init.py" ]