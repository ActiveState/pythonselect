"""Set the current Python to the given version.

  Usage:
    sudo pysel <pyver>

  where "<pyver>" is "<major>.<minor>" for a Python installed under
  '/Library/Frameworks'.

  Note: We are talking about a non-system framework Python install. I.e. a
  Python installed in '/Library/Frameworks' and '/usr/local/bin'.

  Without <pyver> argument, print the list of installed Pythons.
"""
# Based on
# http://svn.activestate.com/activestate/checkout/komodo/trunk/mozilla/support/set-curr-python.py
from __future__ import print_function

import os
import sys
from glob import glob


class Error(Exception):
    pass


class Platform(object):

    @staticmethod
    def get_current():
        """Return an instance representing the current platform"""
        if sys.platform == 'win32':
            return WindowsPlatform()
        if sys.platform == 'darwin':
            return OSXPlatform()
        else:
            raise NotImplementedError('unsupported platform: %s' % sys.platform)
            
            
class WindowsPlatform(Platform):
    
    def get_installed_pyvers(self):
        # TODO: Use windows registry to get Python install paths
        pyvers = [self._pypath2pyver(d)
                  for d in glob(r"C:\Python??")]
        pyvers.sort(reverse=True)
        return pyvers
    
    def get_default_pyver(self):
        for path in os.environ.get('PATH', '').split(';'):
            if os.path.exists(os.path.join(path, 'python.exe')):
                return self._pypath2pyver(os.path.dirname(path))
    
    def set_curr_python(self, pyver):
        raise NotImplementedError
    
    def _pypath2pyver(self, p):
        if p.endswith('\\'):
            p = os.path.dirname(p)
        assert p.lower().startswith(r'c:\python')
        return '{0[0]}.{0[1]}'.format(p[-2:])
    

class OSXPlatform(Platform):

    def get_installed_pyvers(self):
        """Return the list of PYVERs currently installed"""
        pyvers = [os.path.basename(d) for d in \
                  glob("/Library/Frameworks/Python.framework/Versions/?.?")]
        pyvers.sort(reverse=True)
        return pyvers
        
    def get_default_pyver(self):
        """Return the pyver that is default"""
        return os.path.basename(
            os.path.realpath(
                "/Library/Frameworks/Python.framework/Versions/Current"))
    
    def set_curr_python(self, pyver):
        pyver_dir = "/Library/Frameworks/Python.framework/Versions/"+pyver
        if not os.path.exists(pyver_dir):
            raise Error("'%s' does not exist: you must install Python %s"
                        % (pyver_dir, pyver))
        
        curr_link = "/Library/Frameworks/Python.framework/Versions/Current"
        print("ln -s %s %s" % (pyver, curr_link))
        os.remove(curr_link)
        os.symlink(pyver, curr_link)
        
        for name in ("python", "pythonw", "python-all", "python-32", "python-64",
                     "python-config", "pydoc", "idle", "2to3", "smtpd.py", 
                     "pypm", "virtualenv", "easy_install", "pip"):
            bin_path = os.path.join("/usr/local/bin", name)
            print("reset '%s'" % bin_path)
            fmwk_path = os.path.join(pyver_dir, "bin", name)
            if os.path.lexists(bin_path):
                os.remove(bin_path)
            if os.path.exists(fmwk_path):
                os.symlink(fmwk_path, bin_path)


def main():
    if len(sys.argv[1:]) != 1:
        p = Platform.get_current()
        # Print the list of Pythons installed when no argument is passed
        default_pyver = p.get_default_pyver()
        for pyver in p.get_installed_pyvers():
            status = 'current' if pyver == default_pyver else (
                'type "sudo pythonselect %s" to set as current' % pyver)
            print('\t%s\t(%s)' % (pyver, status))
    elif sys.argv[1] in ('-h', '-?', '--help', 'help'):
        print(__doc__)
    else:
        p.set_curr_python(sys.argv[1])


if __name__ == '__main__':
    main()