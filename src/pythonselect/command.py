"""Set the current Python to the given version.

  Usage:
    sudo pythonselect <pyver>

  where "<pyver>" is "<major>.<minor>" for a Python installed under
  '/Library/Frameworks'.

  Note: We are talking about a non-system framework Python install. I.e. a
  Python installed in '/Library/Frameworks' and '/usr/local/bin'.
"""

import sys
from pythonselect.base import set_curr_python


def main():
    if len(sys.argv[1:]) != 1:
        sys.stderr.write("pythonselect: error: incorrect number "
                         "of arguments\n\n")
        sys.stderr.write(__doc__)
        sys.exit(1) 
    set_curr_python(sys.argv[1])
    