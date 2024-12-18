from kafka import KafkaProducer
import json
from utils.logger import logger

kafka_port = None #TODO: configurare kafka

class KafkaProducerService:
    def __init__(self, bootstrap_servers=kafka_port):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        try:
            self.producer.send(topic, message)
            logger.info(f"Messaggio inviato al topic Kafka '{topic}': {message}")
        except Exception as e:
            logger.error(f"Errore nell'invio del messaggio Kafka: {e}")
