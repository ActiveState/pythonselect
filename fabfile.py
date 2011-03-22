import sys
import os.path as P
from fabric.api import *
# Import github.com/srid/fablib
sys.path.append(P.abspath(
    P.join(P.dirname(__file__), 'fablib')))
import venv

clean = venv.clean
init = venv.init
