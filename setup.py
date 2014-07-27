#!/usr/bin/env python3
# -*- coding utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name="Pycorn",
    version="0.1.3",
    packages=find_packages(),
    package_data={
        'pycorn': ['default.conf'],
        },
    include_package_data=True,

    install_requires=['beautifulsoup4>=4.3.2', 'requests'],

    author="Sandro Covo",
    author_email="sandro@covo.ch",
    description="""
                    This packages provides 'pycorntime'a clone
                    of the popular programm popcorntime.
                    It is written in python and provides a cli-interface.
                 """,
    license="GPLv2",
    keywords="torrent yts eztv popcorntime streaming",

    entry_points={
        'console_scripts': [
            'pycorntime = pycorn.main:main_loop',
        ],
    }
)
