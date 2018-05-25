#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "python-logstash"
]

setup(
    name='magic_logger',
    version='0.1.0',
    description="MagicLogger handle Logstash, Stream and File logging",
    long_description=readme,
    author="Raphaël Courivaud",
    author_email='r.courivaud@gmail.com',
    url='https://github.com/rcourivaud/MagicLogger',
    packages=find_packages(include=['magic_logger']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='magic_logger',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
