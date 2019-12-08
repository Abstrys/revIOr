#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

setup(
    name="revIOr",
    version="0.1",
    author="Eron Hennessey",
    author_email="eron@abstrys.com",
    description="An auto-updating HTML window for reStructuredText, Markdown and more.",
    license="BSD",
    keywords="restructuredtext markdown text processor renderer view viewer review",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts' : ['revIOr = abstrys.revIOr.app:main'],
        'setuptools.installation': ['eggsecutable = abstrys.revIOr.app:main']
        },
    install_requires = ['docutils', 'commonmark', 'PyGObject', 'abstrys-core']
)

