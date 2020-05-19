#!python
#cython: language_level=3
from setuptools import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize('engine.pyx'))