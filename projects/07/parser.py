from constants import *

class Parser:
    def __init__(self, filepath):
        self.command = None
        self.f = open(filepath)

    def __enter__(self):
        # with文に入ったときに__enter__メソッドが呼ばれる
        return self
        
    def __exit__(self, exception_type, exception_value, traceback):
        # with文を抜けるとき__exit__メソッドが呼ばれる
        self.f.close()

    def advance(self):
        # 一行ずつ出力
        while True:
            line = self.f.readline() # => hasMoreCommands()の役割
            if not line:
                self.command = None
                break
            # strip() コマンドで \n を消す
            val = line.strip()
            comment_i = val.find("//")
            if comment_i != -1:
                val = val[:comment_i]
                
            if val != '':
                self.command = val.split()
                return self.command

    def command_type(self):
        # 命令のタイプを出力
        if self.command[0] == "push":
            return C_PUSH
        elif self.command[0] == "pop":
            return C_POP
        elif self.command[0] == "label":
            return C_LABEL
        elif self.command[0] == "goto":
            return C_GOTO
        elif self.command[0] == "if-goto":
            return C_IF
        elif self.command[0] == "function":
            return C_FUNCTION
        elif self.command[0] == "return":
            return C_RETURN
        elif self.command[0] == "call":
            return C_CALL
        elif self.command[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return C_ARITHMETIC

    # C_RETURN のときは arg1 ルーチンを呼ばない
    def arg1(self):
        if self.command_type() == C_ARITHMETIC:
            return self.command[0]
        else:
            return self.command[1]
        
    def arg2(self):
        if self.command_type() in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return self.command[2]
