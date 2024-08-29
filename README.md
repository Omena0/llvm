
# LLVM

A Low Level Virtual Machine in python. (obviously not very performant)

Also has a compiler

## LLVM Instructions

```list
0000: inc - Increment a register
0001: dec - Decrement a register
0010: mov - Copy a register
0011: set - Set a register to a value
0100: psh - Push a register to the stack
0101: pop - Pop and get a value from the stack
0110: beq - Branch if equal
0111: bne - Branch if not equal
1000: bnz - Branch if not zero
1001: jmp - Jump
1010: and - And 2 registers
1011: or - Or 2 registers
1100: xor - Xor 2 registers
1101: shl - Shift left
1110: shr - Shift right
1111: hlt - Halt (exit)
```

## Registers

8 bit registers

### Special registers

```list
0b0    - does syscall
0b1    - syscall arg 1
0b11   - syscall arg 2
0b100  - syscall return
0b101  - flags
0b110  - jump address
0b111  - return address
0b1111 - Assembler temp register
```

## Syscalls

```list
0b0:   no call
0b1:   print    - Print a byte
0b10   input    - Get a byte from stdin
0b11   getstack - Get stack pointer
0b100  setstack - Set stack pointer
```

more soon

## Flags

```list
0b0   - No flag
0b1   - Stack err
0b10  - Print err
0b11  - Input err
```

## Example program

```asm

#define arg1 0b1

print:                ;; print a byte stored in the syscall arg1 register
    syscall 0b0001    ;; print syscall

start:                ;; The program prints every 8-bit ascii character.
    inc arg1          ;; increment arg1 (syscall does not wipe args)
    bnz print arg1    ;; if arg1 is not zero, branch to print
    hlt               ;; Halt

```

## Using the llvm

Syntax:
py llvm.py \<filename>

## Using the compiler

Syntax:
py compiler.py \<filename> \<outfilename>
