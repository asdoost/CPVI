import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="CPVI",
    version="v0.1.4-beta",
    description="Comprehensive Persian Verb Inflector",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/asdoost/CPVI",
    download_url = "https://github.com/asdoost/CPVI/archive/refs/tags/v0.1.4-beta.tar.gz",
    author="Abbas Safardoost",
    author_email="a.safardoust@gmail.com",
    license="MIT",
    classifiers=[
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Persian",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["CPVI"],
    package_dir={'CPVI': 'CPVI'},
    package_data={'CPVI': ['data/*.json']},
    install_requires=["pathlib"]
)

