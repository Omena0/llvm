import sys

in_file = sys.argv[1]

with open(in_file,'rb') as f:
    p = f.read()

pc = 0b0000000000000000 # program counter
reg = [0b00000000 for _ in range(0b1111)] # 4 bits of 8 bit registers

debug = False

while pc < len(p):
    opcode = p[pc]

    step = 0
    match opcode:
        case 0b0000:
            if debug: print("inc",p[pc+1])
            reg[p[pc+1]] += 1
            step = 2

        case 0b0001:
            if debug: print("dec",p[pc+1])
            reg[p[pc+1]] -= 1
            step = 2

        case 0b0010:
            if debug: print("mov",p[pc+1],p[pc+2])
            reg[p[pc+2]] = reg[p[pc+1]]
            step = 3

        case 0b0011:
            if debug: print("set",p[pc+1],p[pc+2])
            reg[p[pc+1]] = p[pc+2]
            step = 3

        case 0b0100:
            if debug: print("beq",p[pc+1],p[pc+2],p[pc+3])
            if reg[p[pc+2]] == reg[p[pc+3]]:
                pc = p[pc+1]
            else:
                step = 4

        case 0b0101:
            if debug: print("bne",p[pc+1],p[pc+2],p[pc+3])
            if reg[p[pc+2]] != reg[p[pc+3]]:
                pc = p[pc+1]
            else:
                step = 4
        
        case 0b0110:
            if debug: print("bnz",p[pc+1],p[pc+2])
            if reg[p[pc+2]] != 0:
                pc = p[pc+1]
            else:
                step = 3

        case 0b0111:
            if debug: print("jmp",p[pc+1])
            pc = p[pc+1]

        case 0b1000:
            if debug: print("nop")
            step = 1

        case 0b1001:
            if debug: print("and",p[pc+1],p[pc+2])
            reg[p[pc+1]] &= reg[p[pc+2]]
            step = 3

        case 0b1010:
            if debug: print("or",p[pc+1],p[pc+2])
            reg[p[pc+1]] |= reg[p[pc+2]]
            step = 3

        case 0b1011:
            if debug: print("xor",p[pc+1],p[pc+2])
            reg[p[pc+1]] ^= reg[p[pc+2]]
            step = 3

        case 0b1100:
            if debug: print("not",p[pc+1])
            reg[p[pc+1]] = ~reg[p[pc+1]]
            step = 2

        case 0b1101:
            if debug: print("shl",p[pc+1])
            reg[p[pc+1]] <<= 1
            step = 2

        case 0b1110:
            if debug: print("shr",p[pc+1])
            reg[p[pc+1]] >>= 1
            step = 2

        case 0b1111:
            if debug: print("halt")
            exit()
        
        case _:
            print('SIGILL: ',p[pc])
            exit(1)
    
    for i in range(0b1111):
        reg[i] %= 0b1111111111111111

    match reg[0b1100]:
        case 0b0001:
            try: print(chr(reg[0b1101]),end='')
            except: ...
            reg[0b1100] = 0b0000

    pc += step
    

print('NOHALT')
exit(1)
