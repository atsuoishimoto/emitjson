import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="emitjson",
    version="0.0.2",
    author="Atsuo Ishimoto",
    description="Help composing objects to build JSON.",
    license="MIT",
    keywords="json",
    url="https://github.com/atsuoishimoto/emitjson",
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    py_modules = ['emitjson']
)
