#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='couchbot',
    version='0.1.0',
    author='Petter Friberg',
    author_email='petter_friberg@hotmail.com',
    description='A Slack bot for queuing movies to Couch Potato',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    license='MIT',
    include_package_data=True,
    url='https://github.com/flaeppe/couchbot',
    entry_points={
        'console_scripts': [
            'couchbot = couchbot:main',
        ],
    },
    classifiers=[
        'Topic :: Utilities'
    ],
)