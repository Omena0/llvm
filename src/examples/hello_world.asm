
#define sysarg1 0b1

start:
    psh !"!"
    psh !"d"
    psh !"l"
    psh !"r"
    psh !"o"
    psh !"w"
    psh !32
    psh !","
    psh !"o"
    psh !"l"
    psh !"l"
    psh !"e"
    psh !"H"

loop:
    pop sysarg1
    syscall 1
    bnz halt 0b101
    jmp loop

halt:
    hlt

