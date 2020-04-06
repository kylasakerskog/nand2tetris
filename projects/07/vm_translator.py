from parser import Parser
from codewriter import CodeWriter

from constants import *
import sys
import glob
import os.path

def main():
    if len(sys.argv) < 2:
        print(u"使い方: %s FILENAME" % sys.argv[0])
        sys.exit(1)

    path = sys.argv[1]

    if path.endswith(".vm"): #file
        with CodeWriter(path[:-3] + ".asm") as c:
            translate_file(path, c)
        print("Translated to " + path[:-3] + ".asm")
    else: #dir
        if path.endswith("/"):
            path = path[:-1]
        # glob.glob (PATHを再帰的に取得)
        files = glob.glob("%s/*" % path)
        for f in files:
            if f.endswith(".vm"):
                print(f)            
                with CodeWriter(f[:-3] + ".asm") as c:
                    translate_file(f, c)
        print("Translated to" + path + ".asm")


def translate_file(f, code_writer):
    filename, _ = os.path.splitext(os.path.basename(f))
    code_writer.set_filename(filename)
    with Parser(f) as parser:
        parser.advance()
        while parser.command != None:
            if parser.command_type() == C_ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            elif parser.command_type() == C_PUSH:
                code_writer.write_push_pop(C_PUSH, parser.arg1(), parser.arg2())
            elif parser.command_type() == C_POP:
                code_writer.write_push_pop(C_POP, parser.arg1(), parser.arg2())

            parser.advance()

        
if __name__ == '__main__':
    main()
