#define flags 5
#define sysarg1

main:
    set 31 2
    set 32 3
    set 33 33
    set 34 4

    psh 32 !"H"
    psh 32 !"e"
    psh 32 !"l"
    psh 32 0b1111
    psh 32 !"o"
    psh 32 !","
    psh 32 !32

    psh 31 !"W"
    psh 31 !"o"
    psh 31 !"r"
    psh 31 !"l"
    psh 31 !"d"
    psh 31 !"!"
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111
    psh 31 0b1111

    jmp str_concat
    jmp print

str_concat: ;; 2, 3, 4
    pop 31 33
    bnz _str_concat flags
    psh 34 33
    jmp str_concat

_str_concat:
    set flags 0
    pop 32 33
    bnz print flags
    psh 34 33
    jmp _str_concat

print:
    set flags 0
    pop 34 33
    bnz exit flags
    mov 33 1
    inc 0          ;; Equivalent to syscall 1 LMFAO (saves 1 byte)
    jmp print

exit:
    hlt
