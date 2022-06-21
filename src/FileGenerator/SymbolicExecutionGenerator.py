from FileGenerator import AbstractBaseFileGenerator
from kafka_handlers.consumer import Consumer

class SymbolicExecutionGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self):
        self.consumer = Consumer()
  
    def generateData(self) -> bytes:
        batches = self.consumer.get_batch(1)
        print("batches = ", batches)
        data = list(batches.values())[0][0].value
        return data

    def generateFile(self, path: str):
        inputData = bytes(self.generateData())
        fileObj = open(path, "wb")
        fileObj.write(inputData)
        fileObj.close()