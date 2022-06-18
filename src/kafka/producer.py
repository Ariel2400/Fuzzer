from dataclasses import dataclass
from kafka import KafkaProducer
from json import dumps
import subprocess as sp
import logging

producer_logger = logging.getLogger('Kafka Producer')
class Producer:
    def __init__(self) -> None:
        
        p_zoo = sp.run('bin/zookeeper-server-start.sh config/zookeeper.properties')
        p_server = sp.run('./kafka_2.13-3.1.1/bin/kafka-server-start.sh ./kafka_2.13-3.1.1/config/server.properties')
        if p_zoo.returncode != 0:
            producer_logger.critical(f"Couldn't start zookeeper:\n{p_zoo.stdout if p_zoo.stdout else p_zoo.stderr}")
        if p_server.returncode != 0:
            producer_logger.critical(f"Couldn't start server:\n{p_server.stdout if p_server.stdout else p_server.stderr}")
        self._producer = KafkaProducer(bootstrap_servers="localhost:9092")

    
    def close(self) -> None:
        self._producer.flush()
        self._producer.close()
    
    def send_file(self, object: bytes) -> None:
        self._producer.send('Samples', object)
