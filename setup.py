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
        "matplotlib == 3.2.2",
        "sympy == 1.5.1",
        "pyopenms == 2.6.0",
        "molmass == 2020.6.10",
        "escher == 1.6.0",
        "freezegun == 1.1.0",
        "openpyxl == 3.0.6",
        "requests == 2.25.1",
        "lazy_object_proxy == 1.6.0",
        "pypika == 0.48.2",
        "networkx == 2.5.1",
        "nbsphinx == 0.8.3",
        "scipy == 1.6.0",
        "seaborn == 0.11.1",
        "scikit-learn == 0.24.2"
    ],
    # dependency_links=
    include_package_data=True,
)
