from abc import ABC, abstractmethod

class AbstractBaseFileGenerator(ABC):
    
    def __init__(self, generated_files_path):
        self.generated_files_path = generated_files_path


    @abstractmethod
    def generateFile(self):
        pass

    @abstractmethod
    def generateData(self):
        pass