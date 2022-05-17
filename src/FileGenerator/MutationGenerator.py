from src.FileGenerator import AbstractBaseFileGenerator
from src.mutation.mutations import BaseMutation, SimpleMutation
import glob
import random
import os

class MutationFileGenerator(AbstractBaseFileGenerator.AbstractBaseFileGenerator):

    def __init__(self, sample_dir_path: str, mutation: BaseMutation):
        self.sample_dir_path = sample_dir_path
        self.mutation = mutation
        self.samples = self.load_samples()


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
            with open(filename, 'rb') as f:
                file_content = f.read()
            corpus.add(file_content)
            if len(corpus) != previous_corpus_size:
                sample_content_dict[filename] = file_content
        return sample_content_dict 


    def generateData(self) -> bytearray:
        sample_path = random.choice(list(self.samples.keys()))
        sample_content = bytearray(self.samples[sample_path])
        return self.mutation.mutate(sample_content)

    def generateFile(self, path: str):
        mutateData = bytes(self.generateData())
        fileObj = open(path, "wb")
        fileObj.write(mutateData)
        fileObj.close()