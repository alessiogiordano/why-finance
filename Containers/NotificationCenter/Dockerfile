#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/12/24.
#

FROM alpine:latest

WORKDIR /why-finance/notification-center

COPY Protos/.build .
COPY Sources .
COPY Containers/NotificationCenter/ .
RUN mkdir ./logs
RUN touch ./logs/app.log

RUN apk update
RUN apk upgrade
RUN apk add python3 py3-pip
# Because of lack of gcc in Alpine, confluent-kafka has to be installed separately
RUN apk add py3-confluent-kafka --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing
RUN pip3 install -r requirements.txt --break-system-packages

ENTRYPOINT [ "python3", "main.py"]