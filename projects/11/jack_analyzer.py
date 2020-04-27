from constants import *
from compilation_engine import *
import glob
import os.path
import sys
from vm_writer import VmWriter

def main():
    if len(sys.argv) < 2:
        print(u"使い方: %s FILENAME" % sys.argv[0])
        sys.exit(1)

    path = sys.argv[1]

    if path.endswith(".jack"):  # file
        compile(path)

    else:  # directory
        if path.endswith("/"):
            path = path[:-1]
        files = glob.glob("%s/*" % path)
        for filepath in files:
            if filepath.endswith(".jack"):
                compilation(filepath)

def compilation(filepath):
    with VmWriter(filepath[:-5] + ".vm") as code_writer:
        with CompilationEngine(filepath, code_writer) as ce:
            print("compiling %s ..." % filepath)
            ce.compile()

if __name__ == '__main__':
    main()

