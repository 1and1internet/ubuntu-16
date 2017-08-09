"""
Configurability script

Python package configuration

 -==========================================================================-
    Written for python 2.7 because it is included with Ubuntu 16.04 and I
      wanted to avoid requiring that python 3 also be installed.
 -==========================================================================-
"""

from distutils.core import setup
from distutils import util

setup(
    name='configurability',
    version='0.3',
    url='https://github.com/1and1internet/',
    author='Brian Wojtczak',
    author_email='brian.wojtczak@1and1.co.uk',
    package_dir={
        'configurability': 'configurability',
        'configurability.ini_merge_process': util.convert_path('configurability/ini_merge_process'),
    },
    packages=[
        'configurability',
        'configurability.ini_merge_process',
    ],
    install_requires=[
        'PyYAML'
    ],
)
