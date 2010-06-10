# A Makefile for those not familiar with the Python/buildout build system

PYTHON := python
BUILDOUTOPTS := 

all: checkapy bootstrap buildout

checkapy:
	${PYTHON} -m activestate > /dev/null || \
		(echo "You do not seem be running ActivePython." \
		      "What does 'which ${PYTHON}' say?" && exit 1)

bootstrap:
	${PYTHON} bootstrap.py

buildout:
	bin/buildout ${BUILDOUTOPTS}
	echo "Type bin/pythonselect now"
	
#test:
#	bin/py.test -x -v src --junitxml=tmp/testreport.xml

