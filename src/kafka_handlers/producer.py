from dataclasses import dataclass
from kafka import KafkaProducer
from json import dumps
import subprocess as sp
import logging
import time
producer_logger = logging.getLogger('Kafka Producer')
class Producer:
    def __init__(self) -> None:
        
        with open("./ZOOKEEPER_LOG", "w") as f:
            p_zoo = sp.Popen('./kafka_2.13-3.2.0/bin/zookeeper-server-start.sh ./kafka_2.13-3.2.0/config/zookeeper.properties', shell=True, stdout=f)
        time.sleep(20)
        with open("./SERVER_LOG", "w") as a:
            p_server = sp.Popen('./kafka_2.13-3.2.0/bin/kafka-server-start.sh ./kafka_2.13-3.2.0/config/server.properties', shell=True, stdout=a)
        if p_zoo.returncode != 0:
            producer_logger.critical(f"Couldn't start zookeeper:\n{p_zoo.stdout if p_zoo.stdout else p_zoo.stderr}")
        if p_server.returncode != 0:
            producer_logger.critical(f"Couldn't start server:\n{p_server.stdout if p_server.stdout else p_server.stderr}")
        self._producer = KafkaProducer(bootstrap_servers="localhost:9092", api_version=(20, 2, 1))

    
    def close(self) -> None:
        self._producer.flush()
        self._producer.close()
    
    def send(self, object: bytes) -> None:
        self._producer.send('Samples', object)
