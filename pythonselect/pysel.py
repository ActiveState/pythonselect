# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.
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
from __future__ import unicode_literals

import os
import sys
from glob import glob

if sys.platform == 'win32':
    import regobj


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
    
    def __init__(self):
        self.env_user = Win32Environment(scope='user')
        self.env_system = Win32Environment(scope='system')
        self.REG_PYTHONCORE = regobj.HKEY_LOCAL_MACHINE.Software.Python.Pythoncore
        
    def _get_path(self, env):
        """Return %PATH% normalized"""
        return list_unique(
            [os.path.normcase(os.path.normpath(p))
            for p in env.getenv('PATH').split(';')])
        
    def _get_pythons(self):
        pythons = {}
        for pyver in self.REG_PYTHONCORE:
            pypath = list(pyver.InstallPath.values())[0].data
            pypath = os.path.normcase(os.path.abspath(pypath))
            pythons[pypath] = pyver.name
        return pythons
            
    def get_installed_pyvers(self):
        return self._get_pythons().values()
        
    def get_default_pyver(self):
        pythons = self._get_pythons()
        # TODO: support user's PATH as well
        for path in self._get_path(self.env_system):
            if os.path.exists(os.path.join(path, 'python.exe')):
                if path in pythons:
                    return pythons[path]
    
    def set_curr_python(self, pyver):
        # 1. re-order %PATH%
        # 2. re-associate .py and .pyw files
        # 3. re-order in AppPath so Start > Run > python will pick this version
        # 4. send broadcast message to all Windows
        pythons = dict_reverse(self._get_pythons())
        pypath = pythons[pyver]
        pypath_scripts = os.path.join(pypath, 'scripts')
        # TODO: support user's PATH as well
        path = self._get_path(self.env_system)
        print(path)
        # put pypath in front of PATH
        path.remove(pypath) if pypath in path else None
        path.remove(pypath_scripts) if pypath_scripts in path else None
        path[0:0] = [pypath, pypath_scripts]
        print(path)
        self.env_system.setenv('PATH', ';'.join(path))
        print('TODO: set .py assoc, AppPath, etc..')
        print('FIXME: you may want to reboot your computer for PATH changes to take effect')
    
    def _pypath2pyver(self, p):
        if p.endswith('\\'):
            p = os.path.dirname(p)
        assert p.lower().startswith(r'c:\python')
        return '{0[0]}.{0[1]}'.format(p[-2:])


# http://code.activestate.com/recipes/577621-manage-environment-variables-on-windows/
class Win32Environment:
    """Utility class to get/set windows environment variable"""
    
    def __init__(self, scope):
        assert scope in ('user', 'system')
        self.scope = scope
        if scope == 'user':
            self.root = regobj.HKEY_CURRENT_USER
            self.subkey = 'Environment'
            self.envkey = getattr(self.root, 'Environment')
        else:
            self.root = regobj.HKEY_LOCAL_MACHINE
            self.subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
            self.envkey = getattr(
                self.root,
                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
            
    def getenv(self, name, default=''):
        try:
            value = self.envkey[name]
        except KeyError:
            return default
        else:
            return value.data
    
    def setenv(self, name, value):
        import win32con
        from win32gui import SendMessage
        try:
            self.envkey[name] = value
        except OSError as e:
            if sys.platform == 'win32' and isinstance(e, WindowsError):
                if e.winerror == 5:
                    # We received 'Access is denied' error, which means that we
                    # are on Vista/Win7 and the user needs to run this script
                    # elevated. XXX: automate this somehow using UAC.
                    raise SystemExit('ERROR: '
                        'Access denied while setting system environment '
                        'variable; please run this program from an '
                        'Administrator prompt: %s' % e)
            raise
        SendMessage(
            win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
    
    

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

def list_unique(l):
    """Return a new list containing unique elements from `l` but preserving order"""
    l2 = []
    found = set()
    for x in l:
        if x not in found:
            found.add(x)
            l2.append(x)
    return l2


def dict_reverse(d):
    """Reverse the keys, values in a dictionary"""
    return dict((v, k) for k, v in d.items())


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
        p = Platform.get_current()
        p.set_curr_python(sys.argv[1])


if __name__ == '__main__':
    main()
