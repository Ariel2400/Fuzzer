
from typing import TypeVar, Generic
from enum import Enum


T = TypeVar('T')

class Endian(Enum):
    BIG = 0
    LITTLE = 1

class GrammarTemplate:
    def __init__(self, arrayOfGrammarValues:list):
        self.arrayOfGrammarValues = arrayOfGrammarValues

    def create_file(self, filename, path):
        pass

class GrammarType(Generic[T]):
    def __init__(self, random:bool, size:int, val:T, endian:Endian):
        self.random = random
        self.size = size
        self.val = val
        self.endian = endian

    def __init__(self, random:bool, size:int, val:T):
        self.random = random
        self.size = size
        self.val = val
        self.endian = None

    
