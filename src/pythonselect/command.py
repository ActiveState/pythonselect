"""Set the current Python to the given version.

  Usage:
    sudo pythonselect <pyver>

  where "<pyver>" is "<major>.<minor>" for a Python installed under
  '/Library/Frameworks'.

  Note: We are talking about a non-system framework Python install. I.e. a
  Python installed in '/Library/Frameworks' and '/usr/local/bin'.

  Without <pyver> argument, print the list of installed Pythons.
"""

import sys

from pythonselect.base import set_curr_python, get_installed_pyvers, \
                              get_default_pyver


def main():
    if len(sys.argv[1:]) != 1:
        # Print the list of Pythons installed when no argument is passed
        default_pyver = get_default_pyver()
        for pyver in get_installed_pyvers():
            status = 'current' if pyver == default_pyver else (
                'type "sudo pythonselect %s" to set as current' % pyver)
            print('\t%s\t(%s)' % (pyver, status))
    elif sys.argv[1] in ('-h', '-?', '--help', 'help'):
        print(__doc__)
    else:
        set_curr_python(sys.argv[1])
    
