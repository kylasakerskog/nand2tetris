import Parser
import Code

def main():
    if len(sys.argv) < 2:
        print(u"使い方: %s FILENAME" % sys.argv[0])
        sys.exit(1)

    asm_file = sys.argv[1]
    
        
    with Parser(asm_file) as hp:

if __name__ == '__main__':
    main()

