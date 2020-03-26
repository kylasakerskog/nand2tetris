import re

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

A_COMMAND_PATTERN = re.compile(r"@([0-9a-zA-Z_\.\$:]+)")
L_COMMAND_PATTERN = re.compile(r"\(([0-9a-zA-Z_\.\$:]*)\)")
C_COMMAND_PATTERN = re.compile(r"(?:(A?M?D?)=)?([^;]+)(?:;(.+))?")

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
            val = line.strip().replace(' ', '')
            comment_i = val.find("//")
            if comment_i != -1:
                val = val[:comment_i]
                
            if val != '':
                self.command = val
                break
                
        return self.command

    def commandType(self):
        # 命令のタイプを出力
        if self.command[0] == '@':
            return A_COMMAND
        elif self.command[0] == '(' :
            return L_COMMAND
        else:
            return C_COMMAND
            
    def symbol(self):
        # Symbolだけを取得
        cmd_type = self.commandType()
        if cmd_type == A_COMMAND:
            m = A_COMMAND_PATTERN.match(self.command)
            if not m:
                raise Exception()
            return m.group(1)
        elif cmd_type == L_COMMAND:
            m = L_COMMAND_PATTERN.match(self.command)
            if not m:
                raise Exception()
            return m.group(1)
        else:
            raise Exception()
                
    def dest(self):
        cmd_type = self.commandType()
        if cmd_type == C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.command)
            return m.group(1)
        else:
            raise Exception()

    def comp(self):
        cmd_type = self.commandType()
        if cmd_type == C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.command)
            return m.group(2)
        else:
            raise Exception()

    def jump(self):
        cmd_type = self.commandType()
        if cmd_type == C_COMMAND:
            m = C_COMMAND_PATTERN.match(self.command)
            return m.group(3)
        else:
            raise Exception()
