import sys
from pythonselect.base import set_curr_python


def main():
    if len(sys.argv[1:]) != 1:
        sys.stderr.write("pythonselect: error: incorrect number "
                         "of arguments\n\n")
        sys.stderr.write(__doc__)
        sys.exit(1) 
    set_curr_python(sys.argv[1])
    