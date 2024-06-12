from setuptools import setup, find_packages
from dotenv import load_dotenv
import os

load_dotenv('.env')

with(open("README.md", "r")) as f:
    description = f.read()


setup(
    name='sortasaurus_rex',
    version=os.environ.get('VERSION_CODE'),
    packages=find_packages(),
    install_requires=[
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'srex = sortasaurus_rex.srex:main',
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)
