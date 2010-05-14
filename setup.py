from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '1.0b3'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]

if not sys.platform.startswith('darwin'):
    raise SystemExit, "error: pythonselect-%s only works on MacOSX, not %s" % (
        version, sys.platform)

setup(name='pythonselect',
      version=version,
      description="A tool to set current Python version (currently MacOSX only)",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Operating System :: MacOS :: MacOS X',
            'Programming Language :: Python',
            'Topic :: System',
            'Topic :: Utilities',
      ],
      keywords='',
      author='ActiveState',
      author_email='activepython-feedback@activestate.com',
      maintainer='srid',
      maintainer_email='srid@nearfar.org',
      url='http://bitbucket.org/activestate/pythonselect',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'pythonselect = pythonselect.command:main',
          ]
      },
      )
