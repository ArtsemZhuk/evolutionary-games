#!python
# cython: language_level=3

from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "enginep",
        ["enginep.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='enginep',
    ext_modules=cythonize(ext_modules),
)