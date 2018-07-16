#!/usr/bin/env python3

import os.path
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pystexchapi',
    version='1.0.0',
    description='https://www.stocks.exchange cryptocurrency exchange API',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Vlsarro',
    author_email='drek.maro@gmail.com',
    url='https://github.com/Vlsarro/pystexchapi',
    install_requires=[
        'requests>=2.19.1'
    ],
    tests_require=[
        'requests-mock>=1.5.0'
    ],
    packages=['pystexchapi'],
    python_requires='>=3.5',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
