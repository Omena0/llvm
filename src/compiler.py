import sys
import os
from stringReader import StringReader
import shlex

infile = sys.argv[1]
#outfile = sys.argv[2]
#intfile = outfile.removesuffix('.bin')+'.int'

with open(infile) as f:
    source = f.read()

# Map variable name to integer address
var = {}

OPEN_PAREN      = 'T_OPEN_PAREN'
CLOSE_PAREN     = 'T_CLOSE_PAREN'
OPEN_SCOPE      = 'T_OPEN_SCOPE'
CLOSE_SCOPE     = 'T_CLOSE_SCOPE'
OPEN_STRING     = 'T_OPEN_STRING'
CLOSE_STRING    = 'T_CLOSE_STRING'
PLUS            = 'T_PLUS'
MINUS           = 'T_MINUS'
STAR            = 'T_STAR'
SLASH           = 'T_SLASH'
ASSIGN          = 'T_ASSIGN'
EQUAL           = 'T_EQUAL'
GREATER_THAN    = 'T_GRATER_THAN'
LESS_THAN       = 'T_LESS_THAN'
GREATER_THAN_E  = 'T_GREATER_THAN_E'
LESS_THAN_E     = 'T_LESS_THAN_E'
INCREMENT       = 'T_INCREMENT'
NEWLINE         = 'T_NEWLINE'
SPACE           = 'T_SPACE'
SEMICOLON       = 'T_SEMICOLON'


def tokenize_char(chars):
    global i
    if i >= len(chars): return
    char = chars[i]

    match char:
        case '(':
            token = OPEN_PAREN
        case ')':
            token = CLOSE_PAREN
        case '{':
            token = OPEN_SCOPE
        case '}':
            token = CLOSE_SCOPE
        case '"':
            token = OPEN_STRING
        case "'":
            token = OPEN_STRING
        case '+':
            match chars[i-1]:
                case '+':
                    token = INCREMENT
                    i += 1
                case _:
                    if chars[i+1] == '+':
                        token = INCREMENT
                        i += 1
                    else:
                        token = PLUS

        case '-':
            token = MINUS
        case '*':
            token = STAR
        case '/':
            token = SLASH
        case '=':
            match chars[i+1]:
                case '=':
                    token = EQUAL
                    i += 1
                case _:
                    token = ASSIGN
        case '>':
            match chars[i+1]:
                case '=':
                    token = GREATER_THAN_E
                    i += 1
                case _:
                    token = GREATER_THAN

        case '<':
            match chars[i+1]:
                case '=':
                    token = LESS_THAN_E
                    i += 1
                case _:
                    token = LESS_THAN

        case '\n':
            token = NEWLINE
        
        case ';':
            token = SEMICOLON

        case _:
            i += 1
            next = tokenize_char(chars)
            if not next:
                return ''

            if next.startswith('T_'):
                token = char
                i -= 1

            else:
                token = f'{char}{next}'

    return token

def tokenize(chars: str) -> list:
    # sourcery skip: while-to-for
    "Convert a string of characters into a list of tokens."
    global i
    tokens = []
    
    i = 0
    while i < len(chars):
        token = tokenize_char(chars)

        tokens.append(token)
        i += 1

    final_tokens = []

    in_string = False
    for i,token in enumerate(tokens):
        if not token.strip(): continue
        if token.startswith('#'): continue

        if token == OPEN_STRING:
            if in_string:
                token = CLOSE_STRING
            in_string = not in_string

        token = token.strip()
        final_tokens.append(token)

    return final_tokens

def parse_tree(tokens):
    "Parse a list of tokens into an abstract syntax tree."
    tree = []

for i in tokenize(source): print(i)

exit()

out = []

with open(intfile,'w') as f:
    f.write('\n'.join(out))


os.system(f'py intermediary.py {intfile} {outfile}')