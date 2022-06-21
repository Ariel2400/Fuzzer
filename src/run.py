import sys
from fuzz_runner.input_validator import Validator
from fuzz_runner.fuzz_run_args import MutationFuzzRunArgs, GenerationFuzzRunArgs, SymbolicFuzzRunArgs
from mutation.mutations import SimpleMutation
from FileGenerator.MutationGenerator import MutationFileGenerator
from FileGenerator.GrammarGenerator import GrammarFileGenerator
from fuzzer.fuzzing import Fuzzer
from symbolic_execution.symbolic_execution import SymbolicExecution
from symbolic_execution.symbolic_execution import SymbolicExecutionProperties
from kafka_handlers.producer import Producer
from symbolic_execution.symbolic_execution_producer import SymbolicExecutionProducer
from FileGenerator.SymbolicExecutionGenerator import SymbolicExecutionGenerator

def main():

    if len(sys.argv) < 2:
        raise Exception("fuzz type not specify(mutation, generation, symbolic_execution)")


    command_line_args = sys.argv[1:]
    fuzz_type = command_line_args[0]
    file_generator = None
    fuzz_run_args = None

    if not Validator.isValidFuzzType(fuzz_type):
        raise Exception("fuzz type not valid(mutation, generation, symbolic_execution)")

    if fuzz_type == "mutation":
        fuzz_run_args = MutationFuzzRunArgs()
        file_generator = MutationFileGenerator(fuzz_run_args.getSampleDirPath(), SimpleMutation())
    elif fuzz_type == "generation":
        fuzz_run_args = GenerationFuzzRunArgs()
        schema_path = "./src/generation/grammar-schema.json"
        file_generator = GrammarFileGenerator(fuzz_run_args.getGrammarFilePath(), schema_path, fuzz_run_args.getMutation())
    elif fuzz_type == "symbolic_execution":
        fuzz_run_args = SymbolicFuzzRunArgs()
        symbolicExecutionProperties = SymbolicExecutionProperties(fuzz_run_args.getLenSymbolicBytes(), fuzz_run_args.getLoadDynamicLibaries())
        symbolicExecutionEngine = SymbolicExecution(symbolicExecutionProperties, fuzz_run_args.getTarget(), fuzz_run_args.getTargetArgs())
        kafkaProducer = Producer()
        symbolicExecutionProducer = SymbolicExecutionProducer(symbolicExecutionEngine, kafkaProducer)
        symbolicExecutionProducer.startProduce()
        file_generator = SymbolicExecutionGenerator()


    fuzzer = Fuzzer(file_generator, fuzz_run_args.getCrashesDirPath())
    fuzzer.fuzz_worker([fuzz_run_args.getTarget()] + fuzz_run_args.getTargetArgs(), fuzz_run_args.getFuzzAmount(), fuzz_run_args.getThreadsNumber())

if __name__ == '__main__':
    main()