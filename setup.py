"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypfp',
    version='0.0.1',
    description='A Python parallel function processor - a demonstration of the Python multiprocessing library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://localhost',
    author='Nico Coetzee',
    author_email='nicc777@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='Multi Processing Library',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3, <4',
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
