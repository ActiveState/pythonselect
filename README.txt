pythonselect
============

pythonselect is a MacOSX tool to set current Python version. If you have
multiple Python versions installed - say, 2.6, 2.7 and 3.1 - then running the
following will set Python 2.7 to be your current Python:

::

    $ sudo pythonselect 2.7

pythonselect does this by creating appropriate symlinks in ``/usr/local/bin``
targetting the necessary binaries in your non-system framework Python
install.

Credits
=======

pythonselect is based on Komodo_'s internal `set-curr-python.py`_.

.. _Komodo: http://www.activestate.com/komodo/
.. _`set-curr-python.py`: http://svn.openkomodo.com/openkomodo/view/openkomodo/trunk/mozilla/support/set-curr-python.py

Roadmap
=======

Even though this tool is MacOSX-only at the moment, we plan to expand support
for Windows and Linux.

