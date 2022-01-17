from typing import TypeVar, Generic

T = TypeVar('T')


class GrammarTemplate:
    def __init__(self, arrayOfGrammarValues:list):
        self.arrayOfGrammarValues = arrayOfGrammarValues

    def create_file(self, filename, path):
        pass

class GrammarType(Generic[T]):
    def __init__(self, random:bool, size:int, val:T):
        self.random = random
        self.size = size
        self.val = val

    
