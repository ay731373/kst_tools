#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for kstdifferencetool.

    This file was generated with PyScaffold 3.0a10, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup

# Add here console scripts and other entry points in ini-style format
entry_points = """
[console_scripts]
console_scripts = kstdiff = kstdifferencetool.kstdiff:run
"""
# entry_points = """
# [console_scripts]
# script_name = kstdifferencetool.module:function
# For example:
# fibonacci = kstdifferencetool.skeleton:run
# """


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(setup_requires=['pyscaffold>=3.0a0,<3.1a0'] + sphinx,
          entry_points=entry_points,
          use_pyscaffold=True)


if __name__ == "__main__":
    setup_package()
