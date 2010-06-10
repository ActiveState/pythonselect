# Based on 
# http://svn.activestate.com/activestate/checkout/komodo/trunk/mozilla/support/set-curr-python.py
import os


class Error(Exception):
    pass


def set_curr_python(pyver):
    pyver_dir = "/Library/Frameworks/Python.framework/Versions/"+pyver
    if not os.path.exists(pyver_dir):
        raise Error("'%s' does not exist: you must install Python %s"
                    % (pyver_dir, pyver))
    
    curr_link = "/Library/Frameworks/Python.framework/Versions/Current"
    print "ln -s %s %s" % (pyver, curr_link)
    os.remove(curr_link)
    os.symlink(pyver, curr_link)
    
    for name in ("python", "pythonw", "python-config", "pydoc", 
                 "idle", "smtpd.py",
                 "pypm", "virtualenv", "easy_install", "pip"):
        bin_path = os.path.join("/usr/local/bin", name)
        print "reset '%s'" % bin_path
        fmwk_path = os.path.join(pyver_dir, "bin", name)
        if os.path.lexists(bin_path):
            os.remove(bin_path)
        if os.path.exists(fmwk_path):
            os.symlink(fmwk_path, bin_path)

