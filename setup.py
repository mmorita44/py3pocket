#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='py3pocket',
    version='1.0.0',
    description='Python3 package for interacting with Pocket via REST APIs.',
    url='https://github.com/mmorita44/p4pocket',
    author='Masato Morita',
    author_email='m.morita44@hotmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    test_suite='tests')
