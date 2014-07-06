#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup


setup(
    name='felt',
    version='0.1.0',
    description='Fabric extensions for ArchLinux',
    author='Peter Sutton',
    author_email='foxxy@foxdogstudios.com',
    url='https://github.com/foxdog-studios/felt',
    license='BSD',
    packages=[
        'felt',
    ],
    package_data={
        '': ['LICENSE.txt'],
    },
    install_requires=[
        'Fabric==1.9.0',
        'PyYAML==3.11',
        'pathlib==1.0',
    ],
)

