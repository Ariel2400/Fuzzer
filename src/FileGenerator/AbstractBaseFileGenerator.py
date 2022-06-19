from abc import ABC, abstractmethod

class AbstractBaseFileGenerator(ABC):

    @abstractmethod
    def generateData(self) -> bytes:
        pass

    @abstractmethod
    def generateFile(self, path: str):
        pass