import random
import os


class BaseMutation:
    def __init__(self):
        pass

    @staticmethod
    def mutate(input_data: bytes) -> bytes:
        pass


class SimpleMutation(BaseMutation):
    def __init__(self):
        super().__init__()

    @staticmethod
    def mutate(input_data: bytes) -> bytes:
        index = random.randint(0, len(input_data))
        return input_data[:index] + os.urandom(4) + input_data[index + 1:]
