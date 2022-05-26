import enum

class FuzzTypes(enum.Enum):
    mutation = "mutation"
    generation = "generation"
    symbolic_execution = "symbolic_execution"