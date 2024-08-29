import sys

in_file = sys.argv[1]

with open(in_file,'rb') as f:
    p = f.read()

pc = 0b000000000 # Program Counter
sp = 0b000000000 # Stack Pointer
memory = [0b00000000 for _ in range(0b11111111)] # 8 bits (preallocated) of 8 bit memory

stack = []

debug = False

while pc < len(p):
    opcode = p[pc]

    step = 0
    match opcode:
        case 0b0000:
            if debug: print("inc",p[pc+1])
            memory[p[pc+1]] += 1
            step = 2

        case 0b0001:
            if debug: print("dec",p[pc+1])
            memory[p[pc+1]] -= 1
            step = 2

        case 0b0010:
            if debug: print("mov",p[pc+1],p[pc+2])
            memory[p[pc+2]] = memory[p[pc+1]]
            step = 3

        case 0b0011:
            if debug: print("set",p[pc+1],p[pc+2])
            memory[p[pc+1]] = p[pc+2]
            step = 3
        
        case 0b0100:
            if debug: print('psh',memory[p[pc+1]])
            stack.insert(sp,memory[p[pc+1]])
            sp += 1
            step = 2
        
        case 0b0101:
            if debug: print('pop',memory[p[pc+1]])
            try:
                memory[p[pc+1]] = stack.pop()
                sp -= 1
            except:
                if debug: print('Stack err')
                memory[p[pc+1]] = 0b0
                memory[0b101] = 0b1
            step = 2

        case 0b0110:
            if debug: print("beq",p[pc+1],p[pc+2],p[pc+3])
            if memory[p[pc+2]] == memory[p[pc+3]]:
                pc = memory[p[pc+1]]
            else:
                step = 4

        case 0b0111:
            if debug: print("bne",p[pc+1],p[pc+2],p[pc+3])
            if memory[p[pc+2]] != memory[p[pc+3]]:
                pc = memory[p[pc+1]]
            else:
                step = 4
        
        case 0b1000:
            if debug: print("bnz",p[pc+1],p[pc+2])
            if memory[p[pc+2]] != 0:
                pc = memory[p[pc+1]]
            else:
                step = 3

        case 0b1001:
            if debug: print("jmp",memory[p[pc+1]])
            pc = memory[p[pc+1]]

        case 0b1010:
            if debug: print("and",p[pc+1],p[pc+2])
            memory[p[pc+1]] &= memory[p[pc+2]]
            step = 3

        case 0b1011:
            if debug: print("or",p[pc+1],p[pc+2])
            memory[p[pc+1]] |= memory[p[pc+2]]
            step = 3

        case 0b1100:
            if debug: print("xor",p[pc+1],p[pc+2])
            memory[p[pc+1]] ^= memory[p[pc+2]]
            step = 3

        case 0b1101:
            if debug: print("shl",p[pc+1])
            memory[p[pc+1]] <<= 1
            step = 2

        case 0b1110:
            if debug: print("shr",p[pc+1])
            memory[p[pc+1]] >>= 1
            step = 2

        case 0b1111:
            if debug: print("halt")
            exit()
        
        case _:
            print(f'SIGILL - at {pc}: {bin(p[pc])}',file=sys.stderr)
            for i,byte in enumerate(p):
                print(f'{i:4} - {bin(byte)}')
            exit(1)

    if debug: print(stack)

    for i in range(len(memory)):
        if memory[i] > 0b11111111:
            memory[i] %= 0b11111111

    match memory[0b0]:
        case 0b1:
            try: sys.stdout.write(chr(memory[0b1]))
            except Exception as e:
                memory[0b101] = 0b10
        
        case 0b10:
            try: memory[0b100] = ord(sys.stdin.read(1))
            except Exception:
                memory[0b101] = 0b11
        
        case 0b11:
            try: memory[0b100] = sp
            except: ...
        
        case 0b100:
            try: sp = memory[0b1]
            except: ...


    memory[0b0] = 0b00

    pc += step
    

print('NOHALT')
exit(1)
