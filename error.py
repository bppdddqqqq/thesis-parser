import sys
from pprint import pprint as print

class InvalidList:
    invalid = []
    raise_instant = False
    def push(msg):
        if InvalidList.raise_instant:
            raise_invalids()
        InvalidList.invalid.append(msg)

def raise_invalids():
    if len(InvalidList.invalid) == 0:
        return
    for i in InvalidList.invalid:
        print(i)
    sys.exit(-1)