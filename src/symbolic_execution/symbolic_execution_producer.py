from symbolic_execution.symbolic_execution_engine import SymbolicExecution
from kafka_handlers.producer import Producer
import threading

class SymbolicExecutionProducer:

     def __init__(self, symbolic_execution: SymbolicExecution, producer : Producer):
          self.symbolic_execution = symbolic_execution
          self.producer = producer

     def startProduce(self):
          threading.Thread(target=self.produceInputs).start()

     def produceInputs(self):
          generator = self.symbolic_execution.getTargetInput()
          while True and not self.symbolic_execution.stop:
               generated_input = next(generator)
               print("sending producer ", generated_input)
               self.producer.send(generated_input)

     def stopProduce(self):
          self.symbolic_execution.stopProcessing()