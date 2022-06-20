import random
import os


class BaseMutation:
    def __init__(self):
        pass

    
    def mutate(self, input_data: bytearray) -> bytearray:
        print("aaaa")
        pass


class SimpleMutation(BaseMutation):
    def __init__(self):
        super().__init__()

    
    def mutate(self, input_data: bytearray) -> bytearray:
        index = random.randint(0, len(input_data) - 1)
        input_data[index] = random.randint(0, 255)
        return input_data


class Mutation3Choices(BaseMutation):
    def __init__(self):
        super().__init__()

    
    def delete_byte(self, input_data: bytearray, index: int) -> bytearray:
        if index == len(input_data):
            index = random.randint(0, len(input_data)-1)
        return input_data[:index]+input_data[index+1:]

    
    def insert_byte(self, input_data: bytearray, index: int) -> bytearray:
        random_byte = os.urandom(1)
        return input_data[:index] + random_byte + input_data[index:]

    
    def flip_byte(self, input_data: bytearray, index: int) -> bytearray:
        random_byte = os.urandom(1)
        return input_data[:index] + random_byte + input_data[index+1:]

    
    def mutate(self, input_data: bytearray) -> bytearray:
        choices = [
            Mutation3Choices.delete_byte,
            Mutation3Choices.insert_byte,
            Mutation3Choices.flip_byte,
        ]

        selected_mutator = random.choice(choices)
        index = random.randint(0, len(input_data) - 1)
        return selected_mutator(self, input_data, index)


    def mutateCycles(self, input_data: bytearray, cycles: int) -> bytearray:
        for _ in range(cycles):
            input_data = self.mutate(input_data)
        return input_data
