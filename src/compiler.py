import sys
import os
from stringReader import StringReader
import shlex

#infile = sys.argv[1]
#outfile = sys.argv[2]
#intfile = outfile.removesuffix('.bin')+'.int'

#with open(infile) as f:
#    source = f.read().split('\n')

# Map variable name to integer address
var = {}


def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    chars = chars.replace('(', ' ( ').replace(')', ' ) ').replace('{', ' { ').replace('}', ' } ').replace("'", '"')
    return shlex.split(chars,posix=False)



print(tokenize(input('> ')))


exit()

out = []

with open(intfile,'w') as f:
    f.write('\n'.join(out))


os.system(f'py intermediary.py {intfile} {outfile}')