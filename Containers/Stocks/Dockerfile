#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

FROM python:3.12

WORKDIR /why-finance/stocks

COPY Protos/.build .
COPY Sources .
COPY Containers/Stocks/ .
RUN mkdir ./logs
RUN touch ./logs/app.log

RUN pip install -r requirements.txt

EXPOSE 50052

CMD ["python", "main.py"]
