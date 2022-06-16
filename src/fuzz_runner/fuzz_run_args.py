import argparse

class FuzzRunArgs:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--target", help="specify target for fuzzing", required=True)
        self.parser.add_argument('--target_args', nargs='+', help="specify command line arguments of target", required=True)
        self.parser.add_argument("--crashes_dir_path", help="specify crashes_dir_path for fuzzing crashes", required=True)
        self.parser.add_argument("--fuzz_amount", help="fuzz amount of fuzzing", type=int)
        self.parser.add_argument("--threads_number", help="number of threads that will be fuzz in parallel", type=int)
        self.parser.add_argument("--snapshot_fuzzing_enable", help="use snapshot fuzzing", action="store_true")

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

    def getSnapshotFuzzingEnable(self):
        return self.args.snapshot_fuzzing_enable

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
        self.args, self.unknown = self.parser.parse_known_args()

    def getGrammarFilePath(self):
        return self.args.grammar_file_path

class SymbolicFuzzRunArgs(FuzzRunArgs):

    def __init__(self):
        super().__init__()
        self.args, self.unknown = self.parser.parse_known_args()