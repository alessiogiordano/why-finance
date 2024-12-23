#
#  broadcast.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 20/12/24.
#

from os import environ # Environment Variables
from utils.logger import logger

#
# Kafka Event Stream
#
from confluent_kafka import Producer
import json

# Format: 'host1:port1:port2,host2:port3'
bootstrap_servers = []
for element in environ.get('KAFKA_BROKERS', 'localhost:9092').split(","):
    component = element.split(":")
    if len(component) > 1:
        for i in range(1, len(component)):
            bootstrap_servers.append(component[0] + ":" + component[i])
#-----------------------------------------------------------------------------------------

# Default values from: https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html
KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': ','.join(bootstrap_servers),
    'acks': str(environ.get('KAFKA_ACKS', 'all')),  # 'all', '1'
    'max.in.flight.requests.per.connection': int(environ.get('KAFKA_IN_FLIGHT_REQUESTS', '5')), # Default value, ordering is not a concern -- set to '1' to ensure ordering of messages
    'batch.size': int(environ.get('KAFKA_BATCH_SIZE', '16384')),
    'linger.ms': int(environ.get('KAFKA_LINGER', '0')),
    'retries': int(environ.get('KAFKA_RETRIES', '2147483647'))
}

kafka_producer = Producer(KAFKA_PRODUCER_CONFIG)

def kafka_log(error, message):
    if error:
        logger.info(f"KAFKA ERROR: '{kafka_topic}' {error}")
    else:
        logger.info(f"KAFKA DELIVERED: '{message.topic()}', partition {message.partition()}, offset {message.offset()}")
#-----------------------------------------------------------------------------------------

def broadcast(topic, payload, callback = None):
    value = None
    if payload is None:
        return
    if type(payload) is str:
        value = payload
    elif (type(payload) is int) or (type(payload) is float):
        value = str(payload)
    else:
        value = json.dumps(payload)
    kafka_producer.produce(topic,
                           key=None, # Round Robin distribution across partitions
                           value=value,
                           callback=callback if callable(callback) else kafka_log)
    kafka_producer.flush()
#-----------------------------------------------------------------------------------------