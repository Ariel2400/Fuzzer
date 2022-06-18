from kafka import KafkaConsumer
from typing import Dict
from json import loads


class Consumer:
    def __init__(self) -> None:
        self._consumer = KafkaConsumer('Samples', bootstrap_servers='localhost:9092', group_id=None, value_deserializer=lambda x: loads(x.decode('utf-8')))

    def get_batch(self, num_of_records) -> Dict:
        while True:
            b = self._consumer.poll(max_records=num_of_records)
            if b.values():
                return b
            else:
                continue




