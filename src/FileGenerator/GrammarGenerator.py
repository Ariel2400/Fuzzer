from FileGenerator import AbstractBaseFileGenerator
from generation.GrammarTemplate import GrammarTemplate
import random
from mutation.mutations import Mutation3Choices
from typing import Union

class GrammarFileGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, grammar_file_path: str, json_schema_file_path: str, mutation_number: Union[int, None]):
        self.mutation_number = mutation_number
        self.grammar_file_path = grammar_file_path
        self.json_schema_file_path = json_schema_file_path
        self.grammar_template = GrammarTemplate(self.grammar_file_path, self.json_schema_file_path)
        self.mutator = Mutation3Choices()

    def generateData(self):
        data = bytearray(self.grammar_template.create_data())
        if self.mutation_number is not None:
            data = self.mutator.mutateCycles(data, self.mutation_number)

        return bytes(data)


    def generateFile(self, path: str):
        self.grammar_template.create_file(path)