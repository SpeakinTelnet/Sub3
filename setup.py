#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()
requirements = ["aiohttp"]

test_requirements = ['pytest>=3',]

setup(
    author="SpeakinTelnet",
    author_email='gui.lac@protonmail.com',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    description="A Python aiohttp wrapper client to subscribe to the Ethereum JSON-RPC PubSub endpoints." ,
    install_requires=requirements,
    license='License :: OSI Approved :: MIT License',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='Sub3',
    name='Sub3',
    packages=find_packages(include=['sub3.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SpeakinTelnet/Sub3',
    version='0.0.1',
    zip_safe=False,
)
