#
#  Dockerfile
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Luca Montera on 24/11/24.
#

FROM python:3.12

WORKDIR /why-finance/users

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir ./logs
RUN touch ./logs/app.log

EXPOSE 50051

CMD ["python", "user.py"]
