#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
# Created on 2014-11-24 22:27:45


import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

import disproxy

install_requires = [
    'pymongo>=2.7.2',
    'unittest2>=0.5.1',
    'redis'
]

setup(
    name='disproxy',
    version=disproxy.__version__,

    description='A distribute proxy client in Python',
    long_description=long_description,

    url='https://github.com/jasonz93/py-disproxy',

    author='Sihao Zhang',
    author_email='spirit.line.523@gmail.com',

    license='Apache License, Version 2.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'License :: OSI Approved :: Apache Software License',

        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='proxy',

    packages=find_packages(exclude=['tests*']),

    install_requires=install_requires,

    extras_require={
        'test': [
            'unittest2>=0.5.1',
            'coverage',
            'httpbin',
            'pyproxy>=0.1.6',
            'easywebdav',
        ]
    },

    package_data={
        'pyspider': [
            'logging.conf',
            'fetcher/phantomjs_fetcher.js',
            'fetcher/splash_fetcher.lua',
            'webui/static/*.js',
            'webui/static/*.css',
            'webui/templates/*'
        ],
    },

    entry_points={
        'console_scripts': [
            'pyspider=pyspider.run:main'
        ]
    },

    test_suite='tests.all_suite',
)
