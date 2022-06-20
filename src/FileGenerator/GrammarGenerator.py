from FileGenerator import AbstractBaseFileGenerator
from generation.GrammarTemplate import GrammarTemplate
import random
from mutation.mutations import Mutation3Choices
class GrammarFileGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, grammar_file_path: str, json_schema_file_path: str, useMutation: bool):
        self.useMutation = useMutation
        self.grammar_file_path = grammar_file_path
        self.json_schema_file_path = json_schema_file_path
        self.grammar_template = GrammarTemplate(self.grammar_file_path, self.json_schema_file_path)
        self.mutator = Mutation3Choices()

    def generateData(self):
        data = bytearray(self.grammar_template.create_data())
        if(self.useMutation):
            cyclesOfMutation = random.randint(0, len(data)//2)
            data = self.mutator.mutateCycles(data, cyclesOfMutation)

        return bytes(data)


    def generateFile(self, path: str):
        self.grammar_template.create_file(path)