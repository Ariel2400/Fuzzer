from FileGenerator import AbstractBaseFileGenerator
from kafka_handlers.consumer import Consumer
from symbolic_execution.symbolic_execution_producer import SymbolicExecutionProducer

class SymbolicExecutionGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, symbolic_execution_producer: SymbolicExecutionProducer):
        self.consumer = Consumer()
        self.symbolic_execution_producer = symbolic_execution_producer
  
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

    def close(self):
        self.symbolic_execution_producer.stopProduce()
