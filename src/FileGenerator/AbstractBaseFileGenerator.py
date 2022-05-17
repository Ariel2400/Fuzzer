from abc import ABC, abstractmethod

class AbstractBaseFileGenerator(ABC):

    @abstractmethod
    def generateFile(self, path: str):
        pass