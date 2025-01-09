#
#  init.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 15/12/24.
#

#
# Fix: ModuleNotFoundError: No module named 'kafka.vendor.six.moves'
# From: https://stackoverflow.com/questions/77287622/modulenotfounderror-no-module-named-kafka-vendor-six-moves-in-dockerized-djan
#
import sys, types
m = types.ModuleType('kafka.vendor.six.moves', 'Mock module')
setattr(m, 'range', range)
sys.modules['kafka.vendor.six.moves'] = m

from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
from os import environ # Environment Variables
from utils.logger import logger

#
# Configuration
#

# Format: 'host1:port1:port2,host2:port3'
bootstrap_servers = []
for element in environ.get('KAFKA_BROKERS', 'localhost:9092').split(","):
    component = element.split(":")
    if len(component) > 1:
        for i in range(1, len(component)):
            bootstrap_servers.append(component[0] + ":" + component[i])
# The number of bootstrap_servers is also used for num_partitions and replication_factor

# Format: 'topic1,topic2,topic3'
topics = environ.get('KAFKA_TOPICS', 'crawler,alert,notification_center').split(",")

if __name__ == "__main__":
    administrator = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id='create_topics')
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
    logger.info(f"CONNECTED TO BROKER TO CREATE TOPICS")
    new_topics = []
    current_topics = consumer.topics()
    for topic in current_topics:
        logger.info(f"TOPIC ALREADY EXISTS: {topic}")
    for topic in topics:
        if topic not in current_topics:
            new_topics.append(NewTopic(
                name=topic,
                num_partitions=len(bootstrap_servers),
                replication_factor=len(bootstrap_servers)
            ))
    error = None
    if len(new_topics) > 0:
        try: administrator.create_topics(new_topics=new_topics, validate_only=False)
        except Exception as e: error = e
    consumer.close()
    administrator.close()
    if error is not None:
        logger.error(f"Error while initializing Kafka topics")
        raise error
    logger.info(f"CREATED {len(new_topics)} KAFKA TOPICS")