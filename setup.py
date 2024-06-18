"""
Setup file for publishing to pypi
"""

import os
from setuptools import setup, find_packages
from dotenv import load_dotenv

load_dotenv('.env')

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name='sortasaurus_rex',
    version=os.environ.get('VERSION_CODE'),
    packages=find_packages(),
    install_requires=[
        'tqdm~=4.66.4',
        'python-dotenv',
        'setuptools',
        'wheel',
        'twine',
        'build'
    ],
    setup_requires=[
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'srex = sortasaurus_rex.srex:main',
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)
