from src.FileGenerator import AbstractBaseFileGenerator
from src.generation.GrammarTemplate import GrammarTemplate

class GrammarGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, grammar_file_path: str, json_schema_file_path: str):
        self.grammar_file_path = grammar_file_path
        self.grammar_template = GrammarTemplate.createGrammarTemplateFromFile(grammar_file_path, json_schema_file_path)


    def generateFile(self, path: str):
        self.grammar_template.create_file(path)