# Copyright (c) 2011 ActiveState Software Inc. All rights reserved.

from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '1.3' # + '.dev' 

if (sys.platform not in ['darwin', 'win32']) and 'install' in sys.argv:
    raise SystemExit(
        "error: pythonselect-%s supports only OSX and Windows at the moment, not %s" % (
            version, sys.platform))


setup(name='pythonselect',
      version=version,
      description="A tool to set current Python version",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: System',
            'Topic :: Utilities',
      ],
      keywords='',
      author='ActiveState',
      author_email='activepython-feedback@activestate.com',
      maintainer='Sridhar Ratnakumar',
      maintainer_email='github@srid.name',
      url='http://github.com/ActiveState/pythonselect',
      license='MIT',
      packages=find_packages('.'),
      include_package_data=False,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'pysel = pythonselect.pysel:main',
          ]
      },
      )
