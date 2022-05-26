import subprocess
import os
import hashlib
import time
import threading
import logging
from src.FileGenerator.AbstractBaseFileGenerator import AbstractBaseFileGenerator
from typing import Union

class Fuzzer:
    def __init__(self, file_generator: AbstractBaseFileGenerator, crashes_dir_path):
        self.file_generator = file_generator
        self.crashes_dir_path = crashes_dir_path
        self.logger = logging.getLogger('Fuzzer info')
        self.amount_of_fuzzings = 0
        logging.basicConfig(level=logging.INFO)

   
    ''' 
    create a new file with content and run it on the target_command_line 
    target command line args is in the format: [[target], [-args]].
    '''

    def fuzz(self, file_save_fuzz_content, content, target_command_line_args):
        assert isinstance(file_save_fuzz_content, str)
        assert isinstance(content, bytearray)
        assert isinstance(target_command_line_args, list)
        # run the target on the sample content with args,
        # if crashed, document the crash in a file and put it in self.crashes_dir
        with open(file_save_fuzz_content, "wb") as fd:
            fd.write(content)

        self.logger.debug(f'running following content: {target_command_line_args + [file_save_fuzz_content]}')
        sp = subprocess.Popen(target_command_line_args + [file_save_fuzz_content],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, )

        ret = sp.wait()
        if ret != 0:
            self.logger.info(f"Exited with {ret}")
            hash = hashlib.sha256(content).hexdigest()
            if ret == -11:
                # SIGSEGV - Invalid memory reference
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGSEGV"),
                     "wb").write(content)
            if ret == -6:
                # SIGABRT - Abort signal from abort()
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGABRT"),
                     "wb").write(content)
            if ret == -7:
                # SIGBUS - Bus error (bad memory access)
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGBUS"),
                     "wb").write(content)
            if ret == -8:
                # SIGFPE - Floating-point exception
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGFPE"),
                     "wb").write(content)
            if ret == -4:
                # SIGILL - Illegal Instruction
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGILL"),
                     "wb").write(content)
            if ret == -31:
                # SIGSYS - Bad system call
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGSYS"),
                     "wb").write(content)
            if ret == -24:
                # SIGXCPU - CPU time limit exceeded
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGXCPU"),
                     "wb").write(content)

    '''
    iterate over samples and fuzz them
    '''

    def fuzz_worker(self, target_command_line_args, fuzz_cycles: Union[int, None]):
        assert isinstance(target_command_line_args, list)

        start_time = time.time()
        t = threading.Thread(target=self.print_statistics, args=[start_time, fuzz_cycles])
        t.start()
        
        #Infinity fuzzing
        if fuzz_cycles == None:
            while True:
                self.generate_fuzz(target_command_line_args)
        
        #Finity fuzzing
        else:
            for _ in range(fuzz_cycles):
                self.generate_fuzz(target_command_line_args)
            
        t.join()


    def generate_fuzz(self, target_command_line_args):
        input_file_content = self.file_generator.generateData()
        
        self.fuzz("thd_0", input_file_content, target_command_line_args)
        self.amount_of_fuzzings += 1



    '''
    print to stdout the statistics about the fuzzing so far
    '''

    def print_statistics(self, start_time, fuzz_cycles):
        while self.amount_of_fuzzings < fuzz_cycles:
            time.sleep(2)
            elapsed = time.time() - start_time
            fscp = float(self.amount_of_fuzzings) / elapsed
            self.logger.info(f"[{elapsed}] cases {self.amount_of_fuzzings} | fcps {fscp}")