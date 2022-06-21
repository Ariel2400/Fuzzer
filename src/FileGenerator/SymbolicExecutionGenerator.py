from FileGenerator import AbstractBaseFileGenerator
from kafka_handlers.consumer import Consumer
from symbolic_execution.symbolic_execution_producer import SymbolicExecutionProducer
from symbolic_execution.symbolic_execution_engine import SymbolicExecution
from typing import Union

class SymbolicExecutionGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, symbolic_execution_producer: Union[SymbolicExecutionProducer, None], symbolic_execution_engine: Union[SymbolicExecution, None]):
        self.symbolic_execution_producer = symbolic_execution_producer
        self.stop_generator = False
        self.symbolic_execution_engine = symbolic_execution_engine
        if symbolic_execution_producer is not None:
            self.consumer = Consumer()
        if symbolic_execution_engine is not None:
            self.generator = self.symbolic_execution_engine.getTargetInput()
  
    def generateData(self) -> bytes:
        if self.stop_generator:
            raise Exception("tried to generate data after stopping")
        if self.symbolic_execution_producer is not None:
            batches = self.consumer.get_batch(1)
            data = list(batches.values())[0][0].value
        else:
            data = next(self.generator)
        return data

    def generateFile(self, path: str):
        inputData = bytes(self.generateData())
        fileObj = open(path, "wb")
        fileObj.write(inputData)
        fileObj.close()

    def close(self):
        self.stop_generator = True
        if self.symbolic_execution_producer is not None:
            self.symbolic_execution_producer.stopProduce()
