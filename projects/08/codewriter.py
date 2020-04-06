from constants import *

class CodeWriter():
    def __init__(self, filepath):
        self.f = open(filepath, 'w')
        self.if_label_num = 0
        self.return_label_num = 0
        self.write_init()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.f.close()

    def write_code(self, code):
        self.f.write(code + '\n')

    def write_codes(self, codes):
        self.write_code('\n'.join(codes))
        
    def push_from_d_reg(self):
        self.write_codes([
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ])

    def pop_2_m_reg(self):
        self.write_codes([
            "@SP",
            "M=M-1",
            "A=M"
        ])

    def get_if_label(self):
        self.if_label_num += 1
        return "IF_LABEL" + str(self.if_label_num)

    def get_return_label(self):
        self.return_label_num += 1
        return "RETURN_LABEL" + str(self.return_label_num)

    def write_binary_op(self, command):
        self.pop_2_m_reg()
        self.write_code("D=M")
        self.pop_2_m_reg()
        if command == "add":
            self.write_code("D=D+M")
        elif command == "sub":
            self.write_code("D=M-D")
        elif command == "and":
            self.write_code("D=D&M")
        elif command == "or":
            self.write_code("D=D|M")
        self.push_from_d_reg()

    def write_unary_op(self, command):
        self.write_codes([
            "@SP",
            "A=M-1"
        ])
        if command == "neg":
            self.write_code("M=-M")
        elif command == "not":
            self.write_code("M=!M")

    def write_comp_op(self, command):
        self.pop_2_m_reg()
        self.write_code("D=M")
        self.pop_2_m_reg()
        l1 = self.get_if_label()
        l2 = self.get_if_label()
        if command == "eq":
            comp_type = "JEQ"
        elif command == "gt":
            comp_type = "JGT"
        elif command == "lt":
            comp_type = "JLT"
        self.write_codes([
            "D=M-D",
            "@%s" % l1,
            "D;%s" % comp_type,
            "D=0", #False
            "@%s" % l2,
            "0;JMP",
            "(%s)" % l1,
            "D=-1", #True
            "(%s)" % l2
        ])
        self.push_from_d_reg()
        
    def write_arithmetic(self, command):
        if command in ["add", "sub", "and", "or"]:
            self.write_binary_op(command)
        elif command in ["neg", "not"]:
            self.write_unary_op(command)
        elif command in ["eq", "gt", "lt"]:
            self.write_comp_op(command)

    def push_from_v_segment(self, segment, index):
        if segment == "local":
            register_name = "LCL"
        elif segment == "argument":
            register_name = "ARG"
        elif segment == "this":
            register_name = "THIS"
        elif segment == "that":
            register_name = "THAT"
        self.write_codes([
            "@%s" % register_name,
            "A=M"
        ])
        for i in range(index):
            self.write_code("A=A+1")
        self.write_code("D=M")
        self.push_from_d_reg()
            
    def pop_from_v_segment(self, segment, index):
        if segment == "local":
            register_name = "LCL"
        elif segment == "argument":
            register_name = "ARG"
        elif segment == "this":
            register_name = "THIS"
        elif segment == "that":
            register_name = "THAT"
        self.pop_2_m_reg()
        self.write_codes([
            "D=M",
            "@%s" % register_name,
            "A=M"
        ])
        for i in range(index):
            self.write_code("A=A+1")
        self.write_code("M=D")
        
    def push_from_s_segment(self, segment, index):
        if segment == "temp":
            base_address = TEMP_BASE_ADDRESS
        elif segment == "pointer":
            base_address = POINTER_BASE_ADDRESS
        self.write_code("@%d" % base_address)
        for i in range(index):
            self.write_code("A=A+1")
        self.write_code("D=M")
        self.push_from_d_reg()
        
    def pop_from_s_segment(self, segment, index):
        if segment == "temp":
            base_address = TEMP_BASE_ADDRESS
        elif segment == "pointer":
            base_address = POINTER_BASE_ADDRESS
        self.pop_2_m_reg()
        self.write_codes([
            "D=M",
            "@%d" % base_address
        ])
        for i in range(index):
            self.write_code("A=A+1")
        self.write_code("M=D")
        
    def write_push_pop(self, command, segment, index):
        index = int(index)

        if command == C_PUSH:
            if segment == "constant":
                self.write_codes([
                    "@%d" % index,
                    "D=A"
                ])
                self.push_from_d_reg()
            elif segment in ["local", "argument", "this", "that"]:
                self.push_from_v_segment(segment, index)
            elif segment in ["temp", "pointer"]:
                self.push_from_s_segment(segment, index)
            if segment == "static":
                self.write_codes([
                    "@%s.%d" % (self.filename, index),
                    "D=M"
                ])
                self.push_from_d_reg()

        elif command == C_POP:
            if segment in ["local", "argument", "this", "that"]:
                self.pop_from_v_segment(segment, index)
            elif segment in ["temp", "pointer"]:
                self.pop_from_s_segment(segment, index)
            if segment == "static":
                self.pop_2_m_reg()
                self.write_codes([
                    "D=M",
                    "@%s.%d" % (self.filename, index),
                    "M=D"
                ])

    def set_filename(self, filename):
        self.filename = filename

    # 8章実装
    def set_sp(self, address):
        self.write_codes([
            '@%d' % address,
            'D=A',
            '@SP',
            'M=D'
        ])

    def write_init(self):
        self.set_sp(256)
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        self.write_code("(%s)" % self.get_label_name(label))

    def get_label_name(self, label):
        try:
            return "%s$%s" % (self.function_name, label)
        except AttributeError:
            return "%s$%s" % ("null", label)

    def write_goto(self, label):
        self.write_codes([
            "@%s" % self.get_label_name(label),
            "0;JMP"
        ])

    def write_if(self, label):
        self.pop_2_m_reg()
        self.write_codes([
            "D=M",
            "@%s" % self.get_label_name(label),
            'D;JNE'
        ])

    def write_function(self, function_name, num):
        self.function_name = function_name
        self.write_codes([
            "(%s)" % self.function_name,
            "D=0"
        ])
        for i in range(int(num)):
            self.push_from_d_reg()

    def write_return(self):
        self.write_codes([
            "@LCL",
            "D=M",
            "@R13", # R13 : FRAME = LCL
            "M=D",
            "@5",
            "D=A",
            "@R13",
            "A=M-D",
            "D=M", # D = *(FRAME-5)
            "@R14",
            "M=D" # R14 = RETURN_ADDR
        ])
        self.pop_2_m_reg()
        self.write_codes([
            "D=M",
            "@ARG",
            "A=M",
            "M=D", # ARG = pop()
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D", # SP = ARG + 1
            "@R13",
            "AM=M-1", # A = FRAME - 1, M = FRAME - 1
            "D=M",
            "@THAT",
            "M=D", # THAT = *(FRAME - 1)
            "@R13",
            "AM=M-1", # A = FRAME - 1, M = FRAME - 1
            "D=M",
            "@THIS",
            "M=D", # THIS = *(FRAME - 1)
            "@R13",
            "AM=M-1", # A = FRAME - 1, M = FRAME - 1
            "D=M",
            "@ARG",
            "M=D", # ARG = *(FRAME - 1)
            "@R13",
            "AM=M-1", # A = FRAME - 1, M = FRAME - 1
            "D=M",
            "@LCL",
            "M=D", # LCL = *(FRAME - 1)
            "@R14",
            "A=M",
            "0;JMP"
        ])

    def write_call(self, function_name, num):
        return_label = self.get_return_label()
        self.write_codes([
            "@%s" % return_label,
            "D=A",
        ])
        self.push_from_d_reg()  # push return_address
        self.write_codes([
            "@LCL",
            "D=M"
        ])
        self.push_from_d_reg() # push LCL
        self.write_codes([
            "@ARG",
            "D=M"
        ])
        self.push_from_d_reg() # push ARG
        self.write_codes([
            "@THIS",
            "D=M"
        ])
        self.push_from_d_reg() # push THIS
        self.write_codes([
            "@THAT",
            "D=M"
        ])
        self.push_from_d_reg() # push THAT
        self.write_codes([
            "@SP",
            "D=M",
            "@5",
            "D=D-A",
            "@%d" % int(num),
            "D=D-A",
            "@ARG",
            "M=D", # ARG = SP
            "@SP",
            "D=M",
            "@LCL",
            "M=D", # LCL = SP
            "@%s" % function_name,
            "0;JMP",
            '(%s)' % return_label
        ])
