#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()

requirements = [
    'kombu>=3.0.16',
    'cryptography>=0.5.4',
]

test_requirements = [
    'mock>=1.0.1',
    'PyYaml>=3.11',
    'msgpack-python>=0.4.2',
]

setup(
    name='kombu-encrypted-serializer',
    version='0.1.0',
    description='Kombu encrypted serializer',
    long_description=readme,
    author='Bryan Shelton',
    author_email='bryan@rover.com',
    url='https://github.com/roverdotcom/kombu-encrypted-serializer',
    packages=[
        'kombu_encrypted_serializer',
    ],
    package_dir={'kombu_encrypted_serializer':
                 'kombu_encrypted_serializer'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='kombu_encrypted_serializer',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
