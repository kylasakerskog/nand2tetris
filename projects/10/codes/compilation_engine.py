from constants import *
from jack_tokenizer import JackTokenizer

class CompilationEngine():
    def __init__(self, filepath):
        self.wf = open(filepath[:-5] + ".my.xml", 'w')
        self.tokenizer = JackTokenizer(filepath)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wf.close()
