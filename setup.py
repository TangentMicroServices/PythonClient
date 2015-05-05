# -*- coding: utf-8 -*-
from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='microclient',
    version='0.0.2',
    author=u'Tangent Solutions',
    author_email='admin@tangentsolutions.co.za',
    packages=['microclient'],
    install_requires=required,
    url='https://github.com/TangentMicroServices/PythonClient',
    license='MIT licence, see LICENCE',
    description='A Python client for interacting with Tangent MicroServices',
    long_description=open('README.md').read(),
)
