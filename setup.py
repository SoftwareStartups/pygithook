#!/usr/bin/env python
"""Setuptools script to build and install the vfgithook"""

from distutils.core import setup

setup (name = 'vfgithook',
    version = '1.0',
    author = 'Vector Fabrics',
    author_email = 'info@vectorfabrics.com',
    url = 'http://vectorfabrics.com',
    description = 'git hooks to check files against Vector Fabrics coding styles',
    license = 'Copyright (c) 2015 Vector Fabrics, all rights reserved',
    packages = ['vfgithook'],
    scripts = ['scripts/vf-pre-commit', 'scripts/pre-commit', 'scripts/vf-update',
    'scripts/update', 'scripts/commit-msg', 'scripts/vf-commit-msg'],
#    install_requires=[
#        'pylint',
#    ],
)
