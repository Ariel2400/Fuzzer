from file_by_template import GrammarTemplate
import sys
import os


NUM_OF_FILES = 100_000
if __name__ == '__main__':
    grammar_path, target_dir = sys.argv[1], sys.argv[2]
    template_creator = GrammarTemplate(GrammarTemplate.createGrammarTemplateFromFile(grammar_path))

    if not os.path.exists(os.path.abspath(target_dir)):
        os.mkdir(os.path.abspath(target_dir))

    for i in range(NUM_OF_FILES):
        template_creator.create_file(os.path.join(os.path.abspath(target_dir), f'target_#{i}'))


