from abc import ABC, abstractmethod

class AbstractBaseFileGenerator(ABC):

    @abstractmethod
    def generateData(self) -> bytearray:
        pass

    @abstractmethod
    def generateFile(self, path: str):
        pass