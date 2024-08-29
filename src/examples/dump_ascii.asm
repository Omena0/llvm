
#define sysarg1 0b1
#define flags 0b101

print:                ;; print a byte stored in the syscall arg1 register
    syscall 0b1       ;; syscall print

start:                ;; The program prints every 8-bit ascii character.
    inc arg1          ;; increment arg1 (syscall does not wipe args)
    bnz print flags   ;; if arg1 is not zero, branch to print
    hlt               ;; Halt
