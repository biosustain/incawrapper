# -*- coding: utf-8 -*-
import re
from setuptools import setup
import setuptools

with open("README.md", "r") as doc:
    long_description = doc.read()


version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open("BFAIR/__init__.py").read(),
    re.M,
).group(1)


setup(
    name="BFAIR",
    version=version,
    author="AutoFlow",
    author_email="TBD",
    description=(
        "General Repository for Omics Data Handling tools"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AutoFlowResearch/BFAIR",
    packages=setuptools.find_packages(),
    # entry_points={
    #     "console_scripts": [
    #         "BFAIR = BFAIR.__main__:main"
    #     ]
    # },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "flake8",
        "cobra == 0.19.0",
        "pytfa == 0.9.3",
        "pandas == 1.1.5",
        "sympy == 1.5.1",
        "pyopenms == 2.6.0",
    ],
    # dependency_links=
    include_package_data=True,
)
