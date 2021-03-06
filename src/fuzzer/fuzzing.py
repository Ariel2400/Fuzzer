import subprocess
import os
import hashlib
import time
from FileGenerator.AbstractBaseFileGenerator import AbstractBaseFileGenerator
from typing import Union
import threading
import multiprocessing



class Fuzzer:

    def __init__(self, file_generator: AbstractBaseFileGenerator, crashes_dir_path):
        self.file_generator = file_generator
        self.crashes_dir_path = crashes_dir_path
        self.amount_of_fuzzings = 0
        self.stop = False
        self.fuzz_lock = threading.Lock()


    ''' 
    create a new file with content and run it on the target_command_line 
    target command line args is in the format: [[target], [-args]].
    '''

    def fuzz(self, file_save_fuzz_content, content, target_command_line_args, isStdinInput: bool):
        assert isinstance(file_save_fuzz_content, str)
        assert isinstance(content, bytes)
        assert isinstance(target_command_line_args, list)
        sp = None

        # run the target on the sample content with args,
        # if crashed, document the crash in a file and put it in self.crashes_dir
        if isStdinInput:
            sp = subprocess.Popen(target_command_line_args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_data = sp.communicate(input=content)[0]
        else:
            with open(file_save_fuzz_content, "wb") as fd:
                fd.write(content)
            sp = subprocess.Popen(target_command_line_args + [file_save_fuzz_content],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, )

        ret = sp.wait()

        if ret < 0:
            hash = hashlib.sha256(content).hexdigest()
            crash_file_name = ""
            if ret == -11:
                # SIGSEGV - Invalid memory reference
                crash_file_name = f"crash_{hash:64}_SIGSEGV"
                print(f"Exited with SIGSEGV")
            if ret == -6:
                # SIGABRT - Abort signal from abort()
                crash_file_name = f"crash_{hash:64}_SIGABRT"
                print(f"Exited with SIGABRT")
            if ret == -7:
                # SIGBUS - Bus error (bad memory access)
                crash_file_name = f"crash_{hash:64}_SIGBUS"
                print(f"Exited with SIGBUS")
            if ret == -8:
                # SIGFPE - Floating-point exception
                crash_file_name = f"crash_{hash:64}_SIGFPE"
                print(f"Exited with SIGFPE")
            if ret == -4:
                # SIGILL - Illegal Instruction
                crash_file_name = f"crash_{hash:64}_SIGILL"
                print(f"Exited with SIGILL")
            if ret == -31:
                # SIGSYS - Bad system call
                crash_file_name = f"crash_{hash:64}_SIGSYS"
                print(f"Exited with SIGSYS")
            if ret == -24:
                # SIGXCPU - CPU time limit exceeded
                crash_file_name = f"crash_{hash:64}_SIGXCPU"
                print(f"Exited with SIGXCPU")
            with open(os.path.join(self.crashes_dir_path, crash_file_name), "wb") as crash_file:
                crash_file.write(content)
            

    '''
    iterate over samples and fuzz them
    '''

    def fuzz_worker(self, target_command_line_args, fuzz_cycles: Union[int, None], threads_number: Union[int, None], isStdinInput: bool):
        assert isinstance(target_command_line_args, list)

        if(threads_number == None):
            threads_number = multiprocessing.cpu_count() * 2

        start_time = time.time()
        t_statistics = threading.Thread(target=self.print_statistics, args=[start_time])
        t_statistics.start()

        fuzz_threads = []

        for thread_number in range(threads_number):
            t_fuzz = threading.Thread(target=self.fuzzing_loop, args=[thread_number, target_command_line_args, fuzz_cycles, isStdinInput])
            t_fuzz.start()
            fuzz_threads += [t_fuzz]

        t_statistics.join()
        for th in fuzz_threads:
            th.join()


    def fuzzing_loop(self, thread_number: int, target_command_line_args, fuzz_cycles: Union[int, None], isStdinInput: bool):
        #Infinity fuzzing
        if fuzz_cycles == None:
            while True:
                self.generate_fuzz(thread_number, target_command_line_args, isStdinInput, fuzz_cycles)

        #Finity fuzzing
        else:
            while True and not self.stop:
                self.generate_fuzz(thread_number, target_command_line_args, isStdinInput, fuzz_cycles)
                if(self.amount_of_fuzzings >= fuzz_cycles) and not self.stop:
                    self.stop = True
                    


    def generate_fuzz(self, thread_number, target_command_line_args, isStdinInput: bool, fuzz_cycles: Union[int, None]):
        self.fuzz_lock.acquire()
        if fuzz_cycles is not None and self.amount_of_fuzzings >= fuzz_cycles:
            self.file_generator.close()
            self.fuzz_lock.release()
            return
        self.amount_of_fuzzings += 1
        input_file_content = self.file_generator.generateData()
        self.fuzz_lock.release()
        self.fuzz("thd_" + str(thread_number), input_file_content, target_command_line_args, isStdinInput)
    




    '''
    print to stdout the statistics about the fuzzing so far
    '''

    def print_statistics(self, start_time):
        while not self.stop:
            time.sleep(2)
            elapsed = time.time() - start_time
            fscp = float(self.amount_of_fuzzings) / elapsed
            print(f"[{elapsed}] cases {self.amount_of_fuzzings} | fcps {fscp}")