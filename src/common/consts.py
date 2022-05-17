import enum

class FuzzTypes(enum.Enum):
    mutation = 1
    generation = 2
    symbolic_execution = 3