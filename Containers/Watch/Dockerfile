FROM python:3.12

WORKDIR ./

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 50052

CMD ["python", "watch.py"]
