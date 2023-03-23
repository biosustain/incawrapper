# -*- coding: utf-8 -*-
import re
from setuptools import find_packages, setup


with open("README.md", "r") as doc:
    long_description = doc.read()


version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open("incawrapper/__init__.py").read(),
    re.M,
).group(1)


setup(
    name="incawrapper",
    version=version,
    author="AutoFlow",
    author_email="TBD",
    description=(
        "General Repository for Omics Data Handling tools"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AutoFlowResearch/incawrapper",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    # ],
    # dependency_links=
    include_package_data=True,
)
