#! /bin/python
#
#
# @file: setup
# @time: 2022/02/03
# @author: Mori
#

from setuptools import setup, find_packages
from moreover import __version__ as VERSION

requirements = []
with open("requirements.txt", "r") as _f:
    requirements = [x.strip() for x in _f.readlines()]
print(requirements)
print(find_packages())

setup(
    name="moreover",
    version=VERSION,
    description="Mori Personal Utils",
    author="moridisa",
    author_email="moridisa@moridisa.cn",
    url="https://github.com/moriW/moreover",
    license="MIT",
    py_modules=["moreover"],
    packages=find_packages(),
    install_requires=requirements,
    package_data={"moreover": ["template/*.j2"]},
    entry_points={"console_scripts": ["mori=moreover.base:cli"]},
)
