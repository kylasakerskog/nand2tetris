import re
import sys
import os

from Parser import Parser
import Code
from SymbolTable import SymbolTable

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2
SYMBOL_PATTERN = re.compile(r"([0-9]+)|([0-9a-zA-Z_\.\$:]+)")

def main():
    if len(sys.argv) < 2:
        print(u"使い方: %s FILENAME" % sys.argv[0])
        sys.exit(1)

    asm_file = sys.argv[1]
    hack_file = os.path.splitext(asm_file)[0] + ".hack"
    st = SymbolTable()

    # SymbolTable作成
    with Parser(asm_file) as hp:
        # ROM アドレス
        op_address = 0

        # 1行ごとに読みながら, ROMアドレス番号を保持
        while hp.advance() != None:
            cmd_type = hp.commandType()
            if cmd_type == A_COMMAND or cmd_type == C_COMMAND:
                op_address += 1
            elif cmd_type == L_COMMAND:
                st.addEntry(hp.symbol(), op_address)

    # シンボルをアドレスに置き換え, 機械語コードの生成
    with Parser(asm_file) as hp:
        with open(hack_file, 'w') as wf:
            # 1行ごとに構文解析
            while hp.advance() != None:
                cmd_type = hp.commandType()
                # print(cmd_type)

                # A_COMMAND の変数を処理
                if cmd_type == A_COMMAND:
                    symbol = hp.symbol()
                    m = SYMBOL_PATTERN.match(symbol)

                    if m.group(1): # @100など
                        bincode = '0' + int_to_bin(int(m.group(1)))

                    # SymbolTableに書き込み
                    elif m.group(2): # @SYMBOL など
                        # symbol = m.group(2)
                        if st.contains(symbol):
                            address = st.getAddress(symbol)
                            bincode = '0' + int_to_bin(address, 15)
                        else:
                            st.addVariable(symbol)
                            address = st.getAddress(symbol)
                            bincode = '0' + int_to_bin(address, 15)

                elif cmd_type == C_COMMAND:
                    bincode = "111" + Code.comp(hp.comp()) + Code.dest(hp.dest()) + Code.jump(hp.jump())
                    
                if cmd_type != L_COMMAND:
                    wf.write(bincode + '\n')
                    
            

def int_to_bin(val, bits=15):
    binval = bin(val)[2:]
    if len(binval) > bits:
        raise Exception()
    return '0' * (bits - len(binval)) + binval
    

if __name__ == '__main__':
    main()

