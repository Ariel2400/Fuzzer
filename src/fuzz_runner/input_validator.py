from src.common.consts import FuzzTypes
import os

class Validator:

    @staticmethod
    def isValidFuzzType(fuzzType: str):
        return fuzzType in [fuzz_Type.value for fuzz_Type in FuzzTypes]

    @staticmethod
    def isMutationParamsValid(params: list):
        if len(params) < 3:
            assert Exception("not enuogh parameters")

        sample_dir_path = params[0]
        target = params[1]
        fuzz_amount = params[2]
        if not os.path.exists(sample_dir_path):
            assert Exception("sample file dir does not exist")
        if not os.path.exists(target):
            assert Exception("target does not exist")
        if not fuzz_amount.isnumeric():
            assert Exception("fuzz_amount not a number")
        if fuzz_amount < 0:
            assert Exception("fuzz amount should be positive")
        return True




    @staticmethod
    def isGenarationParamsValid(params: list):
        if len(params) < 3:
            assert Exception("not enuogh parameters")

        grammar_file_path = params[0]
        target = params[1]
        fuzz_amount = params[2]
        if not os.path.exists(grammar_file_path):
            assert Exception("grammar file path does not exist")
        if not os.path.exists(target):
            assert Exception("target does not exist")
        if not fuzz_amount.isnumeric():
            assert Exception("fuzz_amount not a number")
        if fuzz_amount < 0:
            assert Exception("fuzz amount should be positive")
        return True


    @staticmethod
    def isSymbolicExecutionParamsValid(params: list):
        if len(params) < 2:
            assert Exception("not enuogh parameters")

        target = params[0]
        fuzz_amount = params[1]
        if not os.path.exists(target):
            assert Exception("target does not exist")
        if not fuzz_amount.isnumeric():
            assert Exception("fuzz_amount not a number")
        if fuzz_amount < 0:
            assert Exception("fuzz amount should be positive")

        return True