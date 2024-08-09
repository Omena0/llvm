
# LLVM Instructions

```list
0000: inc - Increment a register
0001: dec - Decrement a register
0010: mov - Copy a register
0011: set - Set a register to a value
0100: beq - Branch if equal
0101: bne - Branch if not equal
0110: bnz - Branch if not zero
0111: jmp - Jump
1000: nop - No operation
1001: and - And 2 registers
1010: or - Or 2 registers
1011: xor - Xor 2 registers
1100: not - Not a register
1101: shl - Shift left
1110: shr - Shift right
1111: hlt - Halt (exit)
```

## Registers

4 bit registers

0000 - 1111

11-- does syscall

# Syscalls

```list
0001: print - Print a byte
```

more soon

# Example program

```asm
inc 0b1101         # Increment syscall arg 1
set 0b1100 0b0001  # Syscall 1 (print)
bnz 0b0000 0b1101  # Branch if not zero
hlt                # Halt
```
