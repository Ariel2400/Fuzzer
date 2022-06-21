import argparse

class FuzzRunArgs:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--target", help="specify target for fuzzing", required=True)
        self.parser.add_argument('--target_args', nargs='+', help="specify command line arguments of target", required=True)
        self.parser.add_argument("--crashes_dir_path", help="specify crashes_dir_path for fuzzing crashes", required=True)
        self.parser.add_argument("--fuzz_amount", help="fuzz amount of fuzzing", type=int)
        self.parser.add_argument("--threads_number", help="number of threads that will be fuzz in parallel", type=int)
        self.parser.add_argument("--stdin_input", help="throw input to target's stdin instead as a file argument", action="store_true")

    def getTarget(self):
        return self.args.target

    def getTargetArgs(self):
        return self.args.target_args

    def getCrashesDirPath(self):
        return self.args.crashes_dir_path

    def getFuzzAmount(self):
        return self.args.fuzz_amount

    def getThreadsNumber(self):
        return self.args.threads_number

    def getStdinInput(self):
        return self.args.stdin_input

class MutationFuzzRunArgs(FuzzRunArgs):

    def __init__(self):
        super().__init__()
        self.parser.add_argument("--sample_dir_path", help="sample_dir_path for samples mutation", required=True)
        self.args, self.unknown = self.parser.parse_known_args()

    def getSampleDirPath(self):
        return self.args.sample_dir_path

class GenerationFuzzRunArgs(FuzzRunArgs):

    def __init__(self):
        super().__init__()
        self.parser.add_argument("--grammar_file_path", help="grammar_file_path for generate samples", required=True)
        self.parser.add_argument("--mutation_number", help="do mutation_number number of mutation after generation", type=int)
        self.args, self.unknown = self.parser.parse_known_args()

    def getGrammarFilePath(self):
        return self.args.grammar_file_path

    def getMutation(self):
        return int(self.args.mutation_number)
        
class SymbolicFuzzRunArgs(FuzzRunArgs):

    def __init__(self):
        super().__init__()
        self.parser.add_argument("--len_symbolic_bytes", help="len_symbolic_bytes for target input len symbolic bytes", required=True, type=int)
        self.parser.add_argument("--load_dynamic_libaries", help="load dynamic libaries for symbolic execution", action="store_true")
        self.parser.add_argument("--use_kafka", help="use kafka for delivering messages to fuzzer", action="store_true")
        self.args, self.unknown = self.parser.parse_known_args()

    def getLenSymbolicBytes(self):
        return self.args.len_symbolic_bytes

    def getLoadDynamicLibaries(self):
        return self.args.load_dynamic_libaries

    def getUseKafka(self):
        return self.args.use_kafka
