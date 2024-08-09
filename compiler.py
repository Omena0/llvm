import sys

infile = sys.argv[1]
outfile = sys.argv[2]

output = []

with open(infile) as f:
    for line in f.read().split('\n'):
        inst, *args = line.split(' ')
        match inst:
            case 'inc':
                output.append(0b0000)

            case 'dec':
                output.append(0b0001)

            case 'mov':
                output.append(0b0010)
            
            case 'set':
                output.append(0b0011)
            
            case 'beq':
                output.append(0b0100)
            
            case 'bne':
                output.append(0b0101)
            
            case 'bnz':
                output.append(0b0110)
            
            case 'jmp':
                output.append(0b0111)
            
            case 'nop':
                output.append(0b1000)
            
            case 'and':
                output.append(0b1001)
            
            case 'or':
                output.append(0b1010)
            
            case 'xor':
                output.append(0b1011)
            
            case 'not':
                output.append(0b1100)
            
            case 'shl':
                output.append(0b1101)
            
            case 'shr':
                output.append(0b1110)
            
            case 'hlt':
                output.append(0b1111)
            
            case _:
                print('SIGILL: ',line)
                exit(1)
            
        
        for arg in args:
            if arg.startswith('0b'):
                arg = arg.removeprefix('0b')
                output.append(int(arg,2))
            elif arg.startswith('0x'):
                arg = arg.removeprefix('0x')
                output.append(int(arg,16))
            else:
                output.append(int(arg))



with open(outfile,'wb') as f:
    f.write(bytes(output))

for i in output:
    print(bin(i))
