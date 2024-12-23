#
#  subscribe.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 21/12/24.
#

from os import environ # Environment Variables
from utils.logger import logger

#
# Kafka Event Stream
#
from confluent_kafka import Consumer
import json

# Format: 'host1:port1:port2,host2:port3'
bootstrap_servers = []
for element in environ.get('KAFKA_BROKERS', 'localhost:9092').split(","):
    component = element.split(":")
    if len(component) > 1:
        for i in range(1, len(component)):
            bootstrap_servers.append(component[0] + ":" + component[i])
#-----------------------------------------------------------------------------------------
# The number of bootstrap_servers is also used for num_partitions and replication_factor

# Format: 'topic1,topic2,topic3'
topics = environ.get('KAFKA_TOPICS', 'crawler,alert,notification-center').split(",")

def no_op(*kargs, **kwargs):
    pass
#-----------------------------------------------------------------------------------------

#             topics, options
def subscribe(*kargs, **kwargs):
    #
    should_log = True if ('log' in kwargs and kwargs['log'] == True) else False
    decode_json = True if ('json' in kwargs and kwargs['json'] == True) else False
    will_poll_consumer = kwargs['before'] if ('before' in kwargs and callable(kwargs['before'])) else no_op
    did_poll_consumer = kwargs['callback'] if ('callback' in kwargs and callable(kwargs['callback'])) else no_op
    failed_polling_consumer = kwargs['error'] if ('error' in kwargs and callable(kwargs['error'])) else no_op
    #
    polling_interval = float(environ.get('KAFKA_POLLING_INTERVAL', '1.0')) # Blocks up to 1s
    group_id = kwargs['group_id'] if ('group_id' in kwargs) else environ.get('KAFKA_GROUP_ID', 'test-consumer-group')
    consumer = Consumer({ 'bootstrap.servers': ','.join(bootstrap_servers), 'group.id': group_id })
    logger.info(f"TOPICS: '{environ.get('KAFKA_TOPICS', 'crawler,alert,notification-center')}'")
    consumer.subscribe(topics if len(kargs) == 0 else kargs)
    while True:
        try:
            will_poll_consumer()
        except Exception as e:
            logger.error(f"{e}")
            pass
        message = consumer.poll(polling_interval) # Blocks up to 'polling_interval' seconds
        if message is not None:
            error = message.error()
            if error:
                failed_polling_consumer(error)
                if should_log:
                    logger.error(f"KAFKA ERROR: '{error}' in '{group_id}' consumer")
                continue
            if should_log:
                logger.info(f"KAFKA RECEIVED: '{message.topic()}', partition {message.partition()}, offset {message.offset()}")
            try:
                if decode_json:
                    did_poll_consumer(json.loads(message.value().decode('utf-8')))
                else:
                    did_poll_consumer(message.value().decode('utf-8'))
            except Exception as e:
                logger.error(f"{e}")
                pass
#-----------------------------------------------------------------------------------------