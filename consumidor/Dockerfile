FROM python:3.10-slim

WORKDIR /app

COPY subscribe.py .

RUN pip install paho-mqtt mysql-connector-python

CMD ["python", "subscribe.py"]

