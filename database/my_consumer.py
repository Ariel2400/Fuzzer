from kafka import KafkaConsumer
from typing import Dict
from json import loads


class MyConsumer:
    def __init__(self) -> None:
        self._consumer = KafkaConsumer('JSON Samples', bootstrap_servers='localhost:9092', group_id=None, value_deserializer=lambda x: loads(x.decode('utf-8')))

    def get_batch(self) -> Dict:
        return self._consumer.poll(max_records=10)

