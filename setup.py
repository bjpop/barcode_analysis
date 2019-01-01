#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''XXX'''


setup(
    name='barcode_analysis',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['barcode_analysis'],
    package_dir={'barcode_analysis': 'barcode_analysis'},
    entry_points={
        'console_scripts': ['barcode_analysis = barcode_analysis.barcode_analysis:main']
    },
    url='https://github.com/bjpop/barcode_analysis',
    license='LICENSE',
    description=('XXX'),
    long_description=(LONG_DESCRIPTION),
    install_requires=["pysam", "biopython"],
)
