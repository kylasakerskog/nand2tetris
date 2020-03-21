import re

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

A_COMMAND_PATTERN = re.compile(r'@([0-9a-zA-Z_\.\$:]+)')
L_COMMAND_PATTERN = re.compile(r'\(([0-9a-zA-Z_\.\$:]*)\)')
C_COMMAND_PATTERN = re.compile(r'(?:(A?M?D?)=)?([^;]+)(?:;(.+))?')

class Parser:
    def __init__(self, filepath):
        self.command = None
        self.f = open(filepath)

    def __enter__(self):
        # with文に入ったときに__enter__メソッドが呼ばれる
        return self
        
    def __exit__(self, ex_type, ex_val, traceback):
        # with文を抜けるとき__exit__メソッドが呼ばれる
        self.f.close()

    def advance():
        # 一行ずつ出力
        line = f.readline() # => hasMoreCommands()の役割
        while True:
            if not line:
                self.command = None
                break
            line = val.replace(' ', '')
            comment_i = line.find("//")
            if comment_i != -1:
                line = line[:comment_i]
                
            if line != '':
                self.command = line
                break
                
        return self.command

    def commandType():
        # 命令のタイプを出力
        if self.command[0] == '@':
            return A_COMMAND
        elif self.command[0] == '(' :
            return C_COMMAND
        else:
            return L_COMMAND
            
    def symbol():
        # Symbolだけを取得
        cmd_type = commandType()
        if cmd_type == A_COMMAND:
            m = A_COMMAND_PATTERN.match(self.command)
            return m.group(1)
        elif cmd_type == L_COMMAND:
            m = L_COMMAND_PATTERN.match(self.command)
            return m.group(1)
        else:
            raise Exception()
                
    def dest():
        cmd_type = commandType()
        if cmd_type != C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.command)
            return m.group(1)
        else:
            raise Exception()

    def comp():
        cmd_type = commandType()
        if cmd_type != C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.command)
            return m.group(2)
        else:
            raise Exception()

    def jump():
        cmd_type = commandType()
        if cmd_type != C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.command)
            return m.group(3)
        else:
            raise Exception()
