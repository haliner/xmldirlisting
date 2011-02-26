#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='xmldirlisting',
    version='0.4',
    description='XML Dirlisting',
    author='Stefan Haller',
    author_email='haliner@googlemail.com',
    url='https://launchpad.net/xmldirlisting',
    license = 'GPLv3',
    scripts = ['xmldirlisting'],
    data_files = [('share/xmldirlisting', ['dirlisting.css',
                                           'dirlisting.dtd',
                                           'dirlisting.js',
                                           'dirlisting.xslt'])]
)
