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
        return input_data[:index] + os.urandom(1) + input_data[index + 1:]


class Mutation3Choices(BaseMutation):
    def __init__(self):
        super().__init__()

    @staticmethod
    def delete_byte(input_data: bytes, index: int) -> bytes:
        if index == len(input_data):
            index = random.randint(0, len(input_data)-1)
        return input_data[:index]+input_data[index+1:]

    @staticmethod
    def insert_byte(input_data: bytes, index: int) -> bytes:
        random_byte = os.urandom(1)
        return input_data[:index] + random_byte + input_data[index:]

    @staticmethod
    def flip_byte(input_data: bytes, index: int) -> bytes:
        random_byte = os.urandom(1)
        return input_data[:index] + random_byte + input_data[index+1:]

    @staticmethod
    def mutate(input_data: bytes) -> bytes:
        choices = [
            Mutation3Choices.delete_byte,
            Mutation3Choices.insert_byte,
            Mutation3Choices.flip_byte,
        ]

        selected_mutator = random.choice(choices)
        index = random.randint(0, len(input_data))
        return selected_mutator(input_data, index)
