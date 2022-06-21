from dataclasses import dataclass
from kafka import KafkaProducer
from json import dumps
import subprocess as sp
import logging
import time
producer_logger = logging.getLogger('Kafka Producer')
class Producer:
    def __init__(self) -> None:
        self._producer = KafkaProducer(bootstrap_servers="localhost:9092", api_version=(20, 2, 1))

    
    def close(self) -> None:
        self._producer.flush()
        self._producer.close()
    
    def send(self, object: bytes) -> None:
        self._producer.send('Samples', object)
