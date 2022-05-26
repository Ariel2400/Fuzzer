from kafka import KafkaConsumer
from json import loads


class MyConsumer:
    def __init__(self) -> None:
        self._consumer = KafkaConsumer('JSON Samples', bootstrap_servers='localhost:9092', group_id=None, )