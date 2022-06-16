from FileGenerator import AbstractBaseFileGenerator
from generation.GrammarTemplate import GrammarTemplate

class GrammarFileGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, grammar_file_path: str, json_schema_file_path: str):
        self.grammar_file_path = grammar_file_path
        self.json_schema_file_path = json_schema_file_path
        self.grammar_template = GrammarTemplate(self.grammar_file_path, self.json_schema_file_path)

    def generateData(self):
        return self.grammar_template.create_data()


    def generateFile(self, path: str):
        self.grammar_template.create_file(path)