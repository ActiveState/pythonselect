pythonselect
============

pythonselect is a tool to set the current Python version; it is included with
`ActivePython`_. If you have multiple Python versions installed - say, 2.6, 2.7
and 3.1 - then running the following will set Python 2.7 to be your current
Python:

::

    $ sudo pysel 2.7
    or
    C:\> pysel 2.7

How does it work?
-----------------

On **OSX**, pythonselect creates symlinks in ``/usr/local/bin`` (hence ``sudo``
is required) linking to appropriate binaries in your non-system framework Python
install at ``/Library/Frameworks/Python.framework``.

On **Windows**, pythonselect manipulates the system ``%PATH%`` environment
variable, `AppPath`_ and .py/.pyw associations. You will have to launch a new
Command Prompt. Windows support is **experimental**. Note that on Vista and
Windows 7, ``pysel`` must be run from an Administrator Command Window.


Credits
-------

pythonselect is originally based on Komodo_'s internal `set-curr-python.py`_.


Roadmap
-------

Linux support is on the horizon.


.. _ActivePython: http://activestate.com/activepython/downloads
.. _Komodo: http://www.activestate.com/komodo/
.. _`set-curr-python.py`: http://svn.openkomodo.com/openkomodo/view/openkomodo/trunk/mozilla/support/set-curr-python.py
.. _AppPath: http://msdn.microsoft.com/en-us/library/ee872121(v=vs.85).aspx#app_exe
