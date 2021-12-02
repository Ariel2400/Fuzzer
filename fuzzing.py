import mutations


class SimpleFuzzer:
    def __init__(self, sample_dir_path, crashes_dir_path, num_of_threads = 1):
        self.sample_dir_path = sample_dir_path
        self.crashes_dir_path = crashes_dir_path
        self.num_of_threads = num_of_threads
        self.samples = self.load_samples()
        self.amount_of_fuzzings = 0

    '''
    load all the samples into a data structure, without duplications.
    there may be two diffrent files with same content, address that.
    '''
    def load_samples(self):

        return {}

    ''' 
    create a new file with sample_content and run it on the target_command_line 
    target command line args is in the format: [[target], [-args]].
    '''
    def fuzz(self, output_file, sample_content, target_command_line_args, sample_name):
        assert isinstance(output_file, str)
        assert isinstance(sample_content, bytearray)
        assert isinstance(target_command_line_args, list)
        assert isinstance(sample_name, str)
        # run the target on the sample content with args,
        # if crashed, document the crash in a file and put it in self.crashes_dir
        pass
    '''
    open num_of_threads threads and in each thread run fuzz with the samples
    '''
    def batch_fuzz(self, target_command_line_args):
        self.fuzz(output_file='', sample_content='', target_command_line_args=[], sample_name='')
    '''
    print to stdout the statistics about the fuzzing so far
    '''
    def print_statiscs(self):
        print('')

