import shlex
import sys
import os

infile = sys.argv[1]
outfile = infile.removesuffix('.asm')+'.bin'
intfile = infile.removesuffix('.asm')+'.int'

debug = True

with open(infile) as f:
    p = f.read()

# Asm -> Int
out = [
    f';; {intfile}',
    ';; Happy debugging!\n'
]

labels = {}

def get_indent(line:str):
    while line.endswith(' '):
        line = line.removesuffix(' ')
    return line.count('    ')

debug_include = False
includePath = 'include'

result = ''
def find_depedency(filename, dir = '.'):
    global result
    if debug_include: print(f'[INCLUDE] {'    '*dir.count('/')}{dir.split('/')[-1]}')
    try:
        for i in os.listdir(dir):
            if i == filename:
                result = f'{dir}/{i}'
            if os.path.isdir(f'{dir}/{i}'):
                find_depedency(filename, f'{dir}/{i}')
            elif debug_include: print(f'[INCLUDE]     {'    '*dir.count('/')}{i}')
    except: ...

    return result

i = -1
pos = 0
while i+1 < len(p.split('\n')):
    i += 1
    line = p.split('\n')[i]
    line = line.split(';;')[0]

    if line == '': continue

    out.append(f';; {line.strip()}')
    step = 0

    indent = get_indent(line)
    line = line.strip()
    if indent == 0:
        if line.endswith(':'):
            label = line.removesuffix(':')
            labels[label] = pos
            print(label,pos)

        elif line.startswith('#'):
            line = line.split(' ')

            if line[0] == '#define':
                labels[line[1]] = ' '.join(line[2:])
            
            elif line[0] == '#include':
                name = line[1].strip('"\'<>')
                path = find_depedency(name,includePath)
                if not path:
                    raise FileNotFoundError(f'Dependency "{name}" could not be found.')
                with open(path) as f:
                    p += '\n'
                    p += f.read()
                    p += '\n'


    else:
        opcode, *args = line.split()
        step += 1

        final_args = []

        for arg in args:
            arg = arg.strip()
            if arg.startswith('0b'):
                arg = arg.removeprefix('0b')
                final_args.append(str(int(arg,2)))
            elif arg.startswith('0x'):
                arg = arg.removeprefix('0x')
                final_args.append(str(int(arg,16)))

            elif arg.startswith('!'):
                arg = arg.removeprefix('!')
                out.append(f'set 0b1111 {arg}')
                final_args.append('0b1111')
                step += 3

            elif not arg.isnumeric() and arg not in labels:
                if not arg: arg = ' '
                final_args.append(f'"{arg}"')

            else:
                final_args.append(arg)


        if opcode == 'syscall':
            opcode = 'set 0b0'
            step += 1

        elif opcode in ['beq','bne','bnz','jmp']:
            if 'ret' in p:
                out.append(f'set 0b111 {pos+9}')         # Set return address
                out.append('psh 0 0b111')                # Push it onto call stack
                out.append(f'set 0b110 {final_args[0]}') # Set Jump address
                final_args[0] = '0b110'
                out.append(f'{opcode} {' '.join(final_args)}'.strip())
                out.append('pop 0 0b111')                # Pop it off call stack
                opcode = None
                step += 12
            else:
                out.append(f'set 0b110 {final_args[0]}')
                final_args[0] = '0b110'
                step += 3

        elif opcode == 'ret':
            final_args.append(1)
            if final_args:
                for _ in range(int(final_args[0])):
                    out.append('pop 0 0b111')
            opcode = 'jmp 0b111'
            final_args = []
            step += 4

        pos += step + len(final_args)

        if opcode:
            out.append(f'{opcode} {' '.join(final_args)}'.strip())

# Labels
for i,line in enumerate(out):
    if line.startswith(';'): continue
    for label in sorted(labels,key=lambda x: len(x),reverse=True):
        dest = labels[label]
        if label in line:
            line = line.replace(f'"{label}"',str(dest))
            line = line.replace(label,str(dest))
            out[i] = line

with open(intfile,'w') as f:
    f.write('\n'.join(out))


# Int -> Binary
output = []

with open(intfile) as f:
    for line in f.read().split('\n'):
        if line.startswith(';;'): continue
        if line.strip() == '': continue
        inst, *args = shlex.split(line)

        if inst.strip().replace('\n','') == '' or inst.startswith('#') or inst.startswith('//'):
            continue

        match inst:
            case 'inc':
                output.append(0b0000)

            case 'dec':
                output.append(0b0001)

            case 'mov':
                output.append(0b0010)

            case 'set':
                output.append(0b0011)

            case 'psh':
                output.append(0b0100)

            case 'pop':
                output.append(0b0101)

            case 'beq':
                output.append(0b0110)

            case 'bne':
                output.append(0b0111)

            case 'bnz':
                output.append(0b1000)

            case 'jmp':
                output.append(0b1001)

            case 'and':
                output.append(0b1010)

            case 'or':
                output.append(0b1011)

            case 'xor':
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
            if arg == '': arg = ' '
            if arg.startswith('0b'):
                arg = arg.removeprefix('0b')
                output.append(int(arg,2))
            elif arg.startswith('0x'):
                arg = arg.removeprefix('0x')
                output.append(int(arg,16))
            elif not arg.isnumeric():
                try: output.append(ord(arg))
                except Exception as e:
                    print(arg)
                    raise e
            else:
                output.append(int(arg))

print(len(output))

with open(outfile,'wb') as f:
    f.write(bytes(output))

