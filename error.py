import sys

def flush_invalids(invalid = []):
    for i in invalid:
        print(f"{i[1]} :: {i[0]} - {' '.join(map(lambda x: str(x), i[2:]))}")
    invalid.clear()

def raise_invalids(invalid = []):
    flush_invalids(invalid)
    sys.exit(1)
