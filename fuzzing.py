import mutations
import glob
import subprocess
import os
import hashlib
import random
import time
import threading


class SimpleFuzzer:
    def __init__(self, sample_dir_path, crashes_dir_path):
        self.sample_dir_path = sample_dir_path
        self.crashes_dir_path = crashes_dir_path
        self.samples = self.load_samples()
        self.amount_of_fuzzings = 0

    '''
    load all the samples into a data structure, without duplications.
    there may be two diffrent files with same content, address that.
    '''

    def load_samples(self):
        corpus_filenames = glob.glob(self.sample_dir_path + "/*")
        corpus = set()
        sample_content_dict = {}
        for filename in corpus_filenames:
            previous_corpus_size = len(corpus)
            file_content = open(filename, 'rb').read()
            corpus.add(file_content)
            if len(corpus) != previous_corpus_size:
                sample_content_dict[filename] = file_content
        return sample_content_dict

    ''' 
    create a new file with content and run it on the target_command_line 
    target command line args is in the format: [[target], [-args]].
    '''

    def fuzz(self, file_save_fuzz_content, content, target_command_line_args, sample_name):
        assert isinstance(file_save_fuzz_content, str)
        assert isinstance(content, bytearray)
        assert isinstance(target_command_line_args, list)
        assert isinstance(sample_name, str)
        # run the target on the sample content with args,
        # if crashed, document the crash in a file and put it in self.crashes_dir

        with open(file_save_fuzz_content, "wb") as fd:
            fd.write(content)

        sp = subprocess.Popen(target_command_line_args + [file_save_fuzz_content],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, )

        ret = sp.wait()
        if ret != 0:
            print(f"Exited with {ret}")
            hash = hashlib.sha256(content).hexdigest()
            if ret == -11:
                # duplicate keys: two identical keys with diffrenet values
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_duplicate_keys:{sample_name.split('/')[-1]}"),
                     "wb").write(content)
            if ret == -6:
                # key collision - using different methods so that the parser interperts two keys as identical
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_key_collision:{sample_name.split('/')[-1]}"),
                     "wb").write(content)
            if ret == -7:
                # number decoding - different interpretation of various numbers
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_number_decoding:{sample_name.split('/')[-1]}"),
                     "wb").write(content)
            if ret == -8:
                # comment- using json comments to insert chars
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_comment:{sample_name.split('/')[-1]}"),
                     "wb").write(content)
            if ret == -4:
                # trailing - adding garbage at the end
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_trailing_garbage:{sample_name.split('/')[-1]}"),
                     "wb").write(content)
            if ret == -31:
                # SIGSYS - Bad system call
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGSYS:{sample_name.split('/')[-1]}"),
                     "wb").write(content)
            if ret == -24:
                # SIGXCPU - CPU time limit exceeded
                open(os.path.join(self.crashes_dir_path, f"crash_{hash:64}_SIGXCPU:{sample_name.split('/')[-1]}"),
                     "wb").write(content)

    '''
    iterate over samples and fuzz them
    '''

    def fuzz_worker(self, target_command_line_args):
        assert isinstance(target_command_line_args, list)
        start_time = time.time()
        threading.Thread(target=self.print_statiscs, args=[start_time]).start()
        while True:
            sample_path = random.choice(list(self.samples.keys()))
            sample_content = bytearray(self.samples[sample_path])

            for _ in range(10):
                sample_content[random.randint(0, len(sample_content) - 1)] = random.randint(0, 255)

            self.fuzz("thd_0", sample_content, target_command_line_args, sample_path)
            self.amount_of_fuzzings += 1

    '''
    print to stdout the statistics about the fuzzing so far
    '''

    def print_statiscs(self, start_time):
        while True:
            time.sleep(2)
            elapsed = time.time() - start_time
            fscp = float(self.amount_of_fuzzings) / elapsed
            print(f"[{elapsed}] cases {self.amount_of_fuzzings} | fcps {fscp}")


if __name__ == '__main__':
    # fuzz = SimpleFuzzer("corpus", "crashes")
    fuzz = SimpleFuzzer("corpus2", "crashes_objdump")
    # fuzz_sample = list(fuzz.samples.keys())[0]
    # print("fuzzing on: ", fuzz_sample)
    # uzz.fuzz("thd_0", fuzz.samples[fuzz_sample], ["objdump", "-d"], fuzz_sample)
    fuzz.fuzz_worker(["./binutils/objdump", "-x"])
